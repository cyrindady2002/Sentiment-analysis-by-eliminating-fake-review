import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()  # Corrected to call r.json() method

# Load Lottie animations
lottie_co = load_lottieurl("https://lottie.host/0bd3638b-9334-488d-b1a3-fde2fabc19d7/dL0iGg9GmC.json")
lottie_review = load_lottieurl("https://lottie.host/caf5261f-702f-424d-9e40-e4ae89122693/eBsa56vUJH.json")

# Display Lottie animations using st_lottie
st_lottie(
    url="https://lottie.host/caf5261f-702f-424d-9e40-e4ae89122693/eBsa56vUJH.json",  # Provide URL directly
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
    height=None,
    width=None,
    key=None
)

# Display Lottie animation loaded from URL using load_lottieurl function
if lottie_review is not None:
    st_lottie(lottie_review, key="lottie_review_key")  # Provide the loaded animation as argument
else:
    st.error("Failed to load Lottie animation for review")

if lottie_co is not None:
    st_lottie(lottie_co, key="lottie_co_key")  # Provide the loaded animation as argument
else:
    st.error("Failed to load Lottie animation for co")

