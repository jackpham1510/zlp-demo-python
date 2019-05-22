import hmac, hashlib
from config import config

def Compute(data, key):
  return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

def _compute(data):
  return Compute(data, config['key1'])

def _createOrderMacData(order):
  return "{}|{}|{}|{}|{}|{}|{}".format(order['appid'], order['apptransid'], order['appuser'], order['amount'], order['apptime'], order['embeddata'], order['item'])

def CreateOrder(order):
  return _compute(_createOrderMacData(order))

def QuickPay(order, paymentcodeRaw):
  return _compute(_createOrderMacData(order) +"|"+ paymentcodeRaw)

def Refund(params):
  return _compute("{}|{}|{}|{}|{}".format(params['appid'], params['zptransid'], params['amount'], params['description'], params['timestamp']))

def GetOrderStatus(params):
  return _compute("{}|{}|{}".format(params['appid'], params['apptransid'], config['key1']))

def GetRefundStatus(params):
  return _compute("{}|{}|{}".format(params['appid'], params['mrefundid'], params['timestamp']))

def GetBankList(params):
  return _compute("{}|{}".format(params['appid'], params['reqtime']))