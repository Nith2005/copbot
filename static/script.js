document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const themeToggle = document.querySelector('.theme-toggle');
    const quickReplyButtons = document.querySelectorAll('.quick-reply-btn');
    const voiceInputBtn = document.querySelector('.voice-input-btn');
    const emojiBtn = document.querySelector('.emoji-btn');
    let isConversationEnded = false;
    let isRecording = false;

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = (event) => {
            const speechResult = event.results[0][0].transcript;
            userInput.value = speechResult;
            stopRecording();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopRecording();
        };

        recognition.onend = () => {
            stopRecording();
        };
    } else {
        voiceInputBtn.style.display = 'none';
        console.log('Speech recognition not supported');
    }

    // Voice Input Handling
    function startRecording() {
        if (recognition) {
            recognition.start();
            voiceInputBtn.innerHTML = '<i class="fas fa-stop"></i>';
            voiceInputBtn.classList.add('recording');
            isRecording = true;
        }
    }

    function stopRecording() {
        if (recognition) {
            recognition.stop();
            voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            voiceInputBtn.classList.remove('recording');
            isRecording = false;
        }
    }

    voiceInputBtn.addEventListener('click', () => {
        if (!isConversationEnded) {
            if (!isRecording) {
                startRecording();
            } else {
                stopRecording();
            }
        }
    });

    // Emoji Picker Setup
    let emojiPicker = null;
    let pickerVisible = false;

    function showEmojiPicker() {
        if (!emojiPicker) {
            const pickerContainer = document.createElement('div');
            pickerContainer.className = 'emoji-picker-container';
            document.body.appendChild(pickerContainer);

            const picker = new EmojiMart.Picker({
                onEmojiSelect: (emoji) => {
                    userInput.value += emoji.native;
                    hideEmojiPicker();
                    userInput.focus();
                },
                theme: document.body.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'
            });

            pickerContainer.appendChild(picker);
            emojiPicker = pickerContainer;

            // Position the picker
            const btnRect = emojiBtn.getBoundingClientRect();
            emojiPicker.style.position = 'fixed';
            emojiPicker.style.bottom = `${window.innerHeight - btnRect.top + 10}px`;
            emojiPicker.style.left = `${btnRect.left}px`;
            emojiPicker.style.zIndex = '1000';
        }
        emojiPicker.style.display = 'block';
        pickerVisible = true;

        // Close picker when clicking outside
        document.addEventListener('click', handleOutsideClick);
    }

    function hideEmojiPicker() {
        if (emojiPicker) {
            emojiPicker.style.display = 'none';
            pickerVisible = false;
            document.removeEventListener('click', handleOutsideClick);
        }
    }

    function handleOutsideClick(e) {
        if (pickerVisible && !emojiPicker.contains(e.target) && e.target !== emojiBtn) {
            hideEmojiPicker();
        }
    }

    emojiBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!isConversationEnded) {
            if (pickerVisible) {
                hideEmojiPicker();
            } else {
                showEmojiPicker();
            }
        }
    });

    // Theme handling
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Update emoji picker theme if it exists
        if (emojiPicker) {
            hideEmojiPicker();
            emojiPicker.remove();
            emojiPicker = null;
        }
    });

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }

    // Quick reply handling
    quickReplyButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!isConversationEnded) {
                const message = button.textContent;
                addMessage(message, true);
                userInput.value = message;
                handleSubmit(new Event('submit'));
            }
        });
    });

    // Function to add a message to the chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (!isUser) {
            const botAvatar = document.createElement('div');
            botAvatar.className = 'bot-avatar';
            botAvatar.innerHTML = `
                <img src="/static/images/tn_police_logo.png" alt="TN Police">
            `;
            messageContent.appendChild(botAvatar);
        }
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = content;
        
        messageContent.appendChild(messageText);
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
            <div class="message-content">
                <div class="bot-avatar">
                    <img src="/static/images/tn_police_logo.png" alt="TN Police">
                </div>
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
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
        voiceInputBtn.disabled = true;
        emojiBtn.disabled = true;
        document.querySelector('.send-btn').disabled = true;
        quickReplyButtons.forEach(btn => btn.disabled = true);
        hideEmojiPicker();
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