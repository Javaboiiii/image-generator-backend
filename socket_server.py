import socketio

# Configure server with CORS support
sio = socketio.Server(
    cors_allowed_origins='*'
) 


@sio.event
def send_message(sid, data): 
    id = data["id"]; 
    print("sending data to", id); 
    sio.emit("recieve_message", data["message"], skip_sid=sid) 


@sio.event
def connect(sid, data): 
    print("connected", sid)


@sio.event
def disconnect(sid, reason): 
    print("disconnected", sid, reason)
