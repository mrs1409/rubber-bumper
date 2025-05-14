import os
import logging
from flask import Flask, render_template, request, jsonify, session
from werkzeug.middleware.proxy_fix import ProxyFix
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

# Initialize vector store with pre-loaded Rubber Bumper data
vector_store = VectorStore()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get chat response
        response = get_chat_response(user_message, vector_store)
        
        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": f"Error generating response: {str(e)}"}), 500

# Route to reset the chat data
@app.route('/clear', methods=['POST'])
def clear_data():
    try:
        # Reload the base Rubber Bumper data
        vector_store.clear()
        if 'chat_history' in session:
            session.pop('chat_history')
        return jsonify({"message": "Chat history cleared successfully"})
    except Exception as e:
        logging.error(f"Error clearing data: {str(e)}")
        return jsonify({"error": f"Error clearing data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
