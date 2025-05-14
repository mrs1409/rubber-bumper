import os
import json
import re
from groq import Groq
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Groq API for better responses
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
groq_client = Groq(api_key=GROQ_API_KEY)

# Thread-local storage for context
thread_context = threading.local()

# Cache for storing previous responses to prevent duplicates
response_cache = {}

# System prompt with case study context for Groq LLM
SYSTEM_PROMPT = """You are a specialized assistant for the Rubber Bumper case study.
Provide direct, concise answers with no unnecessary text.
Never start responses with phrases like "Based on the case study" or "According to the information."
Just give the direct answer to the question in a single short sentence or paragraph.

Here's key information about Rubber Bumper Co:
- Small family-owned company producing rubber bands and condoms
- Has two factories: one for rubber bands, one for condoms
- Rubber band market has been flat (0% growth)
- Condom market has grown 30% from 2011 to 2017
- Rubber band factory: 40% profit margin, $4M profit (2017)
- Condom factory: 60% profit margin, $4.5M profit (2017)
- Converting rubber band factory would cost $2M and take 1 year
- Payback period would be 5 years (company target is 4 years)
- Key risks: uncertain market growth, marketing challenges, employee training
"""

def get_direct_response(user_message):
    """
    Generate a direct response based on predefined questions about Rubber Bumper.

    Args:
        user_message: A string containing the user's message.

    Returns:
        A string containing the response if a matching question is found, otherwise None.
    """
    # Convert message to lowercase for case-insensitive matching
    message_lower = user_message.lower().strip()

    # Check if we've seen this exact question before
    if message_lower in response_cache:
        logger.info(f"Using cached response for: {message_lower}")
        return response_cache[message_lower]

    # Handle greetings and common phrases
    greetings = ["hello", "hi ", "hey", "greetings", "howdy", "good morning", "good afternoon", "good evening"]
    for greeting in greetings:
        if greeting in message_lower and len(message_lower) < len(greeting) + 5:
            response = "Hello! I'm your Rubber Bumper case study assistant. How can I help you?"
            response_cache[message_lower] = response
            return response

    # Handle thank you messages
    thanks = ["thank you", "thanks", "appreciate", "grateful"]
    for thank in thanks:
        if thank in message_lower and len(message_lower) < len(thank) + 10:
            response = "You're welcome!"
            response_cache[message_lower] = response
            return response

    # Handle questions about the chatbot
    bot_questions = ["who are you", "what are you", "what can you do", "how do you work", "what do you know"]
    for question in bot_questions:
        if question in message_lower:
            response = "I'm a specialized assistant for the Rubber Bumper case study. I can answer questions about their products, market position, financial data, and strategic options."
            response_cache[message_lower] = response
            return response

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
        "what products": "Rubber Bumper Co sells two products: rubber bands and condoms.",
        "what product": "Rubber Bumper Co sells two products: rubber bands and condoms.",
        "what does rubber bumper make": "Rubber Bumper Co makes rubber bands and condoms.",
        "what does rubber bumper sell": "Rubber Bumper Co sells rubber bands and condoms.",
        "how many products": "Rubber Bumper Co sells two products: rubber bands and condoms.",
        "compare products": "Rubber Bumper Co sells rubber bands and condoms. The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin.",

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
        "decreasing profits": "Rubber Bumper has experienced decreasing profits over the last couple of years, despite stable sales.",
        "profit": "The condom factory had a profit of $4.5 million in 2017, while the rubber band factory had a profit of $4 million.",
        "margin": "The condom factory has a 60% profit margin, while the rubber band factory has a 40% profit margin.",
        "profit margin": "The condom factory has a 60% profit margin, while the rubber band factory has a 40% profit margin.",
        "profitability": "The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin.",
        "which is more profitable": "The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin.",
        "compare profitability": "The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin.",

        # Markets
        "rubber band market": "The rubber band market has been flat (around 30-31 million pounds annually). Rubber Bumper's share has decreased from 4 million pounds in 2011 to 2 million pounds in 2017. The dominant player (Max Rubber) has increased from 17 to 24 million pounds.",
        "condom market": "The condom market has grown from 350 million units in 2011 to 450 million in 2017 (30% growth). Rubber Bumper's sales grew from 1 million to 10 million units but have plateaued since 2014.",
        "market growth": "The rubber band market has been flat, while the condom market has grown 30% from 2011 to 2017.",
        "market trend": "The rubber band market has been flat, while the condom market has shown strong growth (30% from 2011 to 2017).",
        "market trends": "The rubber band market has been flat, while the condom market has shown strong growth (30% from 2011 to 2017).",
        "what are the market trends": "The rubber band market has been flat, while the condom market has shown strong growth (30% from 2011 to 2017).",

        # Factories
        "factory": "Rubber Bumper has two factories: a larger rubber band factory with $4 million annual overhead, and a smaller condom factory with $2 million annual overhead.",
        "factories": "Rubber Bumper has two factories: a larger rubber band factory with $4 million annual overhead, and a smaller condom factory with $2 million annual overhead.",
        "production": "Rubber Bumper produces rubber bands in one factory and condoms in another factory.",
        "how many factories": "Rubber Bumper has two factories - one for rubber bands and one for condoms.",

        # Factory conversion
        "convert factory": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year. After conversion, the factory could produce 20 million condoms total, with a potential profit of $11 million. The payback period would be approximately 5 years.",
        "convert the factory": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year. After conversion, the factory could produce 20 million condoms total, with a potential profit of $11 million. The payback period would be approximately 5 years.",
        "conversion": "Converting the rubber band factory to produce condoms would cost $2 million and take 1 year. After conversion, the factory could produce 20 million condoms total, with a potential profit of $11 million. The payback period would be approximately 5 years.",
        "should they convert": "Converting the factory has long-term benefits but the 5-year payback period exceeds the company's 4-year target. Market research to verify demand for increased condom production is recommended.",
        "should they convert the factory": "Converting the factory has long-term benefits but the 5-year payback period exceeds the company's 4-year target. Market research to verify demand for increased condom production is recommended.",

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
        response = qa_dict[message_lower]
        response_cache[message_lower] = response
        return response

    # Score-based matching for partial matches
    best_match = None
    best_score = 0

    # Split the user message into words for better matching
    message_words = set(message_lower.split())

    for key, answer in qa_dict.items():
        # Skip very short keys that might cause false matches
        if len(key) < 4:
            continue

        # Calculate match score based on word overlap
        key_words = set(key.split())
        overlap = message_words.intersection(key_words)

        # Score is based on number of matching words and their proportion to key length
        if overlap:
            score = len(overlap) / max(len(message_words), len(key_words))

            # Boost score for keys that are fully contained in the message
            if key in message_lower:
                score += 0.5

            # Update best match if this score is higher
            if score > best_score:
                best_score = score
                best_match = answer

    # Return the best match if it exceeds a threshold
    if best_score > 0.4:
        response_cache[message_lower] = best_match
        return best_match

    # No good match found
    return None

