import os
import json
import re

# Note: We're not actually using any external API calls in this chatbot anymore
# All responses are generated directly from our predefined knowledge base

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
            return "Hello! I'm your Rubber Bumper case study assistant. How can I help you?"
    
    # Handle thank you messages
    thanks = ["thank you", "thanks", "appreciate", "grateful"]
    for thank in thanks:
        if thank in message_lower:
            return "You're welcome!"
    
    # Handle questions about the chatbot
    bot_questions = ["who are you", "what are you", "what can you do", "how do you work", "what do you know"]
    for question in bot_questions:
        if question in message_lower:
            return "I'm a specialized assistant for the Rubber Bumper case study. I can answer questions about their products, market position, financial data, and strategic options."
    
    # Comprehensive dictionary of predefined questions and direct answers
    qa_dict = {
        # Company information
        "company name": "Rubber Bumper Co.",
        "name of the company": "Rubber Bumper Co.",
        "what is the company": "Rubber Bumper Co.",
        "who is the company": "Rubber Bumper Co.",
        "about the company": "Rubber Bumper Co is a small family-owned producer of rubber products.",
        "tell me about rubber bumper": "Rubber Bumper Co is a small family-owned producer of rubber products that sells rubber bands and condoms with highest quality on the market.",
        "what does rubber bumper do": "Rubber Bumper Co produces and sells rubber bands and condoms.",
        "what type of company": "Rubber Bumper Co is a small family-owned manufacturing company.",
        "company size": "Rubber Bumper Co is a small family-owned company with two factories.",
        
        # Products
        "what product": "Rubber Bumper Co sells two products: rubber bands and condoms.",
        "what does rubber bumper make": "Rubber Bumper Co makes rubber bands and condoms.",
        "what does rubber bumper sell": "Rubber Bumper Co sells rubber bands and condoms.",
        "how many products": "Rubber Bumper Co sells two products: rubber bands and condoms.",
        
        # Market position
        "market position": "Rubber Bumper is the market leader in both their product industries (rubber bands and condoms).",
        "market share": "In the rubber band market, Rubber Bumper's share has decreased from 4 million pounds in 2011 to 2 million pounds in 2017. In the condom market, they've grown from 1 million units in 2011 to 10 million in 2017.",
        "industry position": "Rubber Bumper is the market leader in both their product industries.",
        "leader": "Rubber Bumper is the market leader in both their product industries.",
        
        # Sales
        "topline sales": "Topline sales have remained relatively stable over the last 3 years.",
        "sales trend": "Topline sales have remained relatively stable over the last 3 years, despite decreasing profits.",
        "sales history": "Rubber band sales have decreased from 4 million pounds in 2011 to 2 million pounds in 2017. Condom sales have increased from 1 million units in 2011 to 10 million in 2017.",
        
        # Profitability
        "decreas": "Rubber Bumper has experienced decreasing profits over the last couple of years, despite stable sales.",
        "profit": "The condom factory had a profit of $4.5 million in 2017, while the rubber band factory had a profit of $4 million.",
        "margin": "The condom factory has a 60% profit margin, while the rubber band factory has a 40% profit margin.",
        "profit margin": "The condom factory has a 60% profit margin, while the rubber band factory has a 40% profit margin.",
        "profitab": "The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin.",
        "which is more profitable": "The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin.",
        
        # Markets
        "rubber band market": "The rubber band market has been flat (around 30-31 million pounds annually). Rubber Bumper's share has decreased from 4 million pounds in 2011 to 2 million pounds in 2017. The dominant player (Max Rubber) has increased from 17 to 24 million pounds.",
        "condom market": "The condom market has grown from 350 million units in 2011 to 450 million in 2017 (30% growth). Rubber Bumper's sales grew from 1 million to 10 million units but have plateaued since 2014.",
        "market growth": "The rubber band market has been flat, while the condom market has grown 30% from 2011 to 2017.",
        "market trend": "The rubber band market has been flat, while the condom market has shown strong growth (30% from 2011 to 2017).",
        
        # Factories
        "factory": "Rubber Bumper has two factories: a larger rubber band factory with $4 million annual overhead, and a smaller condom factory with $2 million annual overhead.",
        "factories": "Rubber Bumper has two factories: a larger rubber band factory with $4 million annual overhead, and a smaller condom factory with $2 million annual overhead.",
        "production": "Rubber Bumper produces rubber bands in one factory and condoms in another factory.",
        "how many factories": "Rubber Bumper has two factories - one for rubber bands and one for condoms.",
        
        # Factory conversion
        "convert": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year. After conversion, the factory could produce 20 million condoms total, with a potential profit of $11 million. The payback period would be approximately 5 years.",
        "conversion": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year. After conversion, the factory could produce 20 million condoms total, with a potential profit of $11 million. The payback period would be approximately 5 years.",
        "should they convert": "Converting the factory has long-term benefits but the 5-year payback period exceeds the company's 4-year target. Market research to verify demand for increased condom production is recommended.",
        "should they": "Converting the factory has long-term benefits but the 5-year payback period exceeds the company's 4-year target. Market research to verify demand for increased condom production is recommended.",
        
        # Recommendations
        "recommendation": "The company should first invest in market research to verify demand for increased condom production, while also exploring ways to reduce conversion costs to improve project economics.",
        "what should they do": "The company should first invest in market research to verify demand for increased condom production, while also exploring ways to reduce conversion costs to improve project economics.",
        "best option": "The best option is to first verify market demand for increased condom production before committing to the factory conversion, as the payback period currently exceeds their target.",
        
        # Risks
        "risk": "Key risks include: assuming Rubber Bumper can triple condom sales immediately, potential rebound in rubber band demand, political changes affecting the condom market, less product diversification, and employee resistance.",
        "risks": "Key risks include: assuming Rubber Bumper can triple condom sales immediately, potential rebound in rubber band demand, political changes affecting the condom market, less product diversification, and employee resistance.",
        "concern": "Key concerns include: the 5-year payback period exceeds the company's 4-year target, the assumption of tripling condom sales immediately may be unrealistic, and loss of product diversification increases market risk.",
        
        # Competitors
        "competitor": "In rubber bands, the main competitor is Max Rubber (24 million pounds in 2017). In condoms, major competitors are Spartan (115 million units) and Durable (170 million units).",
        "competitors": "In rubber bands, the main competitor is Max Rubber (24 million pounds in 2017). In condoms, major competitors are Spartan (115 million units) and Durable (170 million units).",
        "who are the competitors": "In rubber bands, the main competitor is Max Rubber. In condoms, major competitors are Spartan and Durable.",
        
        # Financial details
        "revenue": "The rubber band factory generates $10 million in revenue. The condom factory generates $7.5 million in revenue.",
        "cost": "Variable costs for the rubber band factory are $2 million, with $4 million overhead. Variable costs for the condom factory are $1 million, with $2 million overhead.",
        "overhead": "The rubber band factory has $4 million in annual overhead. The condom factory has $2 million in annual overhead.",
        
        # President
        "president": "The company has recently appointed a new President who noticed decreasing profits over the last couple of years.",
        "new president": "The company has recently appointed a new President who noticed decreasing profits over the last couple of years.",
        "who is the president": "The case study mentions that Rubber Bumper Co has recently appointed a new President who noticed decreasing profits."
    }
    
    # First check for exact matches with the whole question
    if message_lower in qa_dict:
        return qa_dict[message_lower]
    
    # Then check for partial matches
    for key, answer in qa_dict.items():
        if key in message_lower:
            return answer
    
    # No direct match found
    return None

