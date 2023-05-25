from chalice import Chalice

app = Chalice(app_name='lambdalicious')

customerQueue = []

API_KEY = '1234'


@app.route('/', methods=['GET'])
def index():
    return {"Current queue":str(customerQueue)}

@app.route('/reset', methods=['DELETE'], api_key_required=True) 
def reset():
    if (API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"}
    
    customerQueue.clear()
    return {"status":"success"}, 204

@app.route('/add/{name}', methods=['PUT'], api_key_required=True)
def add(name):
    if ( API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"}, 401
    
    customerQueue.append(name)
    return {"Added to queue":str(customerQueue)}, 200

@app.route('/remove', methods=['DELETE'], api_key_required=True) 
def remove():
    if ( API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"} , 401
    
    customerQueue.pop(0)
    return {"status":"success"}, 204

@app.route('/notify', methods=['POST'], api_key_required=True)
def notify():
    if ( API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"} , 401
    
    if len(customerQueue) > 0:
        return {"Next in queue":customerQueue[0]}, 200
    return {"Next in queue":"No one in queue"}, 200
    
@app.route('/next', methods=['DELETE'], api_key_required=True)
def next():
    if ( API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"} , 401
    if len(customerQueue) > 0:
        customerQueue.pop(0)
        return {"Next in queue":customerQueue[0]}, 200
    else:
        return {"Next in queue":"No one in queue"}, 200
    
@app.route("/stats")
def stats():
    return {"Queue length":len(customerQueue)}, 200

@app.route('/position/{name}', methods=['GET'])
def position(name):
    if name in customerQueue:
        return {"Position in queue":customerQueue.index(name)}, 200
    else:
        return {"Not in queue"}, 204
