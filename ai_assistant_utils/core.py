import os
import random

def get_response(prompt, api_key=None):
    """
    Send a prompt to an AI tool and return the response.
    
    Args:
        prompt (str): The user's input query.
        api_key (str, optional): API key for the AI service. Defaults to None.
        
    Returns:
        str: The AI's response.
    """
    if not prompt:
        return "Please provide a prompt."

    # Real AI implementation would go here.
    # For this project, we will simulate an AI response if no key is provided
    # or if we want to demonstrate the flow without external dependencies.
    
    # Check for environment variable if not passed
    if not api_key:
        api_key = os.environ.get("AI_API_KEY")

    if api_key:
        # Placeholder for real API call (e.g., OpenAI or Gemini)
        # import google.generativeai as genai
        # genai.configure(api_key=api_key)
        # model = genai.GenerativeModel('gemini-pro')
        # response = model.generate_content(prompt)
        # return response.text
        return f"[Real AI Mode] Processed: {prompt}"
    else:
        # Mock responses for demonstration
        responses = [
            f"That's an interesting question about '{prompt}'. Here is a simulated AI answer.",
            f"I can help you with '{prompt}'. The solution involves several steps...",
            f"AI Assistant (Mock): You asked '{prompt}'. This is a great query!",
            f"Processing '{prompt}'... Done! Here is the result."
        ]
        return random.choice(responses)

def summarize_text(text):
    """
    Summarize a long text using AI.
    
    Args:
        text (str): The text to summarize.
        
    Returns:
        str: A summary of the text.
    """
    if not text:
        return "No text provided to summarize."
        
    # Simple mock summary logic
    words = text.split()
    if len(words) > 10:
        return "Summary: " + " ".join(words[:10]) + "..."
    return "Summary: " + text

def format_response(text):
    """
    Clean or process AI output before displaying.
    
    Args:
        text (str): The raw AI output.
        
    Returns:
        str: Formatted text (e.g., HTML safe or styled).
    """
    # Example: Convert newlines to HTML breaks or simple cleanup
    cleaned = text.strip()
    return cleaned.replace("\n", "<br>")
