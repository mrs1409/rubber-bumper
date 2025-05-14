# Changelog

All notable changes to the Rubber Bumper Chatbot will be documented in this file.

## [1.1.0] - 2023-07-15

### Added
- Response caching system to prevent duplicate responses
- Score-based keyword matching algorithm for better query understanding
- Vector store integration for context-aware responses
- Health check endpoint with system status information
- Performance monitoring with timing metrics
- Thread-local storage for context management
- Enhanced error handling with fallback responses
- Improved logging for better debugging

### Changed
- Updated keyword matching to use word overlap scoring instead of simple substring matching
- Enhanced Groq API integration with context-aware prompts
- Improved frontend error handling with user-friendly messages
- Updated clear functionality to reset response cache
- Modified chat response format to include processing time

### Fixed
- Fixed issue with duplicate responses to similar questions
- Resolved incorrect responses when queries contained multiple keywords
- Fixed partial matching problems with short keywords
- Improved error handling to prevent crashes on API failures

## [1.0.0] - 2023-06-30

### Added
- Initial release of the Rubber Bumper Chatbot
- Basic chat interface with suggested questions
- Integration with Groq API for LLM responses
- Simple TF-IDF vector store for document search
- Dark mode support
- Mobile-responsive design
