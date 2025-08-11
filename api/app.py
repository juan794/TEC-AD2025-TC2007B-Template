import os
import psycopg2 # type: ignore
import subprocess # type: ignore
from flask import Flask, request, jsonify, make_response # type: ignore

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'project'

def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route("/appointments/<appointment_id>", methods=["POST"])
def postAppointments(appointment_id):
    try:
        user_id = request.cookies.get("user")
        app.logger.info(f"User ID: {user_id}, Appointment ID: {appointment_id}")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE appointments SET user_id='{user_id}' WHERE id='{appointment_id}'")
        conn.commit()
        
        return jsonify({"message": "Appointment booked successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error booking appointment: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/appointments", methods=["GET"])
def getAppointments():
    try:
        conn = get_connection()
        if conn is None:
            app.logger.error("Database connection failed")
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, u.name, a.appointment_date, a.appointment_time 
            FROM appointments a
                INNER JOIN users u ON u.id = a.doctor_id
            WHERE a.user_id IS NULL
        """)
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return """
            <option selected>Choose an appointment</option>
            """ + "".join([f"<option value='{appointment[0]}'>{appointment[1]} - {appointment[2]} {appointment[3]}</option>" for appointment in appointments]) + """
        """
    except Exception as e:
        app.logger.error(f"Error fetching appointments: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@app.route("/appointments/user/<user_id>", methods=["GET"])
def getUserAppointments(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT a.id, a.appointment_date, a.appointment_time, u.name 
            FROM appointments a
                INNER JOIN users u ON u.id = a.doctor_id
            WHERE a.user_id='{user_id}'
        """)
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not appointments:
            app.logger.info(f"No appointments found for user: {user_id}")
            return jsonify([]), 200
        
        rows_html = ""
        for appointment in appointments:
            rows_html += f"""
            <tr>
                <td class="px-6 py-4 whitespace-nowrap">{appointment[1]}</td>
                <td class="px-6 py-4 whitespace-nowrap">{appointment[2]}</td>
                <td class="px-6 py-4 whitespace-nowrap">{appointment[3]}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <button class="bg-blue-500 text-white py-2 px-4 rounded-lg mr-2"
                        onclick="window.open('/api/appointments/pdf?appointment_id=' + {appointment[0]}, '_blank')">PDF</button>
                </td>
            </tr>
            """
        return rows_html, 200
        
    except Exception as e:
        app.logger.error(f"Error fetching user appointments: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/appointments/pdf", methods=["GET"])
def getAppointmentPDF():
    try:
        appointment_id = request.args.get('appointment_id')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT u.name, a.appointment_date, a.appointment_time 
            FROM appointments a
                INNER JOIN users u ON u.id = a.doctor_id
            WHERE a.id='{appointment_id}'
        """)
        appointment = cursor.fetchone()
        
        doctor_name, appointment_date, appointment_time = appointment
        app.logger.info(f"Generating PDF for appointment: {appointment_id}, Doctor: {doctor_name}, Date: {appointment_date}, Time: {appointment_time}")

        command = [
            "pandoc",
            "default.md",
            "--template", f"appointment_template.latex",
            "--variable", f"doctor:{doctor_name}",
            "--variable", f"date:{appointment_date}",
            "--variable", f"time:{appointment_time}",
            "-o", "appointment.pdf",
        ]
        templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=templates_dir
        )

        if result.returncode != 0:
            app.logger.error(f"Pandoc error: {result.stderr}")
            return jsonify({"error": "Failed to generate PDF"}), 500
        
        app.logger.info("PDF generated successfully")
        with open("./templates/appointment.pdf", "rb") as pdf_file:
            response = make_response(pdf_file.read())
            response.headers.set('Content-Type', 'application/pdf')
            response.headers.set('Content-Disposition', 'attachment', filename='appointment.pdf')
            return response
        
    except Exception as e:
        app.logger.error(f"Error generating PDF: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, role, password FROM users WHERE email='{email}'")
        user = cursor.fetchone()
        if user is None:
            app.logger.error(f"User not found: {email}")
            return jsonify({"error": "User not found"}), 404
        
        if user[2] != password:
            app.logger.error(f"Incorrect password for user: {email}")
            return jsonify({"error": "Incorrect password"}), 401
        
        response = make_response(jsonify({"message": "Login successful"}), 200) 
        response.set_cookie("user", str(user[0]))
        response.set_cookie("role", user[1])
        response.set_cookie("session", random_session_token())
        return response
    except Exception as e:
        app.logger.error(f"Error during login: {e}")
        return jsonify({"error": "Internal server error"}), 500

def random_session_token() -> str:
    return "random_session_token"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)