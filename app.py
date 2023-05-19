from chalice import Chalice

app = Chalice(app_name='lambdalicious')

@app.route('/')
def index():
    return {"lambda":"licious"}

@app.route('/{name}')
def hello_name(name):
   return {'hello': name}
