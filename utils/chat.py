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
    
    # Handle greetings and common phrases
    greetings = ["hello", "hi ", "hey", "greetings", "howdy", "good morning", "good afternoon", "good evening"]
    for greeting in greetings:
        if greeting in message_lower:
            return "Hello! I'm your Rubber Bumper case study assistant. How can I help you analyze the business situation today?"
    
    # Handle thank you messages
    thanks = ["thank you", "thanks", "appreciate", "grateful"]
    for thank in thanks:
        if thank in message_lower:
            return "You're welcome! Feel free to ask any other questions about the Rubber Bumper case study."
    
    # Handle questions about the chatbot
    bot_questions = ["who are you", "what are you", "what can you do", "how do you work", "what do you know"]
    for question in bot_questions:
        if question in message_lower:
            return "I'm a specialized assistant for the Rubber Bumper case study. I can answer questions about their products, market position, financial data, and strategic options like factory conversion. What would you like to know about Rubber Bumper Co?"
    
    # Dictionary of predefined questions and answers about Rubber Bumper
    qa_dict = {
        "what product": "Rubber Bumper Co sells two main products: rubber bands and condoms. They pride themselves on producing a limited range of high-quality products.",
        
        "what does rubber bumper": "Rubber Bumper Co is a small family-owned producer of rubber products. They sell two main products: rubber bands and condoms. They pride themselves on producing a limited range of high-quality products.",
        
        "tell me about rubber bumper": "Rubber Bumper Co is a small family-owned producer of rubber products. It prides itself on producing a limited range of products (rubber bands and condoms) but producing the highest quality on the market. The company has recently appointed a new President who noticed decreasing profits over the last couple of years.",
        
        "market position": "Rubber Bumper is the market leader in both of their product industries (rubber bands and condoms).",
        
        "topline sales": "Topline sales have remained relatively stable over the last 3 years, despite decreasing profits.",
        
        "decreas": "Rubber Bumper has experienced decreasing profits over the last couple of years, despite relatively stable topline sales. This suggests issues with cost management or product mix profitability.",
        
        "rubber band": "The rubber band market has been relatively flat, with total industry volume around 30-32 million pounds annually. However, Rubber Bumper's share has decreased from 4 million pounds in 2011 to 2 million pounds in 2017, while the dominant player (Max Rubber) has increased from 17 to 24 million pounds.",
        
        "condom": "The condom market has shown strong growth, increasing from 350 million units in 2011 to 450 million in 2017 (approximately 30% growth). Rubber Bumper's condom sales grew from 1 million in 2011 to 10 million in 2017, but have plateaued since 2014.",
        
        "profit margin": "The condom factory has a higher profit margin than the rubber band factory. In 2017, the condom factory had a profit of $4.5 million on $7.5 million in revenue (60% margin), while the rubber band factory had a profit of $4 million on $10 million in revenue (40% margin).",
        
        "profitab": "In terms of profitability, the condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin. The condom factory had a profit of $4.5 million on $7.5 million in revenue, while the rubber band factory had a profit of $4 million on $10 million in revenue.",
        
        "factory": "Rubber Bumper Co has two factories, each producing one of their two products. The rubber band factory is larger and has an annual overhead of $4 million, while the condom factory is smaller with an annual overhead of $2 million.",
        
        "convert": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year, during which the company would lose $8 million in contribution. After conversion, the larger factory could produce twice as many condoms (20 million total), potentially generating $11 million in profit. However, the payback period would be approximately 5 years, which exceeds the company's 4-year target.",
        
        "should they": "Converting the rubber band factory to produce condoms has potential long-term benefits but exceeds the company's 4-year payback target. The recommendation would be to first invest in market research to verify demand for increased condom production, while also exploring ways to reduce conversion costs or time to improve the project economics.",
        
        "recommendation": "Based on the analysis, converting the rubber band factory to produce condoms would increase profitability in the long run, but the payback period of approximately 5 years exceeds the company's target of 4 years. Additionally, there are significant risks in assuming the company can triple its condom sales immediately. The recommendation would be to first invest in market research to verify demand for increased condom production.",
        
        "risk": "Key risks of the factory conversion include: assuming Rubber Bumper can triple condom sales immediately, potential rebound in rubber band demand, political changes affecting condom market, less product diversification, increased advertising requirements for condoms, potential legal risks with contraception products, and employee resistance to making condoms.",
        
        "concern": "Several concerns with the factory conversion plan include: the 5-year payback period exceeds the company's 4-year target, the assumption that Rubber Bumper can triple condom sales immediately may be unrealistic, and the loss of product diversification increases market risk.",
        
        "competitor": "In the rubber band market, the main competitor is Max Rubber, which has been gaining market share (from 17 million pounds in 2011 to 24 million pounds in 2017). In the condom market, major competitors include Spartan (115 million units in 2017) and Durable (170 million units in 2017).",
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
    # Check if the message is empty or too short
    if not user_message or len(user_message.strip()) < 2:
        return "Please ask me a question about Rubber Bumper Co. I can help with information about their products, market position, financials, or strategic options."
    
    # First try to get a direct response to common questions
    direct_response = get_direct_response(user_message)
    if direct_response:
        return direct_response
    
    # Check if question is completely unrelated to Rubber Bumper
    rubber_bumper_terms = ["rubber", "bumper", "band", "condom", "factory", "profit", "market", "competitor", 
                           "risk", "conversion", "president", "product", "margin", "overhead", "payback", 
                           "cost", "revenue", "sales", "strategic"]
    
    is_related = False
    message_lower = user_message.lower()
    for term in rubber_bumper_terms:
        if term in message_lower:
            is_related = True
            break
    
    if not is_related:
        # Check if it's a general business question that might still be relevant
        business_terms = ["business", "company", "industry", "manufacture", "production", "strategy", 
                         "financial", "economic", "recommendation", "analysis"]
        
        for term in business_terms:
            if term in message_lower:
                is_related = True
                break
    
    # If clearly unrelated, acknowledge that
    if not is_related:
        return "I'm a specialized assistant focused on the Rubber Bumper case study. I can answer questions about Rubber Bumper's products (rubber bands and condoms), their market position, financial data, or strategic options like factory conversion. What would you like to know about Rubber Bumper?"
    
    # Get relevant context from the vector store
    relevant_contexts = vector_store.search(user_message, top_k=3)
    relevance_threshold = 0.25  # Minimum similarity score to consider a result relevant
    
    # Filter contexts with sufficient relevance
    filtered_contexts = [(doc, score) for doc, score in relevant_contexts if score > relevance_threshold]
    
    # If no sufficiently relevant context found
    if not filtered_contexts:
        # Return a helpful message suggesting topics to ask about
        suggested_topics = [
            "What are Rubber Bumper's main products?",
            "How has the rubber band market changed?",
            "How has the condom market changed?",
            "What is the profitability of each factory?",
            "Should they convert the rubber band factory to produce condoms?",
            "What risks are involved in factory conversion?"
        ]
        
        random_suggestion = suggested_topics[hash(user_message) % len(suggested_topics)]
        
        return (f"I don't have specific information about that aspect of Rubber Bumper Co. " 
                f"Try asking about their products, market position, factory profitability, or the potential factory conversion project.\n\n"
                f"For example: \"{random_suggestion}\"")
    
    # Use the most relevant context to formulate a response
    best_context = filtered_contexts[0][0]
    
    # Determine if the context text directly answers the question
    # Some keywords that might indicate different types of questions
    question_type = "information"
    if "compare" in message_lower or "difference" in message_lower or "versus" in message_lower or " vs " in message_lower:
        question_type = "comparison"
    elif "recommend" in message_lower or "should" in message_lower or "best option" in message_lower:
        question_type = "recommendation"
    elif "why" in message_lower or "reason" in message_lower or "cause" in message_lower:
        question_type = "explanation"
    
    # Format the response based on question type
    if question_type == "comparison":
        return f"Based on the Rubber Bumper case study, here's a comparison I found:\n\n{best_context.strip()}"
    elif question_type == "recommendation":
        return f"Regarding your question about recommendations for Rubber Bumper Co:\n\n{best_context.strip()}"
    elif question_type == "explanation":
        return f"Here's why this is happening at Rubber Bumper Co:\n\n{best_context.strip()}"
    else:
        return f"Based on the Rubber Bumper case study data:\n\n{best_context.strip()}"
