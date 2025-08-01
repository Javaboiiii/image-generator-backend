document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');
    const connectionStatus = document.querySelectorAll('#connection-status');
    const clientIdSpan = document.getElementById('client-id');
    
    let socket = null;
    
    connectToServer();

    window.addEventListener('beforeunload', () => {
        if (socket) {
            socket.disconnect();
        }
    });
    
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    function connectToServer() {
        if (socket) return; 
        
        try {
            socket = io(window.location.origin, {
                reconnection: true,
                reconnectionAttempts: 5,
                reconnectionDelay: 1000,
                reconnectionDelayMax: 5000,
                timeout: 20000,
                transports: ['websocket', 'polling']
            });
            
            socket.on('connect', () => {
                connectionStatus.forEach(status => {
                    status.textContent = 'Connected';
                    status.classList.remove('disconnected');
                    status.classList.add('connected');
                });
                clientIdSpan.textContent = socket.id;
                
                addMessage('System', `Connected to server with ID: ${socket.id}`, 'system');
            });
            
            socket.on('recieve_message', (message) => {
                addMessage('Other User', message, 'received');
            });
            
            socket.on('disconnect', () => {
                handleDisconnect('Server disconnected');
            });
            
            // Connection error
            socket.on('connect_error', (error) => {
                addMessage('System', `Connection error: ${error.message}`, 'system');
                handleDisconnect('Connection failed');
                
                // Don't manually reconnect, let Socket.IO handle reconnection
                // The built-in reconnection logic will handle it based on our options
            });
            
        } catch (error) {
            addMessage('System', `Error: ${error.message}`, 'system');
        }
    }
    
    function sendMessage() {
        if (!socket || !socket.connected) {
            addMessage('System', 'Not connected to server', 'system');
            // Try to reconnect
            connectToServer();
            return;
        }
        
        const message = messageInput.value.trim();
        
        if (!message) return;
        
        // Send message through socket
        socket.emit('send_message', {
            id: socket.id, // Using own ID for global broadcast
            message: message
        });
        
        // Add message to UI
        addMessage('You', message, 'sent');
        
        // Clear input
        messageInput.value = '';
    }
    
    // Helper to add message to UI
    function addMessage(sender, content, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', type);
        
        const time = new Date().toLocaleTimeString();
        
        messageElement.innerHTML = `
            ${content}
            <div class="time">${time}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Handle disconnection
    function handleDisconnect(reason) {
        addMessage('System', reason, 'system');
        
        // Update UI for disconnected state
        connectionStatus.forEach(status => {
            status.textContent = 'Disconnected';
            status.classList.remove('connected');
            status.classList.add('disconnected');
        });
        clientIdSpan.textContent = 'Not connected';
        
        // Don't set socket to null, just let the reconnection logic handle it
        // If we need to completely disconnect, we should call socket.disconnect() first
    }
});
