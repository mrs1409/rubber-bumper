"""
Main entry point for the Rubber Bumper chatbot application.
This file imports the Flask app from app.py and serves as the entry point for Gunicorn.
"""

from app import app

if __name__ == "__main__":
    # Use debug=False for production deployment
    app.run(host="0.0.0.0", port=5000, debug=False)
