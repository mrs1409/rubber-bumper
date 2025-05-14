document.addEventListener('DOMContentLoaded', function() {
    console.log('Chat interface loaded');

    // Note: Page transitions and navigation are now handled by page-transitions.js

    // DOM Elements
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const clearButton = document.getElementById('clear-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const chatContainer = document.querySelector('.chat-container');

    console.log('messageInput:', messageInput);
    console.log('sendButton:', sendButton);

    // Chat history
    let chatHistory = [];

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
        "How many employees work at Rubber Bumper?",
        "What is the rubber band factory's profit?",
        "What is the condom factory's profit?",
        "What is the overhead for each factory?",
        "How has market share changed since 2011?",
        "Which factory has better margins?",
        "Why are profits decreasing?",
        "What's the expected ROI for conversion?",
        "What are the competitive advantages?",
        "What are the disadvantages of conversion?",
        "How long would conversion take?",
        "Would the company lose customers during conversion?",
        "What are the long-term benefits of conversion?",
        "Should they keep both product lines?",
        "What's the biggest challenge for Rubber Bumper?",
        "How would conversion affect employees?"
    ];

    // Track which questions have been asked
    let askedQuestions = new Set();

    // Function to update the suggested questions
    function updateSuggestedQuestions() {
        console.log('Updating suggested questions');

        // Get the question list container
        const questionList = document.getElementById('question-list');
        if (!questionList) {
            console.log('Question list container not found');

            // Try to find the container by class instead
            const suggestedQuestionsSection = document.querySelector('.suggested-questions-section');
            if (suggestedQuestionsSection) {
                console.log('Found suggested questions section, creating question list');

                // Find or create the suggested questions container
                let suggestedQuestions = suggestedQuestionsSection.querySelector('.suggested-questions');
                if (!suggestedQuestions) {
                    console.log('Creating suggested questions container');
                    suggestedQuestions = document.createElement('div');
                    suggestedQuestions.className = 'suggested-questions';
                    suggestedQuestionsSection.appendChild(suggestedQuestions);
                }

                // Create the question list
                const newQuestionList = document.createElement('div');
                newQuestionList.id = 'question-list';
                newQuestionList.className = 'question-list';
                suggestedQuestions.appendChild(newQuestionList);

                // Call this function again after a short delay
                setTimeout(updateSuggestedQuestions, 100);
                return;
            }

            return;
        }

        // Get questions that haven't been asked yet
        const availableQuestions = allSuggestedQuestions.filter(q => !askedQuestions.has(q));
        console.log('Available questions:', availableQuestions.length);

        // If almost all questions have been asked, reset
        if (availableQuestions.length < 5) {
            console.log('Resetting asked questions');
            askedQuestions.clear();
        }

        // Clear the current questions
        questionList.innerHTML = '';

        // Add 6 questions (or all available if less than 6)
        const questionsToShow = availableQuestions.slice(0, 6);
        console.log('Showing questions:', questionsToShow.length);

        questionsToShow.forEach(question => {
            const questionItem = document.createElement('div');
            questionItem.className = 'question-item';
            questionItem.textContent = question;
            questionItem.addEventListener('click', function() {
                console.log('Question clicked:', this.textContent);
                messageInput.value = this.textContent;

                // Mark this question as asked
                askedQuestions.add(this.textContent);

                // Send the message
                sendMessage();

                // Update suggested questions with a slight delay
                setTimeout(updateSuggestedQuestions, 300);
            });
            questionList.appendChild(questionItem);
        });
    }

    // Initialize suggested questions
    updateSuggestedQuestions();

    // Only clean the chat input container, not the sidebar
    function cleanChatInputContainer() {
        const chatInputContainer = document.querySelector('.chat-input-container');
        if (chatInputContainer) {
            Array.from(chatInputContainer.children).forEach(child => {
                if (!child.classList.contains('input-group')) {
                    chatInputContainer.removeChild(child);
                }
            });
        }
    }

    // Call immediately and set an interval to keep cleaning
    cleanChatInputContainer();
    setInterval(cleanChatInputContainer, 500);

    // Debug: Log if the question list exists
    const questionList = document.getElementById('question-list');
    console.log('Question list exists:', questionList !== null);
    console.log('Question list parent:', questionList ? questionList.parentElement : 'Not found');
    console.log('Suggested questions section exists:', document.querySelector('.suggested-questions-section') !== null);

    // Force create the suggested questions section if it doesn't exist
    if (!document.querySelector('.suggested-questions-section')) {
        console.log('Creating suggested questions section from scratch');

        // Find the sidebar content
        const sidebarContent = document.querySelector('.sidebar-content');
        if (sidebarContent) {
            // Create the section
            const suggestedQuestionsSection = document.createElement('div');
            suggestedQuestionsSection.className = 'mb-4 suggested-questions-section';

            // Create the heading
            const heading = document.createElement('h5');
            heading.textContent = 'Suggested Questions';
            suggestedQuestionsSection.appendChild(heading);

            // Create the container
            const suggestedQuestions = document.createElement('div');
            suggestedQuestions.className = 'suggested-questions';
            suggestedQuestionsSection.appendChild(suggestedQuestions);

            // Create the question list
            const newQuestionList = document.createElement('div');
            newQuestionList.id = 'question-list';
            newQuestionList.className = 'question-list';
            suggestedQuestions.appendChild(newQuestionList);

            // Insert before the about section
            const aboutSection = sidebarContent.querySelector('.about-section');
            if (aboutSection) {
                sidebarContent.insertBefore(suggestedQuestionsSection, aboutSection);
            } else {
                sidebarContent.appendChild(suggestedQuestionsSection);
            }

            // Make sure the section is visible
            suggestedQuestionsSection.style.display = 'block';
            suggestedQuestions.style.display = 'block';
            newQuestionList.style.display = 'block';
        }
    }

    // Force update the suggested questions after a short delay
    setTimeout(updateSuggestedQuestions, 1000);

    // Also set an interval to keep updating the suggested questions
    setInterval(function() {
        // Check if the question list exists and has children
        const questionList = document.getElementById('question-list');
        if (!questionList || questionList.children.length === 0) {
            console.log('Question list is empty or not found, updating...');
            updateSuggestedQuestions();
        }
    }, 2000);

    // Sidebar toggle functionality
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar-collapsed');
        chatContainer.classList.toggle('chat-container-expanded');

        // Force layout recalculation
        document.body.offsetHeight;

        // Change icon based on sidebar state
        const icon = this.querySelector('i');
        if (sidebar.classList.contains('sidebar-collapsed')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-chevron-right');
        } else {
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-bars');
        }

        // Trigger window resize event to force layout recalculation
        window.dispatchEvent(new Event('resize'));
    });

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
        console.log('Key pressed:', e.key);
        if (e.key === 'Enter' && !e.shiftKey) {
            console.log('Enter key pressed without shift');
            e.preventDefault();
            sendMessage();
        }
    });

    // Send message on button click
    sendButton.addEventListener('click', function() {
        console.log('Send button clicked');
        sendMessage();
    });

    // Clear button
    clearButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear your chat history?')) {
            clearAllData();
        }
    });

    // Function to send a message
    function sendMessage() {
        console.log('sendMessage function called');
        const message = messageInput.value.trim();
        console.log('Message:', message);
        if (!message) {
            console.log('Message is empty, returning');
            return;
        }

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

        // Add animation class
        messageRow.classList.add('fade-in');

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

        // Animate the message bubble after a small delay
        setTimeout(() => {
            const messageBubble = messageRow.querySelector('.message-bubble');
            if (messageBubble) {
                messageBubble.classList.add(role === 'user' ? 'slide-in-right' : 'slide-in-left');
            }
        }, 50);

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
        typingIndicator.className = 'message-row bot-message fade-in';

        typingIndicator.innerHTML = `
            <div class="avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble typing-indicator-bubble">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;

        chatMessages.appendChild(typingIndicator);

        // Add animation class after a small delay
        setTimeout(() => {
            const indicatorBubble = typingIndicator.querySelector('.typing-indicator-bubble');
            if (indicatorBubble) {
                indicatorBubble.classList.add('slide-in-left');
            }
        }, 50);

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
        // Start request time
        const requestStartTime = new Date();

        fetch('/chat-api', {
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

            // Calculate response time
            const responseTime = (new Date() - requestStartTime) / 1000;
            console.log(`Response received in ${responseTime.toFixed(2)}s`);

            // Add bot response to chat
            if (data.error) {
                // If there's an error but also a fallback response, use that
                if (data.fallback_response) {
                    addMessageToChat('bot', data.fallback_response);
                } else {
                    addMessageToChat('bot', `Error: ${data.error}`);
                }
            } else {
                addMessageToChat('bot', data.response);

                // If processing time is available, log it
                if (data.processing_time) {
                    console.log(`Server processing time: ${data.processing_time}s`);
                }
            }
        })
        .catch(error => {
            // Remove typing indicator
            removeTypingIndicator();

            // Add error message
            addMessageToChat('bot', 'Sorry, I encountered an error processing your request. Please try asking about Rubber Bumper\'s products, market position, or factory conversion options.');
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

            // Update suggested questions
            updateSuggestedQuestions();

            // Add system message with cache info if available
            let message = 'Chat history has been cleared. You can start a new conversation.';
            if (data.cache_size !== undefined) {
                message += ` (Cache size: ${data.cache_size})`;
            }
            addMessageToChat('bot', message);

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
