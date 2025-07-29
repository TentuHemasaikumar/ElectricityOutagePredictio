import streamlit as st
import joblib
import requests
import numpy as np

# 🔑 OpenWeatherMap API Key
API_KEY = "9ec898ed86ffafa9f14138eade261bf0"  # Replace with your real API key

# 🚀 Load the trained Random Forest model
model = joblib.load("models/rf_outage_model.pkl")

# 🌦️ Get weather data from OpenWeatherMap
def get_weather_data(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        weather_info = {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["main"]
        }
        return weather_info
    except:
        return None

# 🔁 Map weather condition to number
weather_mapping = {
    'Clear': 0,
    'Clouds': 1,
    'Rain': 2,
    'Haze': 3,
    'Thunderstorm': 4,
    'Drizzle': 5,
    'Mist': 6,
    'Fog': 7
}

# 🎯 Streamlit UI
st.title("⚡ Electricity Outage Prediction App")

city = st.text_input("Enter town / city / village name (India)", "")

if city:
    weather = get_weather_data(city)
    
    if weather:
        st.subheader("📊 Real-Time Weather Data")
        st.json(weather)

        # Handle unknown weather types safely
        weather_code = weather_mapping.get(weather["weather"], 0)

        # 🧠 Prepare input for model
        features = np.array([
            weather["temp"],
            weather["humidity"],
            weather["pressure"],
            weather["wind_speed"],
            weather_code
        ]).reshape(1, -1)

        # 🔮 Make prediction
        prediction = model.predict(features)[0]

        if prediction == 1:
            st.error("⚠️ Predicted: Power Outage Likely")
        else:
            st.success("✅ Predicted: No Power Outage")
    else:
        st.warning("⚠️ Could not fetch weather data. Please check city name.")
