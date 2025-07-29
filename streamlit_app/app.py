import requests
import streamlit as st

# ✅ Replace with your actual OpenWeatherMap API key
API_KEY = "9ec898ed86ffafa9f14138eade261bf0"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

    data = response.json()
    
    # If city is invalid or not found
    if "main" not in data:
        st.error(f"City not found: {data.get('message', 'Unknown error')}")
        return None

    weather_info = {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "weather": data["weather"][0]["main"]
    }

    return weather_info

# ✅ Streamlit App UI
st.title("⚡ Electricity Outage Prediction App")
city = st.text_input("Enter town / city / village name (India)")

if city:
    weather_data = get_weather(city)
    if weather_data:
        st.subheader("📊 Real-Time Weather Data")
        st.json(weather_data)
