from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import get_response
import os

app = Flask(__name__)
CORS(app)

# Set static folder explicitly
app.static_folder = os.path.abspath(os.path.dirname(__file__))
app.static_url_path = ''

@app.route('/')
def serve_html():
    print("Serving index.html...")  # Debug print
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    print(f"Serving static file: {filename}")  # Debug print
    return send_from_directory(app.static_folder, filename)

@app.route('/chat', methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        response_text = get_response(user_message)
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({"response": "Error processing request"}), 500

if __name__ == "__main__":
    print(f"Static folder path: {app.static_folder}")
    app.run(debug=True)