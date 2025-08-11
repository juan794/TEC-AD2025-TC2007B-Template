<template>
  <div class="flex items-center justify-center min-h-screen">
    <div v-if="!logged">
      <form class="w-full max-w-sm bg-white p-6 rounded-lg shadow-md" @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 font-medium mb-2">Email:</label>
          <input type="email" id="email" v-model="email" required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 font-medium mb-2">Password:</label>
          <input type="password" id="password" v-model="password" required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <button type="submit"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200">Login</button>
      </form>
    </div>
    <div v-else>
      <h1 class="text-4xl font-bold">Welcome!</h1>
      <button type="button" @click="handleLogout"
        class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200">Logout</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      logged: false,
    };
  },
  mounted() {
    document.cookie.split(';').forEach(cookie => {
      if (cookie.trim().startsWith('session=')) {
        this.logged = true;
      }
    });
  },
  methods: {
    handleLogin() {
      axios.post('/api/login', {
        email: this.email,
        password: this.password
      }, { withCredentials: true }).then(response => {
        window.location.reload();
      }).catch(error => {
        console.error('Login error:', error);
      });
    },
    handleLogout() {
      document.cookie.split(';').forEach(cookie => {
        document.cookie = cookie.replace(/^ +/, '').replace(/=.*/, `=;expires=${new Date().toUTCString()};path=/`);
      });
      window.location.reload();
    }
  }
};
</script>