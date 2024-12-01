import requests

url = "http://192.168.1.118:8080/exchangeRate/USDEUR"
data = {"rate": "1.3"}

response = requests.patch(url, data=data)

if response.headers.get('Content-Type') == 'application/json':
    print(f"Response JSON: {response.json()}")
else:
    print(f"Response Text: {response.text}")
