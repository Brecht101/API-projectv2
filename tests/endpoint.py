import json
import requests

headers = {
"accept": "application/json",
"Content-Type": "application/x-www-form-urlencoded"
}

request_data = {
    "client_id": "",
    "client_secret": "",
    "scope": "",
    "grant_type": "",
    "refresh_token": "",
    "username": "test@test.net",
    "password": "test"
}

tokenrequest = requests.post("http://localhost:8000/token", data=request_data, headers=headers)
# Printing the information for debugging and illustration purposes
print(tokenrequest.text)
# Extracting the token that came with the response
token = json.loads(tokenrequest.text)['access_token']

# Using the token in the headers of a secured endpoint
headerswithtoken = {
"accept" : "application/json",
"Authorization": f'Bearer {token}'
}

getrequest = requests.get("http://localhost:8000/users", headers=headerswithtoken)

# Printing the information for debugging and illustration purposes
print(getrequest .text)