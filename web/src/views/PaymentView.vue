<template>
    <div class="w-full max-w-sm bg-white p-6 rounded-lg shadow-md mx-auto mt-4">
        <h1 class="text-4xl font-bold">Top-up</h1>
        <div class="mt-4">
            <button class="w-full bg-blue-500 text-white py-2 px-4 rounded mb-2 hover:bg-blue-600" @click="topUp(10)">
                $10
            </button>
            <button class="w-full bg-blue-500 text-white py-2 px-4 rounded mb-2 hover:bg-blue-600" @click="topUp(20)">
                $20
            </button>
            <button class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600" @click="topUp(50)">
                $50
            </button>
        </div>
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