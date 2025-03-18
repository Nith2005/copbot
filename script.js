function sendMessage() {
    var inputField = document.getElementById('user-input');
    var userMessage = inputField.value.trim();

    if (userMessage === "") return;  // Prevent empty messages
    appendMessage("user", userMessage);
    inputField.value = "";  

    fetch('http://127.0.0.1:5000/chat', {  // Correct API URL
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
}
