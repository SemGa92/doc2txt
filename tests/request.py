import os
import base64
import dotenv
import json
import jwt
import requests
import time

dotenv.load_dotenv()


def get_token():
    now = int(time.time())
    to_encode = {
        "nbf" : now, # NOT BEFORE - WHEN THIS TOKEN IS CONSIDERED VALID
        "exp" : now + 1800, # EXPIRY - 1/2 HR (1800 SECS) FROM NOW IN THIS EXAMPLE
    }
    return jwt.encode(to_encode, JWT_KEY, algorithm=JWT_ALGO)


JWT_KEY = os.getenv('JWT_KEY')
JWT_ALGO = 'HS512'
url = os.getenv('DOC2TXT_URL')

headers = {
    'Authorization': f'Bearer {get_token()}',
    'Content-type': 'application/json'
}

f_name = 'test.pdf'

with open(f_name, "rb") as f:
    doc = base64.b64encode(f.read()).decode("utf-8")

payload = {
    'source': 'locale',
    'f_name': f_name,
    'content': doc,
}

response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

if response.status_code == 200:
    print(response.json())
else:
    print(response.status_code)
    print(response.json())