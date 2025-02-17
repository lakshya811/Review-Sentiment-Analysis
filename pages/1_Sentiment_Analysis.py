
import requests
import streamlit as st
import time
import random
from dotenv import load_dotenv
from logger import MyLogger
st.set_page_config(page_title="Sentiment Analyze", layout="centered")
# Setting the title of the Page
# st.title("Sentiment Analyzer")
# Provide navigation back to the main page or other pages

st.write("Analyze sentiment of user reviews")

# Setting up the sidebar
# Initiating logger
logger = MyLogger.get_logger(__name__)

# Storing App URL in a variable
API_URL = "http://127.0.0.1:8080/reviews"
logger.info(
            f"Api URL stored: {API_URL}"
        )
# Loading the environment
load_dotenv()

# Headers for the authentication
headers = {
    'Authorization': 'Bearer 1234' ,
    'Content-Type': 'application/json'
}

# Input for the request
user_id= str(st.text_input("Enter the desired user id"))
# Button to sent the request to the model
random_request_id= random.randint(1,545445)
request_id= str(random_request_id)
review= {"review_text": str(st.text_input("Enter your review"))}
logger.info(
            f"User request for the sentiment analysis{review, user_id}"
        )

if st.button("Sentiment Analyze"):
        start_time= time.perf_counter()
        logger.info(
                f"Program starts now: {start_time}"
        )
        if user_id is not None and review is not None:
            try:
                payload={"request_id" :request_id,
                    "user_id":user_id,
                    "data": review}
                response = requests.post(API_URL, json= payload
                ,headers=headers)
                logger.info(
                f"this the json response generated by the api: {response}"
            )
                # printing the response on the streamlit page
                if response.status_code == 200 :
                    response_data = response.json()
                    if "error" in response_data:
                        st.error(response_data["error"])
                    else: 
                        sentiment_response= response.json()['data']
                        st.header(f'Analysis for the review ')
                        st.write(f"The sentiment is : {sentiment_response['sentiment']}")
                        st.write(f"The score is: {sentiment_response['confidence']}")
                        logger.info(
                f"this the json response for the data generated by the api: {sentiment_response}"
            )
                if response.status_code == 200:
                    response_data= response.json()
                else:
                    st.error(f"Request failed with status code {response.status_code}")

            except Exception as e:
                st.error(f"an error occured : {e}")
        else:
            st.warning("please enter a message")
