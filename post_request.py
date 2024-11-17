import requests

url = "http://192.168.1.118:8080/data"
data = {"key1": "value1", "key2": "value2"}

response = requests.post(url, json=data)

# Печать ответа от сервера
print("Status code:", response.status_code)  # HTTP статус
print("Response:", response.json())          # Тело ответа (если сервер вернул JSON)