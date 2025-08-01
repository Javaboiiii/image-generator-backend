import socketio

sio = socketio.Client() 

@sio.on('recieve_message')
def on_recieve(data) : 
    print("Data recieved", data); 

@sio.event
def connect(): 
    print("connected to server")

@sio.event
def disconnect():
    print("Disconnected from the server")

try : 
    sio.connect("http://localhost:5000")
    sio.wait() 
except: 
    sio.disconnect
    print("Disconnected"); 
