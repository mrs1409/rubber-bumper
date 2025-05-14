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
    
    // Add static suggested questions instead of dynamic ones to fix the issue
    const suggestedQuestionsContainer = document.querySelector('.suggested-questions');
    const questionList = document.createElement('div');
    questionList.className = 'question-list';
    questionList.id = 'question-list';
    
    // All available suggested questions (more than what we'll display at once)
    const allSuggestedQuestions = [
        "What is the company name?",
        "What products does Rubber Bumper sell?",
        "What is Rubber Bumper's market position?",
        "How have the rubber band sales changed over time?",
        "How has the condom market grown?",
        "Which product is more profitable?", 
        "What are the profit margins for each product?",
        "Should they convert the rubber band factory?",
        "What are the risks of factory conversion?",
        "Who are the main competitors?",
        "What is the payback period for conversion?",
        "How much would the conversion cost?",
        "What is the current financial status?",
        "What does the president think about conversion?",
        "How many employees work at Rubber Bumper?"
    ];
    
    // Track which questions have been asked
    let askedQuestions = new Set();
    
    // Function to update the suggested questions
    function updateSuggestedQuestions() {
        // Get questions that haven't been asked yet
        const availableQuestions = allSuggestedQuestions.filter(q => !askedQuestions.has(q));
        
        // If almost all questions have been asked, reset
        if (availableQuestions.length < 5) {
            askedQuestions.clear();
        }
        
        // Clear the current questions
        const existingQuestionList = document.getElementById('question-list');
        if (existingQuestionList) {
            existingQuestionList.innerHTML = '';
            
            // Add 10 questions (or all available if less than 10)
            const questionsToShow = availableQuestions.slice(0, 10);
            
            questionsToShow.forEach(question => {
                const questionItem = document.createElement('div');
                questionItem.className = 'question-item p-2 mb-2 suggested-question';
                questionItem.textContent = question;
                questionItem.addEventListener('click', function() {
                    messageInput.value = this.textContent;
                    
                    // Mark this question as asked
                    askedQuestions.add(this.textContent);
                    
                    // Send the message
                    sendMessage();
                    
                    // Update suggested questions with a slight delay
                    setTimeout(updateSuggestedQuestions, 300);
                });
                existingQuestionList.appendChild(questionItem);
            });
        }
    }
    
    // Update the quick reply buttons behavior
    quickReplyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const question = this.textContent;
            messageInput.value = question;
            
            // Remove this button after it's clicked
            this.style.display = 'none';
            
            // Send the message
            sendMessage();
        });
    });
    
    // Initialize suggested questions
    updateSuggestedQuestions();
    
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
    
    // Suggested questions
    suggestedQuestions.forEach(question => {
        question.addEventListener('click', function() {
            messageInput.value = this.textContent.trim();
            sendMessage();
        });
    });
    
    // Clear button
    clearButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear your chat history?')) {
            clearAllData();
        }
    });
    
    // Function to send a message
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Check if the message matches any suggested question
        allSuggestedQuestions.forEach(question => {
            if (message.toLowerCase() === question.toLowerCase()) {
                askedQuestions.add(question);
            }
        });
        
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
        
        // Update suggested questions
        updateSuggestedQuestions();
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
            
            // Reset asked questions
            askedQuestions.clear();
            updateSuggestedQuestions();
            
            // Add system message
            addMessageToChat('bot', 'Chat history has been cleared. You can start a new conversation.');
            
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
