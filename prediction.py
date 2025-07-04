import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pickle
import json
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid
import get_data
from warnings import filterwarnings

filterwarnings("ignore")

###############################################################################
# --------------------------- Utility Functions ----------------------------- #
###############################################################################

def load_lottiefile(filepath: str):
    """Load a local Lottie animation JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


@st.cache_resource(show_spinner=False)
def load_model(path: str = "houseing_model"):
    """Load and cache the pre‑trained LightGBM model."""
    return pickle.load(path)


# Load the trained model once per session
model = load_model()

###############################################################################
# --------------------------- Lookup Dictionaries --------------------------- #
###############################################################################

house_condition_dict = {1: "new", 0: "old"}
house_type_dict = {1: "Apartment", 0: "Independent house"}
BHK_dict = {1.0: "1", 2.0: "2", 3.0: "3", 4.0: "4", 5.0: "5"}

# (location_dict abridged for brevity – use the full dictionary from your data)
location_dict = {
    55.088: "Canada Corner",
    44.45074394774749: "Chandshi",
    43.991854295812175: "Dwarka",
    # ... add the rest of your mappings here ...
}

###############################################################################
# --------------------------- Streamlit App --------------------------------- #
###############################################################################

def app():
    st.title("Nashik Apartment Price Prediction 🏠")

    # ------------------------------------------------------------------
    # Intro Lottie animation
    # ------------------------------------------------------------------
    try:
        lottie_coding = load_lottiefile("home.json")
        st_lottie(lottie_coding, speed=1, loop=True, quality="low")
    except FileNotFoundError:
        st.info("home.json animation file not found – skipping animation.")

    # ------------------------------------------------------------------
    # About section
    # ------------------------------------------------------------------
    st.markdown(
        """
        Nashik, the wine capital of India, is quickly becoming a preferred city for
        both investment and retirement living. With soaring real‑estate prices in
        Mumbai and Pune, Nashik offers an attractive alternative. This app helps
        you estimate apartment prices across Nashik and visualise listings by
        budget.
        """
    )

    # ------------------------------------------------------------------
    # User inputs for prediction
    # ------------------------------------------------------------------
    st.header("Find the price for your dream house ✨")

    house_type = st.selectbox("House Type", list(house_type_dict.keys()), format_func=lambda x: house_type_dict[x])
    house_condition = st.selectbox("House Condition", list(house_condition_dict.keys()), format_func=lambda x: house_condition_dict[x])
    BHK = st.selectbox("Number of BHK", list(BHK_dict.keys()), format_func=lambda x: BHK_dict[x])
    total_sqft = st.number_input("Total square‑foot area", min_value=100.0, value=1000.0, step=10.0)
    location = st.selectbox("Location", list(location_dict.keys()), format_func=lambda x: location_dict[x])

    if st.button("Predict"):
        try:
            features = np.array([[house_type, house_condition, BHK, total_sqft, location]])
            prediction = model.predict(features)[0]
            st.success(f"Estimated price: ₹ {round(prediction, 2)} Lakhs")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

    # ------------------------------------------------------------------
    # Interactive map section
    # ------------------------------------------------------------------
    st.header("Explore properties on the Nashik map 💰")
    st.text("(Tip: hover over points for more details)")

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
            hover_data=["owners", "house_condition", "BHK", "price", "per_month_emi", "total_sqft"],
            zoom=11,
            height=500,
            width=1000,
        )
        fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    st.sidebar.subheader("Pick your budget")
    price_range = st.sidebar.radio(
        "Budget range (₹ Lakhs)",
        (
            "1 – 15",
            "15 – 30",
            "30 – 45",
            "45 – 60",
            "60 and above",
        ),
    )

    if price_range == "1 – 15":
        show_map(1.0, 15.0)
    elif price_range == "15 – 30":
        show_map(15.0, 30.0)
    elif price_range == "30 – 45":
        show_map(30.0, 45.0)
    elif price_range == "45 – 60":
        show_map(45.0, 60.0)
    else:  # "60 and above"
        show_map(60.0, df["price"].max())


if __name__ == "__main__":
    app()
