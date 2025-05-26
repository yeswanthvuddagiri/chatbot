from flask import Flask, render_template, request, jsonify
import requests
import os
app = Flask(__name__)

# Replace this with your actual key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
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
def is_basic_question(msg):
    keywords = ['who', 'what', 'when', 'where', 'how', 'why', 'hello', 'hi', 'help']
    return any(word in msg.lower() or msg.upper() for word in keywords)
def handle_basic_question(msg):
    # For now, simple canned replies
    if 'hello' in msg.lower() or 'hi' in msg.lower()  'hello' in msg.upper() or 'hi' in msg.upper() :
        return "Hello! How can I assist you today?"
    elif 'help' in msg.upper():
        return "I can provide weather info or answer basic questions. Try asking me!"
    else:
        return "That's a great question! I'm still learning to answer that."

@app.route('/')
def index():
    return render_template('s1.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')

    if is_weather_query(user_msg):
        # Extract city, etc.
        city = user_msg.split()[-1]
        bot_reply = get_weather(city)
    elif is_basic_question(user_msg):
        bot_reply = handle_basic_question(user_msg)
    else:
        bot_reply = "Sorry, I didn't understand that. Try asking about weather or say hi!"

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
