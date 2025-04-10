import streamlit as st
from streamlit_lottie import st_lottie
import json
from datetime import datetime
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="Code Hunt", layout="wide", initial_sidebar_state="collapsed")

# --- Load Animation ---
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_login = load_lottie("login_animation.json")

# --- Hide Sidebar, Header, Footer ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            margin: 0 !important;
            padding: 0 !important;
            height: 100%;
            width: 100%;
            background-color: #0f1117;
            color: white;
        }
        #MainMenu, footer, header, section[data-testid="stSidebar"] {
            display: none !important;
        }
        .main {
            padding: 0 !important;
        }
        .login-box {
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 2rem;
            width: 100%;
            max-width: 400px;
            text-align: center;
            animation: fadeInUp 1s ease;
        }
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translate3d(0, 40px, 0);
            }
            to {
                opacity: 1;
                transform: none;
            }
        }
        .custom-button {
            background-color: #007bff;
            color: white;
            padding: 0.6rem 1.5rem;
            border-radius: 10px;
            font-size: 1rem;
            border: none;
            cursor: pointer;
        }
        .custom-button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fullscreen + Tab Change Warning JS ---
st.markdown("""
    <script>
        window.onload = () => {
            const docEl = document.documentElement;
            if (docEl.requestFullscreen) {
                docEl.requestFullscreen();
            } else if (docEl.webkitRequestFullscreen) {
                docEl.webkitRequestFullscreen();
            } else if (docEl.msRequestFullscreen) {
                docEl.msRequestFullscreen();
            }
        };

        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "left" }, "*");
            }
        });

        window.onblur = () => {
            window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "left" }, "*");
        };

        document.addEventListener("fullscreenchange", () => {
            if (!document.fullscreenElement) {
                window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: "left" }, "*");
            }
        });
    </script>
""", unsafe_allow_html=True)

# --- Warning on tab switch ---
warning_placeholder = st.empty()
js_trigger = warning_placeholder.text_input("tab_check", label_visibility="collapsed", key="tab_event")

if js_trigger == "left":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    warning_placeholder.warning(f"⚠️ {timestamp} — Please stay in fullscreen mode and avoid switching tabs.")

# --- Header & Image ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center;">Accolade 3.0 presents<br>Code Hunt</h2>', unsafe_allow_html=True)
image = Image.open("codehunt_banner.jpg")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(image, width=800)

# --- Lottie Animation + Login ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st_lottie(lottie_login, height=180, key="login_animation")

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        year = st.selectbox("🎓 Select your year", ["Select Year", "1st Year", "2nd Year", "3rd Year"])

        if st.button("Login ✅", use_container_width=True):
            if username.strip() == "" or password.strip() == "" or year == "Select Year":
                st.error("Please enter all details and select your year.")
            elif password != "Pranav@123":
                st.error("Incorrect password.")
            else:
                st.session_state.username = username
                st.session_state.logged_in = True
                st.session_state.year = year
                st.success("Login successful!")
                st.switch_page("pages/Instructions.py")

        st.markdown('</div>', unsafe_allow_html=True)
