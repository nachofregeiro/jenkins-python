print("Downloading report...")

import requests

url = 'http://httpbin.org/response-headers?language=Python'
response = requests.get(url, allow_redirects=True)
open('response.txt', 'wb').write(response.content)
