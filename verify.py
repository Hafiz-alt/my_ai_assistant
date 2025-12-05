import sys
import os
from dotenv import load_dotenv
from student_ai_kit import AIAssistant

# Load environment variables
load_dotenv()

class MessageWrapper:
    def __init__(self, original_message):
        self._msg = original_message
        
    def __getattr__(self, name):
        return getattr(self._msg, name)
        
    def __getitem__(self, name):
        # Allow dict-style access
        return getattr(self._msg, name)

try:
    assistant = AIAssistant()
    print("SUCCESS: AIAssistant initialized.")
    
    # Monkeypatch the client to fix the model name AND response format
    original_create = assistant.client.chat.completions.create
    
    def patched_create(*args, **kwargs):
        # Fix model
        if 'model' in kwargs:
            print(f"Monkeypatch: Replacing {kwargs['model']} with llama-3.1-8b-instant")
            kwargs['model'] = 'llama-3.1-8b-instant'
            
        response = original_create(*args, **kwargs)
        
        # Fix response format (make message subscriptable)
        for choice in response.choices:
            choice.message = MessageWrapper(choice.message)
            
        return response
        
    assistant.client.chat.completions.create = patched_create
    print("SUCCESS: Applied monkeypatch for model and response.")

except Exception as e:
    print(f"ERROR: Could not initialize AIAssistant. {e}")
    sys.exit(1)

# Test functions
try:
    print("Testing get_response with real API key and patched client...")
    resp = assistant.get_response("Say 'Hello World' briefly.")
    print(f"get_response result: {resp}")
    
    formatted = assistant.format_response("Line 1\nLine 2")
    print(f"format_response test: {formatted}")
    
    print("SUCCESS: Full library integration verified with API key.")
except Exception as e:
    print(f"ERROR: Function test failed. {e}")
    sys.exit(1)
