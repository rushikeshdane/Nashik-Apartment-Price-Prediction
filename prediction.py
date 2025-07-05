import json
import  get_data
import pickle
from warnings import filterwarnings

import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pickle
import json

import requests  # pip install requests
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid
import get_data
from warnings import filterwarnings

import get_data  # your helper for reading CSV

import plotly.express as px
filterwarnings("ignore")

# -------------------------------------------------------------------
# 1. Utility helpers
# -------------------------------------------------------------------
###############################################################################
# --------------------------- Utility Functions ----------------------------- #
###############################################################################

def load_lottiefile(filepath: str):
    """Load a local Lottie animation JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


@st.cache_resource(show_spinner=False)
def load_model(path: str = "houseing_model"):
    """Load and cache the pickled LightGBM model."""
    """Load and cache the pre‑trained LightGBM model."""
    with open(path, "rb") as f:
        return pickle.load(f)

model = load_model()  # cached once per session

# -------------------------------------------------------------------
# 2. Lookup dictionaries  (shortened here – include full list in prod)
# -------------------------------------------------------------------
# Load the trained model once per session
model = load_model()

location_dict ={41.19074425156919: 'Adgaon', 35.15558520943228:
    'Adhav Nagar', 33.27856689936921: 'Ambad Village', 38.9939456702571: 'Ambedkar Nagar',
                37.86019329602969: 'Amrutdham', 39.119435136709306: 'Anand Nagar',
                37.49946669821956: 'Anand Vihar Colony', 38.26167675974769: 'Ashok Nagar',
                35.133940693807254: 'Ashwamegh Nagar', 30.74821126624614: 'Ashwin Nagar',
                35.27: 'Astavinayak Colony', 35.942727272727275: 'Atharva Heights',
                27.58943661874724: 'Ayodhya Nagar', 45.23638928466679: 'Balawant Nagar',
                41.971999999999994: 'Balram Nagar', 42.312: 'Bhagwant Nagar',
                37.42216243941126: 'Bhujbal Knowledge City', 45.239102613654914: 'Buddha Vihar',
                55.088: 'Canada Corner', 44.45074394774749: 'Chandshi', 33.26123943581739: 'Chetana Nagar',
                34.758620689655174: 'Cidco Nashik', 44.34642253249226: 'College Road',
                42.67975586582561: 'DGP Nagar', 35.96514953441179: 'Damodar Nagar', 30.55: 'Date Nagar',
                28.474117647058822: 'Deepali Nagar', 38.265256105247055: 'Deolali Gaon',
                39.80810165162539: 'Dnyaneshwar Nagar', 43.991854295812175: 'Dwarka', 18.53: 'Forest Colony',
                41.02392675974768: 'Gajanan Nagar', 36.08003239287075: 'Gandhi Nagar Airport Area',14.487: '2nd Street & 3rd Avenue',
                39.83066197124835: 'Ganesh Baba Nagar', 43.38474205103208: 'Gangapur', 39.17699178301794: 'Gayakhe Colony', 51.06531848975282: 'Govind Nagar', 34.56889201572047: 'Gurudatta Nagar', 41.665: 'Hanuman Nagar', 36.43139013962151: 'Hirawadi', 42.32042422339444: 'Indira Nagar', 43.43070824677799: 'Jagtap Nagar Road', 45.89872372133011: 'Janak Nagari Road', 48.18116699909887: 'Jejurkar Wadi', 39.465011634672905: 'Kala Nagar', 40.74824178301793: 'Kalpataru Nagar', 40.43833674442233: 'Kamod Nagar', 33.481818181818184: 'Khutwad Nagar', 32.163238781336666: 'Kishor Nagar', 40.19427912635521: 'Kokanipura', 31.52896337987384: 'Konark Nagar', 49.26748731823378: 'L B Nagar Road', 32.050415905288666: 'Laxman Nagar', 46.01138539850903: 'Mahatma Nagar Road', 33.85112567682603: 'Mahatmanagar', 36.64362208630431: 'Makhmalabad', 40.78436306638631: 'Matoshree Nagar', 21.76: 'Matoshri Nagar', 30.75385351949536: 'Meri Colony', 33.666969131002254: 'Mhasrul Gaon', 33.27808919915895: 'Midc Ambad Nashik', 48.7181529128439: 'Murari Nagar', 42.073270162374776: 'Nandur Village', 49.42448731823379: 'Nashi', 33.833426223719414: 'Nashik', 33.41831559488374: 'Nashik Road', 19.439285714285713: 'Niphad', 39.329159621241: 'Ojhar', 22.178957744995788: 'Palase', 25.9499389664564: 'Panchak', 37.797312816234246: 'Panchavati', 38.34156213135812: 'Pandav Nagari', 43.39405633631092: 'Parijat Nagar', 36.868096212692095: 'Pathardi Gaon', 43.73560930270227: 'Pimpalgaon Bahula', 35.66370703899073: 'Pinto Colony', 41.22834886115028: 'Pokar Colony', 40.54182897034722: 'Prabhat Colony', 41.86150621087418: 'Prabhat Nagar', 38.89528027924304: 'Prashant Nagar', 46.55802816561535: 'Professors Colony Road', 33.967408449684605: 'Rajiv Nagar', 36.6913476623611: 'Ram Krishna Nagar', 38.876544599579475: 'Rane Nagar', 47.654750765107686: 'Raviwar Karanja', 33.49625: 'Rto Colony', 51.51300782110081: 'Sadguru Nagar', 36.686021124211514: 'Samarth Nagar', 24.353999999999996: 'Samraat Dream Citi', 38.04918108535383: 'Samta Nagar', 34.5871868528287: 'Saptashrungi Nagar', 32.451299632634765: 'Satpur', 38.036300465405084: 'Satpur Midc', 43.856933599279095: 'Serene Meadows', 44.629999999999995: 'Shankar Nagar', 49.01180064440704: 'Shanti Nagar Chowk', 40.071280279243055: 'Shivaji Nagar', 25.82315023270254: 'Shramik Nagar', 37.430457038990724: 'Sinnar', 38.093461538461526: 'Suyog Colony', 18.47934182849134: 'Swami Samarth Nagar', 32.275454545454544: 'Trimbak', 33.66692675974768: 'Uttam Nagar', 42.85337947313225: 'Vasantdada Nagar', 32.02680633726345: 'Vijaynagar', 42.379913834997275: 'Vivekanand Nagar', 32.63973613040628: 'Vrindavan Nagar', 43.998900018141676: 'Wadala', 45.95385210748524: 'Wasan Nagar', 35.49779873792046: 'other'}
house_condition_dict = {1:'new',0:'old'}
house_type_dict = {1:'Apartment',0:'Independent house'}
BHK_dict = {1.0:'1', 2.0:'2', 3.0:'3', 4.0:'4', 5.0:'5'}
def app():
    try:
        st.title('        Nashik Apartment Price Prediction')
        lottie_coding = load_lottiefile("home.json")
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="low"
        )
        st.markdown('Nashik is 4th largest city in Maharastra ,'
                 'Located at an approximate distance of 200 kms from Mumbai and Pune,'
                 'Nashik gained traction as a vacation hotspot and a location for investing in one’s retirement home.'
                 'As real estate prices in Pune and Mumbai soared, wine capital of India started being considered as a viable option'
                 ' for living. Social infrastructure gradually improved, with the economic growth of the city and with'
                 ' people choosing the region for their permanent homes. ')





        #CHOICES.keys(), format_func=lambda x:CHOICES[ x ]

        st.markdown('Inspiration 💡: I am always curious about real estate market in nashik ,many of my friend and relatives'
                    'are looking for buying house in Nashik .They are always asking me, if you could find any nearby apartement '
                    'within our budget then let us know , finding your dream house is real struggle. Then I thought with my'
                    ' python and data science skills , I can help them and make their job little easy. ')

###############################################################################
# --------------------------- Lookup Dictionaries --------------------------- #
###############################################################################

        st.header('Find Price for your Dream House 🏚️ ')
        house_type = st.selectbox('Select House Type',house_type_dict.keys(),format_func= lambda x:house_type_dict[x])

        house_condition=st.selectbox('Select House condition',house_condition_dict.keys(),format_func=lambda x:house_condition_dict[x])
        BHK=st.selectbox('Select Number of BHK ',BHK_dict.keys(),format_func=lambda x: BHK_dict[x])
        toatal_sqft=st.number_input('enter Total sqare foot area')
        location = st.selectbox('Select Location',location_dict.keys(),format_func=lambda x: location_dict[x])





        submit = st.button('Predict')
        if submit:
                loading_model = pickle.load(open('houseing_model', 'rb'))
                prediction = loading_model.predict([[house_type,house_condition,BHK,toatal_sqft,location]])

                st.subheader('The estimated price for your new house is {0} Lakhs '.format(round(prediction[0]),4))

        #st.select_slider('pick budget',options=['1lakh','10lakh','20lakh'])
        st.header('Select property on Nashik map according to your budget 💰')
        st.text('(note : hover your mouse on the map '
                        'to get extra detail about particular house)')
        def get_map(value1,value2):
            df = get_data.get_data(path='read_data/raw_data.csv')
            dff = df[df['price'].between(value1,value2,inclusive=True)]
            fig = px.scatter_mapbox(dff,
                                    lat=dff.latitude,
                                    lon=dff.longitude, hover_name='address', color='housetype',
                                    color_discrete_sequence=['brown', 'green'],
                                    # size = 'BHK',
                                    hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft'],
                                    zoom=11, height=500, width=1000)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            return st.plotly_chart(fig, use_container_width=False)
        st.sidebar.subheader('pick your budget')
        price_range= st.sidebar.radio('click following button',['1 lakh to 15 lakh ','15 lakh to 30 lakh ','30 lakh to 45 lakh ','45 lakh to 60 lakh ','60 lakh and above ',])


        if price_range == '1 lakh to 15 lakh ':
            get_map(1.0,15.0)
        elif price_range == '15 lakh to 30 lakh ':
            get_map(15.0,30.0)
        elif price_range == '30 lakh to 45 lakh ':
            get_map(30.0,45.0)
        elif price_range ==  '45 lakh to 60 lakh ':
            get_map(45.0,60.0)
        elif price_range == '60 lakh and above ':
            get_map(60.0,208.00)
    except  Exception as e:
        st.write(e)
        pass
house_condition_dict = {1: "new", 0: "old"}
house_type_dict = {1: "Apartment", 0: "Independent house"}
BHK_dict = {1.0: "1", 2.0: "2", 3.0: "3", 4.0: "4", 5.0: "5"}

# (location_dict abridged for brevity – use the full dictionary from your data)
location_dict = {
    55.088: "Canada Corner",
    44.45074394774749: "Chandshi",
    43.991854295812175: "Dwarka",
    # ... add ALL other mappings used in training ...
    # ... add the rest of your mappings here ...
}

# -------------------------------------------------------------------
# 3. Streamlit app
# -------------------------------------------------------------------
def app() -> None:
###############################################################################
# --------------------------- Streamlit App --------------------------------- #
###############################################################################

def app():
    st.title("Nashik Apartment Price Prediction 🏠")

    # Lottie header
    # ------------------------------------------------------------------
    # Intro Lottie animation
    # ------------------------------------------------------------------
    try:
        st_lottie(load_lottiefile("home.json"), speed=1, loop=True, quality="low")
        lottie_coding = load_lottiefile("home.json")
        st_lottie(lottie_coding, speed=1, loop=True, quality="low")
    except FileNotFoundError:
        st.info("home.json animation not found – skipping animation.")
        st.info("home.json animation file not found – skipping animation.")

    # ------------------------------------------------------------------
    # About section
    # ------------------------------------------------------------------
    st.markdown(
        """
        Nashik, the wine capital of India, is growing fast as an affordable
        alternative to Mumbai & Pune. Use this app to estimate apartment prices
        and explore current listings.
        """,
        unsafe_allow_html=True,
        Nashik, the wine capital of India, is quickly becoming a preferred city for
        both investment and retirement living. With soaring real‑estate prices in
        Mumbai and Pune, Nashik offers an attractive alternative. This app helps
        you estimate apartment prices across Nashik and visualise listings by
        budget.
        """
    )

    # ----------------------------------------------------------------
    # User inputs
    # ----------------------------------------------------------------
    st.header("Estimate the price of your dream house ✨")
    # ------------------------------------------------------------------
    # User inputs for prediction
    # ------------------------------------------------------------------
    st.header("Find the price for your dream house ✨")

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
    house_type = st.selectbox("House Type", list(house_type_dict.keys()), format_func=lambda x: house_type_dict[x])
    house_condition = st.selectbox("House Condition", list(house_condition_dict.keys()), format_func=lambda x: house_condition_dict[x])
    BHK = st.selectbox("Number of BHK", list(BHK_dict.keys()), format_func=lambda x: BHK_dict[x])
    total_sqft = st.number_input("Total square‑foot area", min_value=100.0, value=1000.0, step=10.0)
    location = st.selectbox("Location", list(location_dict.keys()), format_func=lambda x: location_dict[x])

    if submitted:
    if st.button("Predict"):
        try:
            features = np.array([[house_type, house_condition, BHK, total_sqft, location]])
            price_lakhs = model.predict(features)[0]
            st.success(f"Estimated price: ₹ {round(price_lakhs, 2)} Lakhs")
            prediction = model.predict(features)[0]
            st.success(f"Estimated price: ₹ {round(prediction, 2)} Lakhs")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

    # ----------------------------------------------------------------
    # Map of listings
    # ----------------------------------------------------------------
    st.header("Explore Nashik listings by budget 💰")
    st.text("(Hover over markers for details)")
    # ------------------------------------------------------------------
    # Interactive map section
    # ------------------------------------------------------------------
    st.header("Explore properties on the Nashik map 💰")
    st.text("(Tip: hover over points for more details)")

    df = get_data.get_data(path="read_data/raw_data.csv")

@@ -118,38 +220,37 @@ def show_map(min_price: float, max_price: float):
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
            hover_data=["owners", "house_condition", "BHK", "price", "per_month_emi", "total_sqft"],
            zoom=11,
            height=500,
            width=1000,
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )
        fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    st.sidebar.subheader("Pick your budget (₹ Lakhs)")
    choice = st.sidebar.radio(
        "", ("1 – 15", "15 – 30", "30 – 45", "45 – 60", "60 and above")
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

    ranges = {
        "1 – 15": (1.0, 15.0),
        "15 – 30": (15.0, 30.0),
        "30 – 45": (30.0, 45.0),
        "45 – 60": (45.0, 60.0),
        "60 and above": (60.0, df["price"].max()),
    }
    show_map(*ranges[choice])
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


# -------------------------------------------------------------------
if __name__ == "__main__":
    app()
