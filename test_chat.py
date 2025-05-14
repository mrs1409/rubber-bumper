"""
Test script for the Rubber Bumper chatbot.
This script tests the chat functionality to ensure the improvements are working correctly.
"""

import unittest
from utils.vector_store import VectorStore
from utils.chat import get_direct_response, get_groq_response, get_chat_response, response_cache

class TestChatFunctionality(unittest.TestCase):
    """Test cases for the chat functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.vector_store = VectorStore()
        # Clear the response cache before each test
        response_cache.clear()
    
    def test_direct_response(self):
        """Test the direct response functionality."""
        # Test exact match
        response = get_direct_response("what products")
        self.assertEqual(response, "Rubber Bumper Co sells two products: rubber bands and condoms.")
        
        # Test partial match with score-based matching
        response = get_direct_response("tell me about the products they sell")
        self.assertIsNotNone(response)
        self.assertTrue("rubber bands and condoms" in response.lower())
        
        # Test no match
        response = get_direct_response("something completely unrelated")
        self.assertIsNone(response)
    
    def test_response_cache(self):
        """Test the response caching functionality."""
        # First request should not be cached
        self.assertNotIn("what is the company name", response_cache)
        
        # Make a request
        response1 = get_direct_response("what is the company name")
        self.assertEqual(response1, "Rubber Bumper Co.")
        
        # Check that the response is now cached
        self.assertIn("what is the company name", response_cache)
        
        # Make the same request again
        response2 = get_direct_response("what is the company name")
        self.assertEqual(response2, "Rubber Bumper Co.")
        
        # The responses should be identical
        self.assertEqual(response1, response2)
    
    def test_chat_response(self):
        """Test the chat response functionality."""
        # Test with a direct response
        response = get_chat_response("what products", self.vector_store)
        self.assertEqual(response, "Rubber Bumper Co sells two products: rubber bands and condoms.")
        
        # Test with a more complex query that should use the vector store
        response = get_chat_response("How has the market for their products changed over time?", self.vector_store)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

if __name__ == "__main__":
    unittest.main()
