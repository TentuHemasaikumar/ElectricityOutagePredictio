import streamlit as st
import requests
import joblib

API_KEY = "9ec898ed86ffafa9f14138eade261bf0"  # Replace this!

model = joblib.load("models/rf_outage_model.pkl")

weather_conditions = ['Clear', 'Clouds', 'Rain', 'Haze', 'Thunderstorm', 'Dust', 'Fog']
weather_mapping = {condition: i for i, condition in enumerate(weather_conditions)}

def get_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},IN&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            'city': city_name,
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'weather': data['weather'][0]['main']
        }
    return None

st.set_page_config(page_title="AP Electricity Outage Predictor", layout="centered")

st.title("⚡ Andhra Pradesh Electricity Outage Predictor")
st.markdown("Enter any major city in Andhra Pradesh to get an outage risk prediction based on real-time weather data.")

city = st.text_input("Enter City Name (e.g., Visakhapatnam, Tirupati, Guntur, etc.)")

if st.button("Predict Outage"):
    if city:
        weather = get_weather(city, API_KEY)
        if weather:
            st.subheader("🌤️ Current Weather:")
            st.write(weather)
            weather_code = weather_mapping.get(weather['weather'], 0)
            features = [[
                weather['temp'], weather['humidity'], weather['pressure'],
                weather['wind_speed'], weather_code
            ]]
            prediction = model.predict(features)[0]
            if prediction == 1:
                st.error(f"⚠️ High Risk of Electricity Outage in {city}")
            else:
                st.success(f"✅ No Immediate Outage Risk in {city}")
        else:
            st.warning("❌ City not found or API error. Check spelling or try again later.")
    else:
        st.info("Please enter a city name to continue.")