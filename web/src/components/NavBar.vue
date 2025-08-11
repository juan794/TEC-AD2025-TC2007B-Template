<template>
    <div class="bg-blue-400 rounded-lg p-4">
        <ul class="flex justify-center space-x-4">
            <li>
                <RouterLink activeClass="p-1 rounded bg-blue-300 font-bold" to="/">Home</RouterLink>
            </li>
            <li>
                <RouterLink activeClass="p-1 rounded bg-blue-300 font-bold" to="/appointment">Appointment</RouterLink>
            </li>
            <li v-if="isAdmin || isDoctor">
                <RouterLink activeClass="p-1 rounded bg-blue-300 font-bold" to="/chat">DoctorGPT</RouterLink>
            </li>
        </ul>
    </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'

export default {
    name: 'NavBar',
    components: {
        RouterLink,
        RouterView
    },
    data() {
        return {
            isAdmin: false,
            isDoctor: false,
        };
    },
    mounted() {
        document.cookie.split(';').forEach(cookie => {
            if (cookie.trim().startsWith('role=admin')) {
                this.isAdmin = true;
            }
            if (cookie.trim().startsWith('role=doctor')) {
                this.isDoctor = true;
            }
        });
    },
}
</script>