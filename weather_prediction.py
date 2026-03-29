import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WeatherNow",
    page_icon="🌤️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #e8f4f8;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Title */
h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 3rem !important;
    letter-spacing: -1px;
    color: #e8f4f8 !important;
    margin-bottom: 0 !important;
}

/* Subtitle */
.subtitle {
    color: #7fb3c8;
    font-size: 1rem;
    margin-bottom: 2rem;
    font-weight: 300;
    letter-spacing: 0.5px;
}

/* Input label */
label {
    color: #a8d4e6 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

/* Input box */
input[type="text"] {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #e8f4f8 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border 0.2s;
}
input[type="text"]:focus {
    border: 1px solid #4fc3f7 !important;
    box-shadow: 0 0 0 3px rgba(79,195,247,0.15) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #4fc3f7, #0288d1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px;
    width: 100%;
    transition: opacity 0.2s, transform 0.1s;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
}

/* Weather card */
.weather-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2rem 2rem 1.5rem;
    margin-top: 1.5rem;
}

.city-name {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #e8f4f8;
    margin: 0;
    line-height: 1.1;
}

.condition-text {
    color: #7fb3c8;
    font-size: 1rem;
    font-weight: 300;
    text-transform: capitalize;
    margin-top: 0.25rem;
    margin-bottom: 1.5rem;
}

.temp-big {
    font-family: 'DM Serif Display', serif;
    font-size: 4.5rem;
    color: #4fc3f7;
    line-height: 1;
    margin-bottom: 1.5rem;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}

.stat-box {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 0.9rem 0.75rem;
    text-align: center;
}

.stat-icon { font-size: 1.4rem; }

.stat-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #7fb3c8;
    margin: 0.35rem 0 0.2rem;
}

.stat-value {
    font-size: 1.15rem;
    font-weight: 500;
    color: #e8f4f8;
}

/* Error box */
.error-box {
    background: rgba(239,83,80,0.12);
    border: 1px solid rgba(239,83,80,0.35);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    color: #ef9a9a;
    font-size: 0.95rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

CONDITION_ICONS = {
    "clear": "☀️", "cloud": "☁️", "rain": "🌧️",
    "drizzle": "🌦️", "thunder": "⛈️", "snow": "❄️",
    "mist": "🌫️", "fog": "🌫️", "haze": "🌫️",
    "smoke": "🌫️", "dust": "🌪️",
}

def get_condition_icon(description: str) -> str:
    desc_lower = description.lower()
    for keyword, icon in CONDITION_ICONS.items():
        if keyword in desc_lower:
            return icon
    return "🌤️"

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>WeatherNow</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time weather at your fingertips</p>', unsafe_allow_html=True)

api_key = "cf468a107a1ff14c67a26b9aec1d146f"  # Replace with your OpenWeatherMap API key
city    = st.text_input("City Name", placeholder="e.g. Mumbai, London, New York")

if st.button("Get Weather"):
    if not api_key.strip():
        st.markdown('<div class="error-box">⚠️ Please enter your OpenWeatherMap API key.</div>', unsafe_allow_html=True)
    elif not city.strip():
        st.markdown('<div class="error-box">⚠️ Please enter a city name.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Fetching weather data…"):
            try:
                resp = requests.get(
                    BASE_URL,
                    params={"q": city.strip(), "appid": api_key.strip(), "units": "metric"},
                    timeout=8,
                )
                data = resp.json()
            except requests.exceptions.ConnectionError:
                st.markdown('<div class="error-box">🔌 Connection error. Check your internet connection.</div>', unsafe_allow_html=True)
                st.stop()
            except requests.exceptions.Timeout:
                st.markdown('<div class="error-box">⏱️ Request timed out. Try again.</div>', unsafe_allow_html=True)
                st.stop()

        if data.get("cod") != 200:
            msg = data.get("message", "Unknown error")
            st.markdown(f'<div class="error-box">❌ {msg.capitalize()}. Please check the city name or API key.</div>', unsafe_allow_html=True)
        else:
            weather_desc = data["weather"][0]["description"]
            temp         = data["main"]["temp"]
            feels_like   = data["main"]["feels_like"]
            humidity     = data["main"]["humidity"]
            wind_speed   = data["wind"]["speed"]
            country      = data["sys"]["country"]
            icon         = get_condition_icon(weather_desc)

            st.markdown(f"""
            <div class="weather-card">
                <p class="city-name">{icon} {city.title()}, {country}</p>
                <p class="condition-text">{weather_desc}</p>
                <div class="temp-big">{temp:.1f}°C</div>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-icon">🌡️</div>
                        <div class="stat-label">Feels Like</div>
                        <div class="stat-value">{feels_like:.1f}°C</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-icon">💧</div>
                        <div class="stat-label">Humidity</div>
                        <div class="stat-value">{humidity}%</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-icon">💨</div>
                        <div class="stat-label">Wind</div>
                        <div class="stat-value">{wind_speed} m/s</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)