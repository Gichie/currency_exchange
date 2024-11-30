import requests

url = "http://192.168.1.118:8080/exchangeRate/USDRUB"
data = {"rate": 148}

try:
    response = requests.patch(url, data=data)
    response.raise_for_status()  # Проверка на ошибки HTTP
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.HTTPError as err:
    print("HTTP error occurred:", err)
except Exception as e:
    print("An error occurred:", e)
