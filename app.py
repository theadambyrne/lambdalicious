from chalice import Chalice

app = Chalice(app_name='lambdalicious')

customerQueue = []

API_KEY = '1234'


@app.route('/', methods=['GET'])
def index():
    return {"Current queue":str(customerQueue)}

@app.route('/reset', methods=['POST']) 
def reset():
    customerQueue.clear()
    return {"Queue reset":str(customerQueue)}

@app.route('/add/{name}', methods=['POST'], api_key_required=True)
def add(name):
    if ( API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"}
    
    customerQueue.append(name)
    return {"Added to queue":str(customerQueue)}

@app.route('/remove', methods=['POST'], api_key_required=True) 
def remove():
    if ( API_KEY != app.current_request.headers['x-api-key'] ):
        return {"Error":"Invalid API key"} 
    
    customerQueue.pop(0)
    return {"Removed from queue":str(customerQueue)}

@app.route('/notify', methods=['POST'])
def notify():
    if len(customerQueue) > 0:
        return {"Next in queue":customerQueue[0]}
    else:
        return {"Next in queue":"No one in queue"}
    
@app.route('/next', methods=['POST'])
def next():
    if len(customerQueue) > 0:
        customerQueue.pop(0)
        return {"Next in queue":customerQueue[0]}
    else:
        return {"Next in queue":"No one in queue"}
    
@app.route("/stats")
def stats():
    return {"Queue length":len(customerQueue)}

@app.route('/position/{name}', methods=['GET'])
def position(name):
    if name in customerQueue:
        return {"Position in queue":customerQueue.index(name)}
    else:
        return {"Position in queue":"Not in queue"}
