# prediction.py
# -------------------------------------------------------------------
import json
import pickle
from warnings import filterwarnings

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid

import get_data  # your helper for reading CSV

filterwarnings("ignore")

# -------------------------------------------------------------------
# 1. Utility helpers
# -------------------------------------------------------------------
def load_lottiefile(filepath: str):
    """Load a local Lottie animation JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)

@st.cache_resource(show_spinner=False)
def load_model(path: str = "houseing_model"):
    """Load and cache the pickled LightGBM model."""
    with open(path, "rb") as f:
        return pickle.load(f)

model = load_model()  # cached once per session

# -------------------------------------------------------------------
# 2. Lookup dictionaries  (shortened here – include full list in prod)
# -------------------------------------------------------------------
house_condition_dict = {1: "new", 0: "old"}
house_type_dict = {1: "Apartment", 0: "Independent house"}
BHK_dict = {1.0: "1", 2.0: "2", 3.0: "3", 4.0: "4", 5.0: "5"}

location_dict = {
    55.088: "Canada Corner",
    44.45074394774749: "Chandshi",
    43.991854295812175: "Dwarka",
    # ... add ALL other mappings used in training ...
}

# -------------------------------------------------------------------
# 3. Streamlit app
# -------------------------------------------------------------------
def app() -> None:
    st.title("Nashik Apartment Price Prediction 🏠")

    # Lottie header
    try:
        st_lottie(load_lottiefile("home.json"), speed=1, loop=True, quality="low")
    except FileNotFoundError:
        st.info("home.json animation not found – skipping animation.")

    st.markdown(
        """
        Nashik, the wine capital of India, is growing fast as an affordable
        alternative to Mumbai & Pune. Use this app to estimate apartment prices
        and explore current listings.
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------------------------------------------
    # User inputs
    # ----------------------------------------------------------------
    st.header("Estimate the price of your dream house ✨")

    with st.form(key="predict_form"):
        house_type = st.selectbox(
            "House Type", list(house_type_dict.keys()),
            format_func=lambda x: house_type_dict[x],
        )
        house_condition = st.selectbox(
            "House Condition", list(house_condition_dict.keys()),
            format_func=lambda x: house_condition_dict[x],
        )
        BHK = st.selectbox(
            "Number of BHK", list(BHK_dict.keys()),
            format_func=lambda x: BHK_dict[x],
        )
        total_sqft = st.number_input(
            "Total square‑foot area", min_value=100.0, value=1000.0, step=10.0
        )
        location = st.selectbox(
            "Location", list(location_dict.keys()),
            format_func=lambda x: location_dict[x],
        )
        submitted = st.form_submit_button("Predict")

    if submitted:
        try:
            features = np.array([[house_type, house_condition, BHK, total_sqft, location]])
            price_lakhs = model.predict(features)[0]
            st.success(f"Estimated price: ₹ {round(price_lakhs, 2)} Lakhs")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

    # ----------------------------------------------------------------
    # Map of listings
    # ----------------------------------------------------------------
    st.header("Explore Nashik listings by budget 💰")
    st.text("(Hover over markers for details)")

    df = get_data.get_data(path="read_data/raw_data.csv")

    def show_map(min_price: float, max_price: float):
        dff = df[df["price"].between(min_price, max_price, inclusive="both")]
        fig = px.scatter_mapbox(
            dff,
            lat="latitude",
            lon="longitude",
            hover_name="address",
            color="housetype",
            color_discrete_sequence=["brown", "green"],
            hover_data=[
                "owners",
                "house_condition",
                "BHK",
                "price",
                "per_month_emi",
                "total_sqft",
            ],
            zoom=11,
            height=500,
            width=1000,
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.sidebar.subheader("Pick your budget (₹ Lakhs)")
    choice = st.sidebar.radio(
        "", ("1 – 15", "15 – 30", "30 – 45", "45 – 60", "60 and above")
    )

    ranges = {
        "1 – 15": (1.0, 15.0),
        "15 – 30": (15.0, 30.0),
        "30 – 45": (30.0, 45.0),
        "45 – 60": (45.0, 60.0),
        "60 and above": (60.0, df["price"].max()),
    }
    show_map(*ranges[choice])

# -------------------------------------------------------------------
if __name__ == "__main__":
    app()
