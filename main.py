from flask import Flask, request, jsonify
from respository import OrderRepository
from flask_sockets import Sockets
from flask_cors import CORS
import zalopay.core
import json

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)
CORS(app)
hub = {}

@app.before_request
def log_request():
  data = request.args
  if request.method == 'POST':
    data = request.get_data()
  app.logger.debug('[{}][{}] {}'.format(request.method, request.url, data))

@sockets.route('/subscribe')
def subscribe(ws):
  apptransid = request.args.get('apptransid')
  hub[apptransid] = ws
  while not ws.closed:
    ws.receive()
  hub.pop(apptransid)

@app.route('/callback', methods=['POST'])
def callback():
  dataStr = request.json['data']
  requestMac = request.json['mac']
  result = zalopay.core.VerifyCallback(dataStr, requestMac)

  if result['returncode'] != -1:
    data = json.loads(dataStr)
    OrderRepository.SaveOrder(data)
    apptransid = data['apptransid']
    ws = hub.get(apptransid)
    if not ws == None:
      if not ws.closed:
        ws.send(dataStr)
        ws.close()

  return jsonify(result)

@app.route('/api/createorder', methods=['POST'])
def createorder():
  params = request.json
  ordertype = request.args.get('ordertype')

  result = None
  if ordertype == 'gateway':
    result = zalopay.core.Gateway(params)
  elif ordertype == 'quickpay':
    result = zalopay.core.QuickPay(params)
  else:
    result = zalopay.core.CreateOrder(params)

  return jsonify(result)

@app.route('/api/refund', methods=['POST'])
def refund():
  return jsonify(zalopay.core.Refund(request.json))

@app.route('/api/getrefundstatus', methods=['GET'])
def getrefundstatus():
  mrefundid = request.args.get('mrefundid')
  return jsonify(zalopay.core.GetRefundStatus(mrefundid))

@app.route('/api/getbanklist', methods=['GET'])
def getbanklist():
  return jsonify(zalopay.core.GetBankList())

@app.route('/api/gethistory', methods=['GET'])
def gethistory():
  page = request.args.get('page')
  try:
    page = int(page)
  except:
    page = 1

  return jsonify(OrderRepository.Paginate(page))

if __name__ == "__main__":
  from gevent import pywsgi
  from geventwebsocket.handler import WebSocketHandler

  PORT = 1789
  print('list at port :%d' % PORT)
  server = pywsgi.WSGIServer(('', PORT), app, log=app.logger, handler_class=WebSocketHandler)
  server.serve_forever()