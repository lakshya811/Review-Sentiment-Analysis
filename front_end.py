# -------------------------------------------------------------
# Module -: front_end
# Desc -: Contains front end UI for the sentiment analyzer app
# -------------------------------------------------------------


# Importing all the required libraries
import streamlit as st
from dotenv import load_dotenv
from logger import MyLogger

# Setting up page configuration
st.set_page_config(page_title="Review Sentiment of a Review-app", layout="centered",initial_sidebar_state= "expanded")
