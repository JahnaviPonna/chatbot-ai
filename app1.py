from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set up Gemini API
API_KEY = "AIzaSyDrkzsvbTU03fESOGxPYAWMe56dJpNS6L4"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Chat history storage (in-memory)
chat_history = {}

@app.route("/")
def home():
    return render_template("flaskfile.html")  # Serve the frontend

@app.route("/api", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    # Generate AI response
    response = model.generate_content(user_input)
    ai_response = response.text.strip() if response.text else "Sorry, I couldn't generate a response."

    # Store in chat history
    chat_id = str(data.get("chat_id", "default"))
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    chat_history[chat_id].append({"user": user_input, "ai": ai_response})

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
