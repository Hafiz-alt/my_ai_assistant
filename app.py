from flask import Flask, render_template, request
from student_ai_kit import AIAssistant
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

app = Flask(__name__)

# --- Monkeypatch Start ---
# The installed library uses a decommissioned model and expects dict access on response objects.
# We patch the client to fix these issues without modifying the library code.

class MessageWrapper:
    def __init__(self, original_message):
        self._msg = original_message
    def __getattr__(self, name):
        return getattr(self._msg, name)
    def __getitem__(self, name):
        return getattr(self._msg, name)

def apply_patch(assistant_instance):
    original_create = assistant_instance.client.chat.completions.create
    
    def patched_create(*args, **kwargs):
        # Fix model
        if 'model' in kwargs:
            kwargs['model'] = 'llama-3.1-8b-instant'
            
        response = original_create(*args, **kwargs)
        
        # Fix response format
        for choice in response.choices:
            choice.message = MessageWrapper(choice.message)
            
        return response
        
    assistant_instance.client.chat.completions.create = patched_create

# --- Monkeypatch End ---

# Initialize and patch
try:
    assistant = AIAssistant()
    apply_patch(assistant)
except Exception as e:
    print(f"Warning: Could not initialize AIAssistant: {e}")
    assistant = None

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    user_input = ""
    
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input and assistant:
            try:
                # Get response from the library
                raw_response = assistant.get_response(user_input)
                # Format the response
                response = assistant.format_response(raw_response)
            except Exception as e:
                response = f"Error: {str(e)}"
        elif not assistant:
            response = "Error: AI Assistant not initialized. Check API Key."
            
    return render_template('index.html', response=response, user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
