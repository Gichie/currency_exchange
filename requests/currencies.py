import requests

url = "http://192.168.1.118:8080/currencies"
data = {
    "name": "Test2",
    "code": "TST2",
    "sign": "Test2£"
}

response = requests.post(url, data=data)

# Печать результата
print("Status Code:", response.status_code)
print("Response:", response.json())