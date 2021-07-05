print("Downloading report...")

import requests
from datetime import datetime

url = 'http://httpbin.org/response-headers?language=Python'
response = requests.get(url, allow_redirects=True)
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
open('response.txt', 'wb').write(response.content)
