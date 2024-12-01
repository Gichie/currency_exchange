import requests

url = "http://192.168.1.118:8080/exchangeRates"
data = {
    "baseCurrencyCode": "EUR",
    "targetCurrencyCode": "USD",
    "rate": 148
}

response = requests.post(url, data=data)

# Печать результата
print("Status Code:", response.status_code)
print("Response:", response.json())