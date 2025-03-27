document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    let isConversationEnded = false;

    // Function to add a message to the chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }

    // Function to add typing indicator
    function addTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message bot';
        indicator.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return indicator;
    }

    // Function to end conversation
    function endConversation() {
        isConversationEnded = true;
        userInput.disabled = true;
        userInput.placeholder = 'Conversation ended. Refresh to start a new chat.';
        chatForm.querySelector('button').disabled = true;
    }

    // Function to handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        
        if (isConversationEnded) return;
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';
        
        // Add typing indicator
        const typingIndicator = addTypingIndicator();
        
        try {
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            typingIndicator.remove();
            
            // Add bot response
            addMessage(data.response);
            
            // Check if conversation should end
            if (data.terminate) {
                endConversation();
            }
            
        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            addMessage('Sorry, I encountered an error. Please try again.');
        }
    }

    // Event listeners
    chatForm.addEventListener('submit', handleSubmit);
    
    // Handle Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    });

    // Focus input on load
    userInput.focus();
}); 