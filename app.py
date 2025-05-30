from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import cohere
from flask_mail import Mail, Message
import datetime

app = Flask(__name__)

# Load API keys from environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Email settings (you can switch these to os.getenv for security)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'     # Replace with Gmail App Password

mail = Mail(app)

# Initialize Cohere
co = cohere.Client(COHERE_API_KEY)

# Helper functions
def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        condition = data['weather'][0]['description']
        return f"The weather in {city.title()} is {temp}°C with {condition}."
    else:
        return f"Sorry, I couldn’t fetch weather info for '{city}'."

def is_weather_query(msg):
    keywords = ['weather', 'temperature', 'climate']
    return any(word in msg.lower() for word in keywords)

def get_cohere_response(prompt):
    try:
        response = co.chat(model='command-nightly', message=prompt)
        return response.text.strip()
    except Exception as e:
        print("Cohere API error:", e)
        return "Sorry, I couldn't process that."


# Routes
@app.route('/')
def index():
    return render_template('s1.html')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@app.route('/static/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/list-models')
def list_models():
    return jsonify({"models": ["command-nightly"]})

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    if is_weather_query(user_msg):
        city = user_msg.split()[-1]
        reply = get_weather(city)
    else:
        reply = get_cohere_response(user_msg)
    return jsonify({'reply': reply})

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Optional: Save user to text file
    with open("user_log.txt", "a") as f:
        f.write(f"{timestamp} - {name} - {email}\n")

    # Send email notification to you
    try:
        msg = Message(
            subject="New Chatbot User",
            sender=app.config['MAIL_USERNAME'],
            recipients=['your_email@gmail.com'],  # Replace with your destination email
            body=f"New user just signed in:\n\n👤 Name: {name}\n📧 Email: {email}\n🕒 Time: {timestamp}"
        )
        mail.send(msg)
        return jsonify({"status": "success"})
    except Exception as e:
        print("Email error:", e)
        return jsonify({"status": "fail", "error": str(e)})

# Run server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
