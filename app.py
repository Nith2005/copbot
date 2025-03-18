from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_response

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

@app.route("/chat", methods=["POST"])
def chat():
    """Handles user messages and returns a response."""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"response": "Please enter a valid query."})

        print(f"User query received: {user_message}")  # Debugging log
        
        response_text = get_response(user_message)
        print(f"Response sent: {response_text}")  # Debugging log
        
        return jsonify({"response": response_text})
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"response": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)

