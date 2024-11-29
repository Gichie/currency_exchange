import requests

url = "http://192.168.1.118:8080/currencies"
data = {
    "name": "British Pound",
    "code": "GBP",
    "sign": "£"
}

response = requests.post(url, data=data)

# Печать результата
print("Status Code:", response.status_code)
print("Response:", response.json())