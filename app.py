import streamlit as st

# Custom imports
from multipage import MultiPage
import prediction,EDA1, EDA2 , feature_engineering,feature_selection,model_building,About # import your pages here
try:
# Create an instance of the app
    app = MultiPage()

    # Title of the main page


    # Add all your applications (pages) here
    app.add_page("Home",prediction.app)
    app.add_page("EDA1",EDA1.app)
    app.add_page("EDA2", EDA2.app)
    app.add_page("Feature Engineering", feature_engineering.app)
    app.add_page("Feature selection",feature_selection.app)
    app.add_page("Model Building",model_building.app)
    app.add_page("About",About.app)
    #app.add_page("Machine Learning", machine_learning.app)
    #app.add_page("Data Analysis",data_visualize.app)
    #app.add_page("Y-Parameter Optimization",redundant.app)

    # The main app
    app.run()
except Exception as e:
    st.write(e)
    pass
