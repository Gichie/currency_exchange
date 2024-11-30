import requests

url = "http://192.168.1.118:8080/currencies"
data = {
    "name": "Test1",
    "code": "TST1",
    "sign": "Test1£"
}

response = requests.post(url, data=data)

# Печать результата
print("Status Code:", response.status_code)
print("Response:", response.json())