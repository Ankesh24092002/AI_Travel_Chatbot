import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv(override=True)

# Initialize the Gemini API with your API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the Gemini model
model = genai.GenerativeModel('models/gemini-1.0-pro')
chat = model.start_chat(history=[])

@app.route('/')
def index():
    return render_template('trip.html')

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    user_message = request.form.get('user_message')

    if user_message:
        prompt = f"""
        I want to plan a detailed trip. Here are the details: {user_message}. 
        Please provide a comprehensive itinerary including:
        1. Suggested destinations and routes.
        2. Daily activities and sightseeing recommendations.
        3. Accommodation suggestions for each night.
        4. Transportation options.
        5. Travel tips and advice.
        6. Any other relevant information for a smooth trip.
        Please give me a full response.
        """

        # Send the user's prompt to the model
        response = chat.send_message(prompt, stream=True)

        # Collect and return the full response text
        assistant_message = ''.join([chunk.text for chunk in response if chunk.text])

        return jsonify({"response": assistant_message})
    return jsonify({"response": "Please provide a message!"})

if __name__ == '__main__':
    app.run(debug=False)
