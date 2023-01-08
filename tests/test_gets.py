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

def test_get_users():
    response = requests.get('http://127.0.0.1:8000/users', headers=headerswithtoken)
    assert response.status_code == 200
    response_dictionary = response.json()
    for item in response_dictionary:
        assert item is not None
    
def test_get_orders():
    response = requests.get('http://127.0.0.1:8000/orders', headers=headerswithtoken)
    assert response.status_code == 200
    response_dictionary = response.json()
    for item in response_dictionary:
        assert item is not None
        
def test_get_warehouses():
    response = requests.get('http://127.0.0.1:8000/warehouses', headers=headerswithtoken)
    assert response.status_code == 200
    response_dictionary = response.json()
    for item in response_dictionary:
        assert item is not None

def test_get_user():
    bad = requests.get('http://127.0.0.1:8000/user?id=ABB', headers=headerswithtoken)
    assert bad.status_code != 200
    good = requests.get('http://127.0.0.1:8000/user?id=1', headers=headerswithtoken)
    assert good.status_code == 200
    dict = good.json()
    assert type(dict["customerID"]) == int
    