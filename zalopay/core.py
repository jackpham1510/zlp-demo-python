from utils.ngrok import public_url
from utils import GetTimestamp
from config import config
from datetime import datetime
from uuid import uuid4
from utils import http
from zalopay import mac, rsa

import json, base64, urllib.parse

def VerifyCallback(data, requestMac):
  result = {}
  _mac = mac.Compute(data, config['key2'])

  if _mac != requestMac:
    result['returncode'] = -1
    result['returnmessage'] = 'mac not equal'
  else:
    result['returncode'] = 1
    result['returnmessage'] = 'success'
  
  return result

def GenTransID():
  return '{:%y%m%d}_{}_{}'.format(datetime.today(), config['appid'], uuid4())

def NewOrder(params):
  return {
    'amount': params['amount'],
    'description': params['description'],
    'appid': config['appid'],
    'appuser': 'Demo',
    'embeddata': json.dumps({
      'forward_callback': public_url + '/callback',
      'description': params['description']
    }),
    'item': '',
    'apptime': GetTimestamp(),
    'apptransid': GenTransID()
  }

def CreateOrder(params):
  order = NewOrder(params)
  order['mac'] = mac.CreateOrder(order)

  result = http.PostForm(config['api']['createorder'], order)
  result['apptransid'] = order['apptransid']

  return result

def Gateway(params):
  order = NewOrder(params)
  order['mac'] = mac.CreateOrder(order)

  orderJSON = json.dumps(order).encode()
  return config['api']['gateway'] + base64.urlsafe_b64encode(orderJSON).decode()

def QuickPay(params):
  order = NewOrder(params)
  order['userip'] = '127.0.0.1'
  order['paymentcode'] = rsa.encryt_base64(params['paymentcodeRaw'])
  order['mac'] = mac.QuickPay(order, params['paymentcodeRaw'])

  result = http.PostForm(config['api']['quickpay'], order)
  result['apptransid'] = order['apptransid']
  return result

def GetOrderStatus(apptransid):
  params = {
    'appid': config['appid'],
    'apptransid': apptransid
  }

  params['mac'] = mac.GetOrderStatus(params)

  return http.PostForm(config['api']['getorderstatus'], params)

def Refund(params):
  refundReq = {
    'appid': config['appid'],
    'zptransid': params['zptransid'],
    'amount': params['amount'],
    'description': params['description'],
    'timestamp': GetTimestamp(),
    'mrefundid': GenTransID()
  }

  refundReq['mac'] = mac.Refund(refundReq)

  result = http.PostForm(config['api']['refund'], refundReq)
  result['mrefundid'] = refundReq['mrefundid']

  return result

def GetRefundStatus(mrefundid):
  params = {
    'appid': config['appid'],
    'mrefundid': mrefundid,
    'timestamp': GetTimestamp()
  }

  params['mac'] = mac.GetRefundStatus(params)
  
  return http.PostForm(config['api']['getrefundstatus'], params)

def GetBankList():
  params = {
    'appid': config['appid'],
    'reqtime': GetTimestamp()
  }

  params['mac'] = mac.GetBankList(params)

  return http.PostForm(config['api']['getbanklist'], params)