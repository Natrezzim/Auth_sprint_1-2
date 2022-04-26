import datetime
import json

import jwt
import requests

# registr = {
#     "username": "test_user",
#     "password": "test_password",
#     "email": "test@email.ru"
# }
#
# registr_j = json.dumps(registr)
#
# response = requests.post(url="http://127.0.0.1:80/api/v1/registration", json=registr, headers={'Content-Type': 'application/json'})
#
# print(response.status_code)
# print(response.text)

expires_delta = datetime.timedelta(hours=2)


current_time = datetime.datetime.now()
expiries_time = current_time + expires_delta

a = expiries_time.strftime("%Y-%m-%dT%H:%M:%S")

b = datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%S")

print(b)
print(a)

