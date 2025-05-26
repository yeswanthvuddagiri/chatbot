from flask import Flask, render_template, request, jsonify
import requests
import os
import google.generativeai as genai

app = Flask(__name__)

# Replace this with your actual key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')def get_weather(city):
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
def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Sorry, I couldn't process that with That."

@app.route('/')
def index():
    return render_template('s1.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')

    if is_weather_query(user_msg):
        city = user_msg.split()[-1]
        reply = get_weather(city)
    elif 'joke' in user_msg.lower():
        reply = get_joke()
    elif 'define' in user_msg.lower():
        word = user_msg.lower().split("define")[-1].strip()
        reply = get_definition(word)
    else:
        reply = get_gemini_response(user_msg)

    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