def get_chat_response(user_message, vector_store, max_context_length=4000):
    """
    Generate a direct response to a user message about Rubber Bumper.
    
    Args:
        user_message: A string containing the user's message.
        vector_store: A VectorStore object containing the document vectors.
        max_context_length: An integer representing the maximum context length.
        
    Returns:
        A string containing the generated response.
    """
    # Check if the message is empty or too short
    if not user_message or len(user_message.strip()) < 2:
        return "Please ask me a question about Rubber Bumper Co."
    
    # First try to get a direct response to common questions
    direct_response = get_direct_response(user_message)
    if direct_response:
        return direct_response
    
    # Check if message contains "company name"
    message_lower = user_message.lower()
    if "company name" in message_lower or "name of the company" in message_lower or "what is the company" in message_lower:
        return "Rubber Bumper Co."
    
    # Check if the question appears to be about specific topics that aren't in the direct responses
    company_info_terms = ["what is rubber bumper", "describe rubber bumper", "tell me about the company", "information about rubber bumper"]
    for term in company_info_terms:
        if term in message_lower:
            return "Rubber Bumper Co is a small family-owned producer of rubber products that makes rubber bands and condoms."
    
    # Check if question is completely unrelated to Rubber Bumper
    rubber_bumper_terms = ["rubber", "bumper", "band", "condom", "factory", "profit", "market", "competitor", 
                           "risk", "conversion", "president", "product", "margin", "overhead", "payback", 
                           "cost", "revenue", "sales", "strategic", "company"]
    
    is_related = False
    for term in rubber_bumper_terms:
        if term in message_lower:
            is_related = True
            break
    
    # If clearly unrelated, give a brief response
    if not is_related:
        return "I can only answer questions about Rubber Bumper Co. Please ask me about their products, market position, financials, or strategic options."
    
    # Get relevant context from the vector store
    relevant_contexts = vector_store.search(user_message, top_k=3)
    
    # Get the best match regardless of score
    if relevant_contexts:
        best_context = relevant_contexts[0][0]
        
        # Extract key facts from the context
        lines = best_context.strip().split('\n')
        relevant_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('---'):
                relevant_lines.append(line)
        
        # Return the most direct, concise answer possible
        if relevant_lines:
            # For very short contexts, just return them directly
            if len(relevant_lines) <= 3:
                return " ".join(relevant_lines)
            # For longer contexts, be more selective
            else:
                # Look for the most specific sentence related to the question
                for line in relevant_lines:
                    for word in message_lower.split():
                        if word in line.lower() and len(line) < 150:  # Short, relevant line
                            return line
                
                # If no single line seems perfect, return the first line or two
                return " ".join(relevant_lines[:2])
    
    # Last resort fallback for Rubber Bumper-related questions we don't have specific info for
    if "product" in message_lower:
        return "Rubber Bumper Co sells two products: rubber bands and condoms."
    elif "factory" in message_lower or "factories" in message_lower:
        return "Rubber Bumper Co has two factories - one for producing rubber bands and one for producing condoms."
    elif "market" in message_lower:
        return "Rubber Bumper is the market leader in both their product industries (rubber bands and condoms)."
    elif "profit" in message_lower or "financial" in message_lower:
        return "The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin."
    else:
        return "Rubber Bumper Co is a small family-owned producer of rubber products that makes rubber bands and condoms. They're considering converting their rubber band factory to produce more condoms due to market trends and profitability differences."
