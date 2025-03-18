from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_response

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

@app.route("/chat", methods=["POST"])
def chat():
    """Handles user messages and returns a response."""
    data = request.get_json()
    user_message = data.get("message", "")
    response_text = get_response(user_message)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