def get_groq_response(user_message):
    """
    Get a response from the Groq API for Rubber Bumper questions.

    Args:
        user_message: A string containing the user's message.

    Returns:
        A string containing the generated response.
    """
    # Check if we've seen this exact question before in the cache
    message_lower = user_message.lower().strip()
    if message_lower in response_cache:
        logger.info(f"Using cached Groq response for: {message_lower}")
        return response_cache[message_lower]

    try:
        # Check if the user message is related to Rubber Bumper
        rubber_terms = ["rubber", "bumper", "band", "condom", "factory", "profit", "market",
                       "competitor", "conversion", "president", "margin", "payback", "company",
                       "product", "sales", "recommendation", "risk", "convert"]

        # Only enforce Rubber Bumper relevance for longer queries
        if len(message_lower.split()) > 3 and not any(term in message_lower for term in rubber_terms):
            response = "I can only answer questions about Rubber Bumper Co."
            response_cache[message_lower] = response
            return response

        # Get response from Groq API
        logger.info(f"Sending request to Groq API: {user_message}")

        # Get context from thread local storage if available
        context = getattr(thread_context, 'context', None)

        # Prepare messages with context if available
        if context:
            enhanced_prompt = SYSTEM_PROMPT + "\n\nAdditional context for this question:\n" + context
            messages = [
                {"role": "system", "content": enhanced_prompt},
                {"role": "user", "content": user_message}
            ]
            logger.info("Using enhanced prompt with context")
        else:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]

        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # Using Llama 3 model for fast, efficient responses
            messages=messages,
            temperature=0.2,  # Low temperature for more factual responses
            max_tokens=300,   # Limit response length for conciseness
            top_p=0.95        # High precision for accurate answers
        )

        # Extract and return the generated text
        if response and response.choices and len(response.choices) > 0 and response.choices[0].message:
            answer = response.choices[0].message.content
            if answer:
                answer = answer.strip()

                # Make sure the answer is concise - take first paragraph only if needed
                if len(answer) > 300:
                    # Try to find the first paragraph break
                    paragraphs = answer.split('\n\n')
                    if paragraphs:
                        answer = paragraphs[0]

                # Cache the response for future use
                response_cache[message_lower] = answer
                return answer
            else:
                default_response = "Rubber Bumper Co makes rubber bands and condoms."
                response_cache[message_lower] = default_response
                return default_response
        else:
            default_response = "Rubber Bumper Co makes rubber bands and condoms."
            response_cache[message_lower] = default_response
            return default_response

    except Exception as e:
        # If API fails, log the error and fall back to direct response
        logger.error(f"Groq API error: {str(e)}")

        # Try to get a direct response
        direct_response = get_direct_response(user_message)
        if direct_response:
            return direct_response

        # If no direct response, return a default response
        default_response = "The rubber band market has been flat, while the condom market has grown 30% from 2011 to 2017. The condom business is more profitable with a 60% margin compared to the rubber band business with a 40% margin."
        response_cache[message_lower] = default_response
        return default_response


