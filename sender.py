import socketio
import time

sio = socketio.Client() 

sio.connect("http://localhost:5000") 

sio.emit("send_message", {
    "message": "hehe 2"
})

time.sleep(1)

sio.disconnect()
