from flask import Flask, render_template, request, jsonify
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# Replace this with your actual key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
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
def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()
@app.route('/')
def index():
    return render_template('s1.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')

    if 'weather' in user_msg.lower():
        # Your weather function here (replace as needed)
        reply = "Weather info coming soon..."
    else:
        reply = ask_gpt(user_msg)

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
