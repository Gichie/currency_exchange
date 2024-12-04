import requests

url = "http://192.168.1.118:8080/exchangeRate/EURAUD"
data = {"rate": 1.63}

response = requests.patch(url, data=data)

if response.headers.get('Content-Type') == 'application/json':
    print(f"Response JSON: {response.json()}")
else:
    print(f"Response Text: {response.text}")
