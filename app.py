import os
import logging
import time
from flask import Flask, render_template, request, jsonify, session
from werkzeug.middleware.proxy_fix import ProxyFix
from utils.vector_store import VectorStore
from utils.chat import get_chat_response, response_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "rubber_bumper_default_key")

# Set up Groq API key in environment variables
groq_api_key = os.environ.get("GROQ_API_KEY", "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")
os.environ["GROQ_API_KEY"] = groq_api_key
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize vector store with pre-loaded Rubber Bumper data
vector_store = VectorStore()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({
        "status": "ok",
        "timestamp": time.time(),
        "cache_size": len(response_cache)
    })

@app.route('/chat-api', methods=['POST'])
def chat_api():
    """Process chat requests and return responses."""
    start_time = time.time()

    try:
        # Parse request data
        data = request.json
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Log the incoming request
        logger.info(f"Chat request received: {user_message[:50]}{'...' if len(user_message) > 50 else ''}")

        # Get chat response
        response = get_chat_response(user_message, vector_store)

        # Calculate processing time
        processing_time = time.time() - start_time
        logger.info(f"Request processed in {processing_time:.2f}s")

        return jsonify({
            "response": response,
            "processing_time": round(processing_time, 2)
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "error": f"Error generating response: {str(e)}",
            "fallback_response": "I'm having trouble processing your request right now. Please try asking about Rubber Bumper's products, market position, or factory conversion options."
        }), 500

# Route to reset the chat data
@app.route('/clear', methods=['POST'])
def clear_data():
    """Clear chat history and reset the vector store."""
    try:
        # Reload the base Rubber Bumper data
        vector_store.clear()

        # Clear session data
        if 'chat_history' in session:
            session.pop('chat_history')

        # Clear response cache
        response_cache.clear()

        logger.info("Chat history and cache cleared successfully")
        return jsonify({
            "message": "Chat history cleared successfully",
            "cache_size": len(response_cache)
        })
    except Exception as e:
        logger.error(f"Error clearing data: {str(e)}", exc_info=True)
        return jsonify({"error": f"Error clearing data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
