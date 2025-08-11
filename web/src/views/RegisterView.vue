<template>
  <div>
    <h1>Register Doctor</h1>
    <p v-if="logged">Only admins can see this!</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      logged: false,
    };
  },
  mounted() {
    document.cookie.split(';').forEach(cookie => {
      if (cookie.trim().startsWith('session=')) {
        this.logged = true;
      }
    });
    if (!this.logged) {
      window.location.href = '/';
    }
  },
}
</script>