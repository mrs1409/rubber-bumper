document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const clearButton = document.getElementById('clear-btn');
    const quickReplyButtons = document.querySelectorAll('.quick-reply-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Chat history
    let chatHistory = [];
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        
        // Limit to 5 rows
        const lineHeight = parseInt(getComputedStyle(this).lineHeight);
        const maxHeight = lineHeight * 5;
        if (this.scrollHeight > maxHeight) {
            this.style.height = maxHeight + 'px';
            this.style.overflowY = 'auto';
        } else {
            this.style.overflowY = 'hidden';
        }
    });
    
    // Send message on enter key (without shift)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Quick reply buttons
    quickReplyButtons.forEach(button => {
        button.addEventListener('click', function() {
            messageInput.value = this.textContent;
            sendMessage();
        });
    });
    
    // Clear button
    clearButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear all uploaded documents and chat history?')) {
            clearAllData();
        }
    });
    
    // Function to send a message
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input
        messageInput.value = '';
        messageInput.style.height = 'auto';
        
        // Scroll to bottom
        scrollToBottom();
        
        // Add typing indicator
        addTypingIndicator();
        
        // Send to backend
        fetchChatResponse(message);
    }
    
    // Function to add a message to the chat
    function addMessageToChat(role, content) {
        const messageRow = document.createElement('div');
        messageRow.className = `message-row ${role}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        let avatarIcon = 'robot';
        if (role === 'user') {
            avatarIcon = 'user';
        }
        
        messageRow.innerHTML = `
            <div class="avatar">
                <i class="fas fa-${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <p>${formatMessage(content)}</p>
                </div>
                <div class="message-info">
                    <span class="message-time">${timestamp}</span>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageRow);
        
        // Add to history
        chatHistory.push({ role, content, timestamp });
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Function to format message content (with markdown-like features)
    function formatMessage(content) {
        // Convert line breaks to <br>
        content = content.replace(/\n/g, '<br>');
        
        // Bold text between **
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text between *
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Code blocks
        content = content.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');
        
        // Inline code
        content = content.replace(/`(.*?)`/g, '<code>$1</code>');
        
        return content;
    }
    
    // Function to add typing indicator
    function addTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.id = 'typing-indicator';
        typingIndicator.className = 'message-row bot-message';
        
        typingIndicator.innerHTML = `
            <div class="avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingIndicator);
        scrollToBottom();
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to fetch chat response from backend
    function fetchChatResponse(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add bot response to chat
            if (data.error) {
                addMessageToChat('bot', `Error: ${data.error}`);
            } else {
                addMessageToChat('bot', data.response);
            }
        })
        .catch(error => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add error message
            addMessageToChat('bot', 'Sorry, I encountered an error processing your request. Please try again later.');
            console.error('Error:', error);
        });
    }
    
    // Function to clear all data
    function clearAllData() {
        // Show loading overlay
        loadingOverlay.classList.remove('d-none');
        
        fetch('/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Clear chat messages except the first welcome message
            while (chatMessages.children.length > 1) {
                chatMessages.removeChild(chatMessages.lastChild);
            }
            
            // Clear chat history
            chatHistory = [];
            
            // Clear document list
            const documentList = document.getElementById('document-list');
            documentList.innerHTML = '<p class="text-muted text-center small empty-state">No documents uploaded yet</p>';
            
            // Add system message
            addMessageToChat('bot', 'All data has been cleared. You can upload new documents to continue.');
            
            // Hide loading overlay
            loadingOverlay.classList.add('d-none');
        })
        .catch(error => {
            // Hide loading overlay
            loadingOverlay.classList.add('d-none');
            
            // Show error
            alert('Failed to clear data: ' + error.message);
            console.error('Error:', error);
        });
    }
    
    // Function to scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
