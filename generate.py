print("Downloading report...")

import requests
import sys
from datetime import datetime
from ftplib import FTP

print("Argument List:", str(sys.argv))

ftpServer = 'ftp.dlptest.com'
ftpUser = 'dlpuser'
ftpPassword = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

if len(sys.argv) >= 4:
    print("Using FTP credentials from args")
    ftpServer = sys.argv[1]
    ftpUser = sys.argv[2]
    ftpPassword = sys.argv[3]

url = 'http://httpbin.org/response-headers?language=Python'
response = requests.get(url, allow_redirects=True)
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
fileName = 'response_{}.txt'.format(date)
open(fileName, 'wb').write(response.content)
 
print(fileName)

ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect(ftpServer, 21) 
ftp.login(ftpUser, ftpPassword)

fp = open(fileName, 'rb')
ftp.storbinary('STOR %s' % fileName, fp, 1024)
fp.close()
