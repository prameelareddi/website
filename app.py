# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the directory containing chatbot.py to the Python path
# This ensures that 'import chatbot' will find chatbot.py
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import chatbot # Import your chatbot logic

app = Flask(__name__)
# Enable CORS for all routes, allowing your frontend to communicate with this backend.
# In a production environment, you might restrict this to your specific frontend URL.
CORS(app)

@app.route('/')
def home():
    """
    A simple home route to confirm the Flask server is running.
    """
    return "InnovateSoft Backend is Running!"

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    """
    Handles contact form submissions.
    It receives JSON data from the frontend and prints it to the console.
    In a real application, you would save this data to a database, send an email, etc.
    """
    if request.is_json:
        data = request.get_json()
        print("Received Contact Form Submission:")
        print(f"Name: {data.get('name')}")
        print(f"Email: {data.get('email')}")
        print(f"Subject: {data.get('subject')}")
        print(f"Message: {data.get('message')}")

        # You can add logic here to:
        # - Store data in a database (e.g., PostgreSQL, MongoDB)
        # - Send an email notification (e.g., using Flask-Mail)
        # - Integrate with a CRM system

        return jsonify({"message": "Form submitted successfully!", "status": "success"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/chatbot_message', methods=['POST'])
def chatbot_message():
    """
    Handles chatbot messages from the frontend.
    It takes the user's message, passes it to the chatbot logic,
    and returns the chatbot's response.
    """
    if request.is_json:
        data = request.get_json()
        user_message = data.get('message')
        print(f"User message to chatbot: {user_message}")

        if not user_message:
            return jsonify({"response": "Please provide a message."}), 400

        try:
            # Get response from the chatbot logic
            bot_response = chatbot.get_chatbot_response(user_message)
            return jsonify({"response": bot_response}), 200
        except Exception as e:
            print(f"Error in chatbot response generation: {e}")
            return jsonify({"response": "Sorry, I'm having trouble responding right now. Please try again later."}), 500
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    # Run the Flask app on port 5000 (default)
    # debug=True allows for automatic reloading on code changes
    # For production, set debug=False and use a production WSGI server like Gunicorn or uWSGI
    app.run(debug=True, port=5000)
