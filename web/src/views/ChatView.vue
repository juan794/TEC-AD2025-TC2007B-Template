<template>
    <div class="flex flex-col h-[80vh] bg-gray-100">
        <div class="flex-1 overflow-y-auto p-4 space-y-4">
            <div v-for="message in messages" :key="message.id" class="message p-3 rounded-lg"
                :class="{ 'bg-blue-500 text-white self-end': message.isUser, 'bg-gray-300 text-black self-start': !message.isUser }">
                <p>{{ message.text }}</p>
            </div>
        </div>
        <div class="chat-input bg-white p-4 border-t">
            <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..."
                class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            messages: [],
            newMessage: ''
        };
    },
    methods: {
        async sendMessage() {
            if (this.newMessage.trim() === '') return;
            this.messages.push({ id: Date.now(), text: this.newMessage, isUser: true });
            const userMessage = this.newMessage;
            this.newMessage = '';

            try {
                axios.post('/ollama/api/generate', {
                    model: 'llama3.2:1b',
                    prompt: userMessage,
                    stream: false,
                })
                    .then(response => {

                        this.messages.push({ id: Date.now(), text: response.data.response, isUser: false });
                    })
                    .catch(error => {
                        console.error('Error fetching AI response:', error);
                        this.messages.push({ id: Date.now(), text: 'Error fetching AI response.', isUser: false });
                    });
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
    },
    mounted() {
        // Initialize chat with a welcome message
        axios.get('/ollama/api/tags').then(response => {
            console.log('Tags:', response.data);
        }).catch(error => {
            console.error('Error fetching tags:', error);
        });
    }
};
</script>