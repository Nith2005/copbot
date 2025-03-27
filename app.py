from flask import Flask, render_template, request, jsonify
from botspacy import get_response, get_greeting, get_termination
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})
    
    try:
        # Check for termination patterns first
        termination = get_termination(user_message)
        if termination:
            return jsonify({'response': termination, 'terminate': True})
        
        # Check for greetings
        greeting = get_greeting(user_message)
        if greeting:
            return jsonify({'response': greeting})
        
        # Process other queries
        response = get_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'response': 'Sorry, I encountered an error. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True) 