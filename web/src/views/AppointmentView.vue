<template>
  <div>
    <div class="w-full max-w-md bg-white p-6 rounded-lg shadow-md justify-center mx-auto mt-4">
      <h2 class="text-2xl font-bold mb-4">Available Appointments</h2>
      <form class="mb-4" @submit.prevent="handlerTakeAppointment">
        <select
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 mb-4"
          v-model="selectedAppointment"
          v-html="available">
        </select>
        <button type="submit"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition duration-200">Take</button>
      </form>
    </div>

    <div class="max-w-2xl bg-white p-6 rounded-lg shadow-md justify-center mx-auto mt-4">
      <h2 class="text-2xl font-bold mb-4">Your Appointments</h2>
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Doctor</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody v-html="appointments"></tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      logged: false,
      user: '',
      available: '<option value="none">No available appointments.</option>',
      appointments: '<tr><td colspan="4" class="px-6 py-4 text-center text-gray-500">No appointments found.</td></tr>',
      selectedAppointment: null,
      comments: '',
    };
  },
  mounted() {
    document.cookie.split(';').forEach(cookie => {
      if (cookie.trim().startsWith('session=')) {
        this.logged = true;
      }
      if (cookie.trim().startsWith('user=')) {
        this.user = cookie.split('=')[1];
      }
    });
    if (!this.logged) {
      window.location.href = '/';
    }
    this.fetchAvailableAppointments();
    this.fetchUserAppointments();
  },
  methods: {
    fetchAvailableAppointments() {
      axios.get('/api/appointments')
        .then(response => {
          const availableAppointments = response.data;
          this.available = availableAppointments;
        })
        .catch(error => {
          console.error('Error fetching appointments:', error);
        });
    },
    fetchUserAppointments() {
      axios.get(`/api/appointments/user/${this.user}`)
        .then(response => {
          const userAppointments = response.data;
          if (userAppointments.length === 0) {
            return;
          }
          this.appointments = userAppointments;
        })
        .catch(error => {
          console.error('Error fetching user appointments:', error);
        });
    },
    handlerTakeAppointment() {      
      axios.post(`/api/appointments/${this.selectedAppointment}`)
        .then(response => {
          console.log('Appointment taken:', response.data);
          alert('Appointment taken successfully!');
          this.fetchAvailableAppointments();
          this.fetchUserAppointments();
        })
        .catch(error => {
          console.error('Error taking appointment:', error);
        });
    },
  },
}
</script>