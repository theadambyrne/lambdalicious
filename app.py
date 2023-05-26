from chalice import Chalice, Response

app = Chalice(app_name='lambdalicious')

customerQueue = []

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
    return Response(body=str(customerQueue), status_code=200)

@app.route('/reset', methods=['DELETE'], api_key_required=True) 
@check_ak
def reset():
    customerQueue.clear()
    return Response(body="Queue reset", status_code=204)

@app.route('/add/{name}', methods=['PUT'], api_key_required=True)
@check_ak
def add(name):
    customerQueue.append(name)
    return Response(body="Client added", status_code=204)

@app.route('/remove/{name}', methods=['DELETE'], api_key_required=True) 
@check_ak
def remove(name):
    customerQueue.remove(name)
    return Response(body="Client removed", status_code=204)

@app.route('/notify', methods=['POST'], api_key_required=True)
@check_ak
def notify():
    if len(customerQueue) > 0:
        return Response(body=customerQueue[0], status_code=200)
    return Response(body='No one in queue', status_code=204)
    
@app.route('/next', methods=['DELETE'], api_key_required=True)
@check_ak
def next():
    if len(customerQueue) > 0:
        customerQueue.pop(0)
        return Response(body=customerQueue[0], status_code=200)
    return Response(body='No one in queue', status_code=204)
    
@app.route("/stats")
def stats():
    return Response(body=str(len(customerQueue)), status_code=200)

@app.route('/position/{name}', methods=['GET'])
def position(name):
    if name in customerQueue:
        return Response(body=str(customerQueue.index(name)), status_code=200)
    return Response(body='Client not in queue', status_code=204)
