import os
import logging
from flask import Flask, render_template, request, jsonify, session
from werkzeug.middleware.proxy_fix import ProxyFix
from utils.pdf_processor import process_pdf
from utils.vector_store import VectorStore
from utils.chat import get_chat_response

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "rubber_bumper_default_key")

# Set up Hugging Face API key in environment variables
os.environ["HUGGINGFACE_API_KEY"] = os.environ.get("HUGGINGFACE_API_KEY", "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")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize vector store
vector_store = VectorStore()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if it's a PDF file
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Process the PDF file
        text_chunks = process_pdf(file)
        
        # Add to vector store
        vector_store.add_documents(text_chunks)
        
        # Save document information to session
        if 'documents' not in session:
            session['documents'] = []
        
        doc_info = {
            'filename': file.filename,
            'chunk_count': len(text_chunks)
        }
        session['documents'].append(doc_info)
        
        return jsonify({
            "message": "PDF processed successfully", 
            "filename": file.filename,
            "chunks": len(text_chunks)
        })
    
    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get chat response
        response = get_chat_response(user_message, vector_store)
        
        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": f"Error generating response: {str(e)}"}), 500

# Route to clear the vector store
@app.route('/clear', methods=['POST'])
def clear_data():
    try:
        vector_store.clear()
        if 'documents' in session:
            session.pop('documents')
        return jsonify({"message": "Document data cleared successfully"})
    except Exception as e:
        logging.error(f"Error clearing data: {str(e)}")
        return jsonify({"error": f"Error clearing data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
