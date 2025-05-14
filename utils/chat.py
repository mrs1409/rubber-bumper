import os
import json
import re
import requests

# Set up Hugging Face API key
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "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")

def get_chat_response(user_message, vector_store, max_context_length=4000):
    """
    Generate a response to a user message using the Hugging Face API.
    
    Args:
        user_message: A string containing the user's message.
        vector_store: A VectorStore object containing the document vectors.
        max_context_length: An integer representing the maximum context length.
        
    Returns:
        A string containing the generated response.
    """
    # Get relevant context from the vector store
    relevant_contexts = vector_store.search(user_message, top_k=3)
    
    # If no relevant context found
    if not relevant_contexts:
        return "I don't have enough information about that. Try uploading a relevant PDF first."
    
    # Prepare context for the prompt
    context_text = "\n\n".join([f"Document {i+1}:\n{doc[0]}" for i, doc in enumerate(relevant_contexts)])
    
    # Truncate context if it's too long
    if len(context_text) > max_context_length:
        context_text = context_text[:max_context_length] + "..."
    
    # Prepare system prompt
    system_prompt = """You are a helpful assistant for the Rubber Bumper case study. 
You have access to PDF documents with information about Rubber Bumper Co, a small family-owned producer of rubber products.
When answering questions, use only information from the provided context. 
If the answer is not in the context, acknowledge that you don't have that information.
Cite specific numbers and facts from the context when relevant.
Be concise but comprehensive in your answers."""
    
    # Combine system prompt and user message with context
    full_prompt = f"{system_prompt}\n\nBased on the following context, please answer this question: {user_message}\n\nContext:\n{context_text}"
    
    try:
        # Use Hugging Face API to generate response
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        # Make API request
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": full_prompt, "parameters": {"max_length": 800, "temperature": 0.5}}
        )
        
        # Extract and return the response text
        if response.status_code == 200:
            answer = response.json()[0]["generated_text"].strip()
            return answer
        else:
            return f"Error from Hugging Face API: {response.text}"
        
    except Exception as e:
        # If API fails, fall back to basic response
        return f"I'm having trouble generating a response. Error: {str(e)}"
