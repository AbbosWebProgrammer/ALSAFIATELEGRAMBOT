import requests
import json
from django.conf import settings
from random import choice

def sendphonepassword(phone,password):
  if len(phone)!=12:
    phone=phone[1:]
  url = "http://notify.eskiz.uz/api/message/sms/send"
  payload={'mobile_phone': f'{phone}',
  'message': f'{password}',
  'from': '4546',
  'callback_url': 'http://0000.uz/test.php'}
  files=[ ]
  headers = {
  'Authorization': f'''Bearer {settings.SMSTOKEN}'''
  }
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  dic = json.loads(f'''{response.text}''')
  if dic['message']=="Token has expired":
      refresh()
      sendphonepassword(phone,password)
  return response.text

def refresh():
  url = "http://notify.eskiz.uz/api/auth/login"
  payload={'email': 'atadjitdinov@gmail.com',
  'password': '4RQ2lCrYGYxhZkFmGL2snlcLlPGCY9bg8fW3wydE'}
  files=[]
  headers = {}
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  dic = json.loads(f'''{response.text}''')
  if 'data' in dic.keys() and 'data' in dic['data'].keys():
      settings.SMSTOKEN=dic['data']['token']


# url = "http://notify.eskiz.uz/api/message/sms/send"
# payload={'mobile_phone': f'998907185835',
# 'message': f'Kod: 56545',
# 'from': '4546',
# 'callback_url': 'http://0000.uz/test.php'}
# files=[ ]
# headers = {
# 'Authorization': 'Bearer '
# }
# response = requests.request("POST", url, headers=headers, data=payload, files=files)