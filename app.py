from flask import Flask, render_template, request
from student_ai_kit import AIAssistant
import os

app = Flask(__name__)

# --- Configuration ---
# Hardcoding key to ensure it works immediately
os.environ["GROQ_API_KEY"] = "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"

# --- Monkeypatch Start ---
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
        if 'model' in kwargs:
            kwargs['model'] = 'llama-3.1-8b-instant'
        response = original_create(*args, **kwargs)
        for choice in response.choices:
            choice.message = MessageWrapper(choice.message)
        return response
        
    assistant_instance.client.chat.completions.create = patched_create
# --- Monkeypatch End ---

# Initialize
assistant = None
try:
    print(f"Initializing AI with Key: {os.environ['GROQ_API_KEY'][:10]}...")
    assistant = AIAssistant()
    apply_patch(assistant)
    print("Success: AIAssistant initialized.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not initialize AIAssistant: {e}")
    assistant = None

# Global Chat History (In-Memory)
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_history
    
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        
        # Clear History Command
        if user_input and user_input.lower() == '/clear':
            chat_history = []
            return render_template('index.html', chat_history=chat_history)

        if user_input:
            # Add User Message
            chat_history.append({'role': 'user', 'content': user_input})
            
            if assistant:
                try:
                    # Build Context from History
                    context_messages = chat_history[-10:] 
                    full_prompt = ""
                    for msg in context_messages:
                        role = "User" if msg['role'] == 'user' else "AI"
                        full_prompt += f"{role}: {msg['content']}\n"
                    
                    # Append AI label to prompt for response
                    full_prompt += "AI:"
                    
                    # Get response
                    raw_response = assistant.get_response(full_prompt)
                    formatted_response = assistant.format_response(raw_response)
                    
                    # Add AI Message
                    chat_history.append({'role': 'ai', 'content': formatted_response})
                    
                except Exception as e:
                    error_msg = f"Error processing request: {str(e)}"
                    chat_history.append({'role': 'ai', 'content': error_msg})
            else:
                # Handle missing assistant
                error_msg = "Error: AI Assistant not initialized. Check server logs."
                chat_history.append({'role': 'ai', 'content': error_msg})
                
    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
