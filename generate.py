print("Downloading report...")

import requests
from datetime import datetime
from ftplib import FTP 

url = 'http://httpbin.org/response-headers?language=Python'
response = requests.get(url, allow_redirects=True)
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
fileName = 'response_{}.txt'.format(date)
open(fileName, 'wb').write(response.content)
 
print(fileName)

ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('ftp.dlptest.com', 21) 
ftp.login('dlpuser', 'rNrKYTX9g7z3RgJRmxWuGHbeu')

fp = open(fileName, 'rb')
ftp.storbinary('STOR %s' % fileName, fp, 1024)
fp.close()
