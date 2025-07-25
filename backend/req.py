import requests

url = "https://humble-carnival-r9rwqpp99r9cw7vj-80.app.github.dev/api/users"
response = requests.get(url)

print(response.status_code)  # Код ответа (200, 404 и т.д.)
print(response.json())
