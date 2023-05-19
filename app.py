from chalice import Chalice,  UnauthorizedError

app = Chalice(app_name='lambdalicious')

customerQueue = []

API_KEYS = ['owner_key']

def authorizer(auth_request):
    token = auth_request.token
    if token in API_KEYS:
        return {'principalId': token}
    else:
        raise UnauthorizedError("Invalid API Key")

@app.route('/protected', methods=['GET'], api_key_required=True)
def protected_route():
    auth_result = authorizer({'token': app.current_request.headers.get('x-api-key')})
    return {'message': 'Protected Route'}

@app.route('/')
def index():
    return {"Current queue":str(customerQueue)}

@app.route('/reset', methods=['POST']) 
def reset():
    customerQueue.clear()
    return {"Queue reset":str(customerQueue)}

@app.route('/add/{name}', methods=['POST'])
def add(name):
    customerQueue.append(name)
    return {"Added to queue":str(customerQueue)}

@app.route('/remove', methods=['POST']) 
def remove():
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
