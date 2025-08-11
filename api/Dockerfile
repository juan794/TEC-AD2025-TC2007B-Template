FROM python:3.13
USER root
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y pandoc texlive-latex-base

EXPOSE 5000
CMD ["python", "app.py"]