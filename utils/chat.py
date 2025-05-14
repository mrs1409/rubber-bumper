import os
import json
import re
import requests

# Set up Hugging Face API key
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "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")

def get_direct_response(user_message):
    """
    Generate a direct response based on predefined questions about Rubber Bumper.
    
    Args:
        user_message: A string containing the user's message.
        
    Returns:
        A string containing the response if a matching question is found, otherwise None.
    """
    # Convert message to lowercase for case-insensitive matching
    message_lower = user_message.lower()
    
    # Dictionary of predefined questions and answers
    qa_dict = {
        "what products": "Rubber Bumper Co sells two main products: rubber bands and condoms. They pride themselves on producing a limited range of high-quality products.",
        
        "market position": "Rubber Bumper is the market leader in both of their product industries (rubber bands and condoms).",
        
        "topline sales": "Topline sales have remained relatively stable over the last 3 years, despite decreasing profits.",
        
        "rubber band market": "The rubber band market has been relatively flat, with total industry volume around 30-32 million pounds annually. However, Rubber Bumper's share has decreased from 4 million pounds in 2011 to 2 million pounds in 2017, while the dominant player (Max Rubber) has increased from 17 to 24 million pounds.",
        
        "condom market": "The condom market has shown strong growth, increasing from 350 million units in 2011 to 450 million in 2017 (approximately 30% growth). Rubber Bumper's condom sales grew from 1 million in 2011 to 10 million in 2017, but have plateaued since 2014.",
        
        "profit margin": "The condom factory has a higher profit margin than the rubber band factory. In 2017, the condom factory had a profit of $4.5 million on $7.5 million in revenue (60% margin), while the rubber band factory had a profit of $4 million on $10 million in revenue (40% margin).",
        
        "factory conversion": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year, during which the company would lose $8 million in contribution. After conversion, the larger factory could produce twice as many condoms (20 million total), potentially generating $11 million in profit. However, the payback period would be approximately 5 years, which exceeds the company's 4-year target.",
        
        "risks": "Key risks of the factory conversion include: assuming Rubber Bumper can triple condom sales immediately, potential rebound in rubber band demand, political changes affecting condom market, less product diversification, increased advertising requirements for condoms, potential legal risks with contraception products, and employee resistance to making condoms."
    }
    
    # Check if any key phrases match the user message
    for key, answer in qa_dict.items():
        if key in message_lower:
            return answer
    
    # No direct match found
    return None

def get_chat_response(user_message, vector_store, max_context_length=4000):
    """
    Generate a response to a user message using context-based approach with fallback options.
    
    Args:
        user_message: A string containing the user's message.
        vector_store: A VectorStore object containing the document vectors.
        max_context_length: An integer representing the maximum context length.
        
    Returns:
        A string containing the generated response.
    """
    # First try to get a direct response to common questions
    direct_response = get_direct_response(user_message)
    if direct_response:
        return direct_response
    
    # Get relevant context from the vector store
    relevant_contexts = vector_store.search(user_message, top_k=3)
    
    # If no relevant context found
    if not relevant_contexts:
        return "I'm not sure about that specific question. Try asking about Rubber Bumper's products, market position, finances, or the factory conversion project."
    
    # Prepare context for analysis
    context_text = "\n\n".join([doc[0] for doc in relevant_contexts])
    
    # Truncate context if it's too long
    if len(context_text) > max_context_length:
        context_text = context_text[:max_context_length] + "..."
    
    try:
        # Try to use Hugging Face API if available
        API_URL = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        # Make API request
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": user_message, "parameters": {"max_length": 100, "temperature": 0.7}}
        )
        
        # If API call is successful, use its response
        if response.status_code == 200:
            try:
                response_data = response.json()
                if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
                    return response_data[0]["generated_text"].strip()
                elif isinstance(response_data, dict) and "generated_text" in response_data:
                    return response_data["generated_text"].strip()
            except:
                # If parsing fails, fall back to context-based response
                pass
    except:
        # API call failed, continue to fallback approach
        pass
    
    # Fallback: Return the most relevant context as the answer
    return f"Based on the Rubber Bumper case study, here's what I found:\n\n{relevant_contexts[0][0]}"
