function sendMessage() {
    var inputField = document.getElementById('user-input');
    var userMessage = inputField.value.trim();

    if (userMessage === "") return;
    appendMessage("user", userMessage);
    inputField.value = "";  

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => {
        if (!response.ok) throw new Error("Server error");
        return response.json();
    })
    .then(data => {
        appendMessage("bot", data.response);
    })
    .catch(error => {
        console.error("Error:", error);
        appendMessage("bot", "Error: Unable to process your request.");
    });
}

function appendMessage(sender, message) {
    var chatbox = document.getElementById('chatbox');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = sender === "user" ? "You: " + message : "Bot: " + message;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
    
    // Save to local storage
    const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
    history.push({ sender, message });
    localStorage.setItem('chatHistory', JSON.stringify(history));
}

function clearChat() {
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML = '';
    localStorage.removeItem('chatHistory');
}

function loadChatHistory() {
    const history = localStorage.getItem('chatHistory');
    if (history) {
        const messages = JSON.parse(history);
        messages.forEach(msg => {
            appendMessage(msg.sender, msg.message);
        });
    }
}

// Add this line at the end of your file
document.addEventListener('DOMContentLoaded', loadChatHistory);

