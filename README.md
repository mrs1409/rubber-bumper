# Rubber Bumper Chatbot

A specialized chatbot for the Rubber Bumper case study that provides information about the company's products, market position, financial data, and strategic options.

## Features

- Interactive chat interface with suggested questions
- Vector store for context-aware responses
- Integration with Groq API for advanced language model capabilities
- Response caching for consistent answers
- Dark mode support
- Mobile-responsive design

## Recent Improvements

### Better Keyword Matching

The chatbot now uses a score-based approach for matching user queries to predefined answers:

- Calculates word overlap between user query and known questions
- Considers context and key terms in the query
- Assigns higher scores to more relevant matches
- Uses a threshold to ensure only high-quality matches are returned

This is a significant improvement over the previous simple substring matching, which often led to incorrect responses when a user query contained multiple keywords.

### Duplicate Response Prevention

A response cache has been implemented to:

- Store previous responses to identical questions
- Ensure consistent answers for repeated questions
- Prevent duplicate responses to the same query
- Improve response time for frequently asked questions

The cache is cleared when the user explicitly resets the chat history.

### Vector Store Integration

The chatbot now leverages the vector store more effectively:

- Searches for relevant documents based on user queries
- Extracts context from the most similar documents
- Enhances the system prompt with relevant context
- Provides more accurate and detailed responses

This integration allows the chatbot to provide more nuanced answers by considering the full context of the case study.

### Enhanced Error Handling

The application now has robust error handling:

- Provides fallback responses when errors occur
- Logs detailed error information for debugging
- Gracefully handles API failures with alternative responses
- Ensures users always receive a helpful answer

This prevents the chatbot from breaking or providing unhelpful error messages to users.

### Performance Monitoring

Added timing metrics to track and optimize performance:

- Measures total request processing time
- Logs API response times
- Tracks cache hit rates
- Provides performance data in the health check endpoint

These metrics help identify potential bottlenecks and optimize the chatbot's performance.

## Technical Implementation

### Backend (Flask)

- `app.py`: Main Flask application with API endpoints
- `utils/chat.py`: Core chat logic and response generation
- `utils/vector_store.py`: TF-IDF vector store implementation

### Frontend

- HTML/CSS/JavaScript with Bootstrap 5
- Interactive chat interface
- Markdown-like formatting for responses
- Suggested questions and quick replies

## API Endpoints

- `GET /`: Main chat interface
- `POST /chat`: Process chat messages and return responses
- `POST /clear`: Clear chat history and reset the vector store
- `GET /health`: Health check endpoint with system status

## Running the Application

The application should be run using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## Dependencies

- Flask: Web framework
- Groq: API client for LLM integration
- scikit-learn: For TF-IDF vectorization
- NLTK: For text processing
- Bootstrap 5: Frontend framework
