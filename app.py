from chalice import Chalice, Response
import boto3

app = Chalice(app_name='lambdalicious')

class DynamoDBConfig:
    TABLE_NAME = 'QueueManagement'
    READ_CAPACITY_UNITS = 5
    WRITE_CAPACITY_UNITS = 5

dynamodb = None
customerQueueTable = None

def initialize_dynamodb(config):
    global dynamodb, customerQueueTable
    dynamodb = boto3.resource('dynamodb')
    customerQueueTable = dynamodb.Table(config.TABLE_NAME)

def get_customer_queue():
    response = customerQueueTable.get_item(Key={'index': 1})
    item = response.get('Item')
    if item:
        return item.get('queue', [])
    else:
        return []

def update_customer_queue(queue):
    customerQueueTable.put_item(Item={'index': 1, 'queue': queue})

def pop_customer_queue():
    customer_queue = get_customer_queue()
    if len(customer_queue) > 0:
        customer = customer_queue.pop(0)
        update_customer_queue(customer_queue)
        return customer
    else:
        return None

def initialize_customer_queue():
    update_customer_queue([])

API_KEYS = ['1234']

def check_ak(func):
    def wrapper(*args, **kwargs):
        api_key = app.current_request.headers.get('x-api-key')
        if api_key not in API_KEYS:
            return Response('Invalid API key', status_code=401)
        return func(*args, **kwargs)
    return wrapper

@app.route('/', methods=['GET'])
def index():
    customer_queue = get_customer_queue()
    return Response(body=str(customer_queue), status_code=200)

@app.route('/reset', methods=['DELETE'], api_key_required=True)
@check_ak
def reset():
    initialize_customer_queue()
    return Response(body="Queue reset", status_code=204)

@app.route('/add/{name}', methods=['PUT'], api_key_required=True)
@check_ak
def add(name):
    customer_queue = get_customer_queue()
    customer_queue.append(name)
    update_customer_queue(customer_queue)
    return Response(body="Client added", status_code=204)

@app.route('/remove/{name}', methods=['DELETE'], api_key_required=True)
@check_ak
def remove(name):
    customer_queue = get_customer_queue()
    if name in customer_queue:
        customer_queue.remove(name)
        update_customer_queue(customer_queue)
        return Response(body="Client removed", status_code=204)
    else:
        return Response(body="Client not in queue", status_code=204)

@app.route('/notify', methods=['POST'], api_key_required=True)
@check_ak
def notify():
    customer_queue = get_customer_queue()
    if len(customer_queue) > 0:
        customer = customer_queue[0]
        return Response(body=customer, status_code=200)
    else:
        return Response(body="No one in queue", status_code=204)
    
@app.route('/next', methods=['DELETE'], api_key_required=True)
@check_ak
def next():
    if len(get_customer_queue()) > 0:
        pop_customer_queue()
        return Response(body=get_customer_queue()[0], status_code=200)
    return Response(body='No one in queue', status_code=204)

@app.route("/stats")
def stats():
    return Response(body=str(len(get_customer_queue())), status_code=200)

@app.route('/position/{name}', methods=['GET'])
def position(name):
    if name in get_customer_queue():
        return Response(body=str(get_customer_queue().index(name)), status_code=200)
    return Response(body='Client not in queue', status_code=204)

initialize_dynamodb(DynamoDBConfig())



    

    