def get_context_from_vector_store(user_message, vector_store, max_results=2):
    """
    Get relevant context from the vector store based on the user's message.

    Args:
        user_message: A string containing the user's message.
        vector_store: A VectorStore object containing the document vectors.
        max_results: Maximum number of results to return.

    Returns:
        A string containing the relevant context.
    """
    if not vector_store:
        return ""

    # Search for relevant documents
    results = vector_store.search(user_message, top_k=max_results)

    if not results:
        return ""

    # Combine the relevant documents into a context string
    context = "\n\n".join([doc for doc, score in results if score > 0.2])
    return context

def get_chat_response(user_message, vector_store, max_context_length=None):
    """
    Generate a direct response to a user message about Rubber Bumper.

    Args:
        user_message: A string containing the user's message.
        vector_store: A VectorStore object containing the document vectors.
        max_context_length: Deprecated parameter, kept for backward compatibility.

    Returns:
        A string containing the generated response.
    """
    # Check if the message is empty or too short
    if not user_message or len(user_message.strip()) < 2:
        return "Please ask me a question about Rubber Bumper Co."

    # Try to get a direct response to common questions first
    direct_response = get_direct_response(user_message)
    if direct_response:
        return direct_response

    # Get relevant context from the vector store
    context = get_context_from_vector_store(user_message, vector_store)

    # If we have relevant context, store it in thread local storage
    if context and len(context) > 50:
        # Log that we're using vector store context
        logger.info(f"Using vector store context for: {user_message}")

        # Store context in thread local storage for use in get_groq_response
        thread_context.context = context
    else:
        # Clear any previous context
        if hasattr(thread_context, 'context'):
            delattr(thread_context, 'context')

    # If no direct answer in our database, use Groq API
    return get_groq_response(user_message)
