document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const documentList = document.getElementById('document-list');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Event listeners for drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('dragover');
    }
    
    function unhighlight() {
        dropArea.classList.remove('dragover');
    }
    
    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
    
    // Handle file input change
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });
    
    // Upload button click
    uploadBtn.addEventListener('click', function() {
        fileInput.click();
    });
    
    // Handle files
    function handleFiles(files) {
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    }
    
    // Upload file to server
    function uploadFile(file) {
        // Check if it's a PDF
        if (file.type !== 'application/pdf') {
            alert('Please upload a PDF file');
            return;
        }
        
        // Show loading overlay
        loadingOverlay.classList.remove('d-none');
        
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading overlay
            loadingOverlay.classList.add('d-none');
            
            // Add document to list
            addDocumentToList(data.filename);
            
            // Add chat message
            const messageElement = document.getElementById('chat-messages');
            
            // Create message element
            const messageRow = document.createElement('div');
            messageRow.className = 'message-row bot-message';
            
            const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            messageRow.innerHTML = `
                <div class="avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p>I've processed "${data.filename}" with ${data.chunks} text chunks. You can now ask me questions about the content!</p>
                    </div>
                    <div class="message-info">
                        <span class="message-time">${timestamp}</span>
                    </div>
                </div>
            `;
            
            messageElement.appendChild(messageRow);
            
            // Scroll to bottom
            messageElement.scrollTop = messageElement.scrollHeight;
        })
        .catch(error => {
            // Hide loading overlay
            loadingOverlay.classList.add('d-none');
            
            // Show error
            alert('Failed to upload file: ' + error.message);
            console.error('Error:', error);
        });
    }
    
    // Add document to the list
    function addDocumentToList(filename) {
        // Remove empty state if present
        const emptyState = documentList.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        // Create document item
        const documentItem = document.createElement('div');
        documentItem.className = 'document-item';
        
        documentItem.innerHTML = `
            <div class="document-icon">
                <i class="fas fa-file-pdf"></i>
            </div>
            <div class="document-name" title="${filename}">
                ${filename}
            </div>
        `;
        
        // Add to list
        documentList.appendChild(documentItem);
    }
});
