import time

import requests
import json
import jwt
import datetime

# registr = {
#     "username": "test_user",
#     "password": "test_password",
#     "email": "test@email.ru"
# }
#
# response_r = requests.post(url="http://127.0.0.1:80/api/v1/registration", json=registr, headers={'Content-Type': 'application/json'})
#
# print(response_r.status_code)
# print(response_r.text)

# time.sleep(3)
#
#
# login = {
#     "username": "test_user",
#     "password": "test_password"
# }
#
# response_l = requests.post(url="http://127.0.0.1:80/api/v1/login", json=login, headers={'Content-Type': 'application/json'})
#
# print(response_l.status_code)
# print(response_l.text)
#
# access = response_l.json()["token"]
# refresh_token = response_l.json()["refresh_token"]
#
# time.sleep(3)
#
# logout = {
#     "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZTZhMjE0ZTEtNzdiZS00ZWY5LThiYTUtODQ5NTJiYWRhMmU1IiwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQiLCJleHBpcmVzIjoiMjAyMi0wNS0wOVQyMjo0Nzo0NSIsInR5cGUiOiJyZWZyZXNoIn0.hBXEbfHQgozBvIjXM9l6hPoczTyz-sZF8eKp1jiOKWg"
# }
#
# response_logout = requests.post(url="http://127.0.0.1:80/api/v1/logout", json=logout, headers={'Content-Type': 'application/json'})
#
# print(response_logout.status_code)
# print(response_logout.text)
#
#
# time.sleep(3)
#
#
# login = {
#     "username": "test_user",
#     "password": "test_password"
# }
#
# response_l = requests.post(url="http://127.0.0.1:80/api/v1/login", json=login, headers={'Content-Type': 'application/json'})
#
# print(response_l.status_code)
# print(response_l.text)
# #
access = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZTZhMjE0ZTEtNzdiZS00ZWY5LThiYTUtODQ5NTJiYWRhMmU1IiwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQiLCJleHBpcmVzIjoiMjAyMi0wNC0yNlQwMDo0Nzo0NSIsInR5cGUiOiJhY2Nlc3MifQ.esL_TjYT2G0j5X-I9QJOmwxUb_oX5fQ3N5Cha-8Us_Y'

auth_history = {
    "access_token": access
}

response_logout = requests.post(url="http://127.0.0.1:80/api/v1/auth_history", json=auth_history, headers={'Content-Type': 'application/json'})

print(response_logout.status_code)
print(response_logout.text)


