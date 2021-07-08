import argparse
import csv
import pysftp
import requests
from datetime import date

stage_url = 'https://{}-stage.civitaslearning.com'
prod_url = 'https://{}.civitaslearning.com'
# base_url = 'http://localhost:3000'

auth = '/auth/login'
students = '/api/illume/current_students.csv'
courses = '/api/course-insights/insights/gIndividualImpact/export.csv?limit=1000'

def get_data(customer, env, product, username, password):
  url = ''
  if env == 'stage':
    url = stage_url.format(customer)
  else:
    url = prod_url.format(customer)
  creds = {
    'username': username,
    'password': password
  }
  resp = None
  with requests.Session() as session:
    print('Authenticating')
    session.get(url + auth)
    session.post(url + auth, data=creds)
    auth_resp = session.get(url + auth)
    
    print('Gathering data')
    if product == 'illume':
      req_body = { 
        '_csrf': auth_resp.cookies['csrfToken'],
        'request':
        '{"show_unenrolled_students":false,"addCols":["first_term"],"sort":{"col":"last_name","dir":"asc"},"feature_filters":[],"completionWindows":[{"key":"normal","value":3}]}'
        }
      resp = session.post(url + students, cookies=auth_resp.cookies, headers={'x-csrf-token': auth_resp.cookies['csrfToken']}, data=req_body)
    else:
      resp = session.get(url + courses, cookies=auth_resp.cookies, headers={'x-csrf-token': auth_resp.cookies['csrfToken']})
    
    if resp and resp.text:
      return resp.text.split('\n')

def format_data(data, delimiter='!~'):
  print('Formatting data')
  if data is None or len(data) == 0:
    return
  csv_data = []
  header_line = -1
  for c in data:
    if len(c.split()) > 1:
      header_line = data.index(c)
      break
  if (header_line >= 0):
    boilerplate = data[0:header_line]
    for row in data[header_line:-1]:
      csv_data.append(tuple(e.encode('utf-8') for e in row.split(',')))
  
  formatted_data = []
  for b in boilerplate:
    formatted_data.append(b)
  for c in csv_data:
    formatted_data.append(delimiter.join(map(decode, c)) + '\n')
    
  return formatted_data

def decode(c):
  return c.decode('utf-8')

def write_data(data, filestub):
  if data is None or len(data) == 0:
    print('No data to write')
    return
  today = date.today()
  filename = '{}_{}.txt'.format(filestub, today.strftime('%Y%m%d'))

  with open(filename, 'w') as outfile:
    print('Writing data to {}'.format(filename))
    for d in data:
      outfile.write(d)
  
  return filename

def send_to_sftp(ftpServer, ftpUser, ftpPassword, filename):
  print("Send data over FTP")

  if filename is None:
    print('Send to FTP: File name is empty')
    return
  
  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None

  with pysftp.Connection(host=ftpServer, username=ftpUser, password=ftpPassword, private_key=".ppk", cnopts=cnopts) as sftp:
    sftp.cwd('/CIVITAS_USAGE')
    sftp.put(filename)

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser()
  parser.add_argument('env', help='Environment.',
                      type=str,
                      choices=('stage', 'prod'))
  parser.add_argument('customer', help='Customer whose data you want to pull',
                      type=str)
  parser.add_argument('product_name', help='The product from which to pull data',
                      type=str,
                      choices=('illume', 'courses'))
  parser.add_argument('username', help='Username for basic auth account on customer illume site',
                      type=str)
  parser.add_argument('password', help='Password for basic auth account on customer illume site',
                      type=str)
  parser.add_argument('ftp_server', help='FTP server url',
                      type=str)
  parser.add_argument('ftp_user', help='FTP user name',
                      type=str)
  parser.add_argument('ftp_password', help='FTP user password',
                      type=str)

  args = parser.parse_args()

  data = get_data(args.customer, args.env, args.product_name, args.username, args.password)
  
  formatted_data = format_data(data)
  
  filename = None
  if args.product_name == 'illume':
    filename = write_data(formatted_data, 'illume_daily_file')
  else:
    filename = write_data(formatted_data, 'illume_courses_daily_file')
  
  send_to_sftp(args.ftp_server, args.ftp_user, args.ftp_password, filename)
