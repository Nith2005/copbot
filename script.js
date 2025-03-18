function sendMessage() {
    var inputField = document.getElementById('user-input');
    var userMessage = inputField.value;
    if (userMessage.trim() === "") return;
    appendMessage("user", userMessage);
    inputField.value = "";
    
    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("bot", data.response);
    })
    .catch(error => {
        appendMessage("bot", "Error: Unable to process your request.");
        console.error("Error:", error);
    });
}

function appendMessage(sender, message) {
    var chatbox = document.getElementById('chatbox');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = sender === "user" ? "You: " + message : "Bot: " + message;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}
