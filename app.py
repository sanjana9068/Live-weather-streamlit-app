import streamlit as st
import json
import urllib.request
from datetime import datetime

st.set_page_config(page_title="Live Weather App", page_icon="🌦️")

API_KEY = "b587846c2df4596e6cabacdba9b5019f"

st.title("🌦️ Live Weather Report (India)")

# 🔹 User input (strip to remove extra spaces)
CITY = st.text_input("Enter City Name (India)", "Dehradun").strip()

if st.button("Get Weather"):
    if CITY == "":
        st.warning("⚠️ Please enter a city name")
    else:
        try:
            # ================= WEATHER API =================
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},IN&appid={API_KEY}&units=metric"
            response = urllib.request.urlopen(weather_url)
            data = json.loads(response.read())

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["description"]

            # ================= PRECIPITATION =================
            rain = data.get("rain", {}).get("1h", 0)
            snow = data.get("snow", {}).get("1h", 0)

            # ================= AQI =================
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            aqi_response = urllib.request.urlopen(aqi_url)
            aqi_data = json.loads(aqi_response.read())

            aqi_value = aqi_data["list"][0]["main"]["aqi"]

            aqi_status = {
                1: "Good 😊",
                2: "Fair 🙂",
                3: "Moderate 😐",
                4: "Poor 😷",
                5: "Very Poor ☠️"
            }.get(aqi_value, "Unknown")

            # ================= SEASON =================
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

            # ================= OUTPUT =================
            st.success("Weather data fetched successfully ✅")

            st.write(f"📍 **City:** {CITY.title()}")
            st.write(f"🗓️ **Season:** {season}")

            st.metric("🌡️ Temperature (°C)", temp)
            st.metric("🤗 Feels Like (°C)", feels_like)
            st.metric("💧 Humidity (%)", humidity)

            st.write(f"☁️ **Condition:** {weather}")
            st.write(f"🌧️ **Rain (last 1 hr):** {rain} mm")
            st.write(f"❄️ **Snow (last 1 hr):** {snow} mm")

            st.subheader("🌍 Air Quality")
            st.write(f"**AQI Level:** {aqi_value} ({aqi_status})")

        except:
            st.error("❌ City not found / API issue / Internet problem")
