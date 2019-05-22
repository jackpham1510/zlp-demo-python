from models.order import Order
import json

ORDER_PER_PAGE = 10

def SaveOrder(data):
  embeddata = json.loads(data['embeddata'])
  Order.create(apptransid=data['apptransid'], zptransid=data['zptransid'], channel=data['channel'], timestamp=data['servertime'], amount=data['amount'], description=embeddata['description'])

def Paginate(page):
  orders = [order for order in Order.select().order_by(Order.timestamp.desc()).paginate(page, ORDER_PER_PAGE).dicts()]
  totalOrder = Order.select().count()

  return {
    'currentPage': page,
    'totalOrder': totalOrder,
    'orders': orders,
    'orderPerPage': ORDER_PER_PAGE
  }