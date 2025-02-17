import requests
# from fastapi_app import SECRET_KEY
# import os
# from dotenv import load_dotenv
# bearer_token = MY_VERY_SECRET_TOKEN

# headers = {"Authorization": f"Bearer {bearer_token}"}
# API_URL = "http://127.0.0.1:8080/docs"

# response = requests.get(API_URL,headers=headers)




url = "http://127.0.0.1:8080/reviews"
headers = {
    'Authorization': 'Bearer 1234',
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers)
print(response.json())