import streamlit as st
import json
import urllib.request
from datetime import datetime

st.set_page_config(page_title="Live Weather App", page_icon="🌦️")

API_KEY = "b587846c2df4596e6cabacdba9b5019f"

st.title("🌦️ Live Weather Report (India)")

# 🔹 NEW: User input for city
CITY = st.text_input("Enter City Name (India)", "Dehradun")

if st.button("Get Weather"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},IN&appid={API_KEY}&units=metric"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]

        # 🔹 Season logic (same as before)
        month = datetime.now().month
        if month in [12, 1, 2]:
            season = "Winter ❄️"
        elif month in [3, 4]:
            season = "Spring 🌸"
        elif month in [5, 6]:
            season = "Summer ☀️"
        elif month in [7, 8, 9]:
            season = "Monsoon 🌧️"
        else:
            season = "Autumn 🍁"

        st.success("Weather data fetched successfully ✅")

        st.write(f"📍 **City:** {CITY}")
        st.write(f"🗓️ **Season:** {season}")
        st.metric("🌡️ Temperature (°C)", temp)
        st.metric("🤗 Feels Like (°C)", feels_like)
        st.metric("💧 Humidity (%)", humidity)
        st.write(f"☁️ **Condition:** {weather}")

    except Exception as e:
        st.error("❌ City not found or API issue")

