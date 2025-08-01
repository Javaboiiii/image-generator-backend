import eventlet
eventlet.monkey_patch()
from flask import Flask, request, logging, render_template
from flask_socketio import SocketIO
from google import genai
from google.genai import types
from flask_cors import CORS 
from socket_server import sio
import socketio
import eventlet.wsgi
import logging

# Configure eventlet to work better with concurrent connections

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

flask_app = Flask(__name__) 
CORS(flask_app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app = socketio.WSGIApp(socketio_app=sio, wsgi_app=flask_app)

# Gemini configuration
client = genai.Client(api_key="AIzaSyDqqQhZZt4PkstxS_t7noqcwxUZVOV2gKc")

@flask_app.route("/chat", methods=["GET"])
def chat() : 
   return render_template('index.html')

@flask_app.route("/", methods=["GET"])
def home() : 
   return "<h1> Image Generator API </h1>"


@flask_app.route('/api/generate_image', methods = ['POST'])  
def generate_image() : 
  try :    
    data = request.get_json() 
    

    contents = (f"{data['content']}") 
    
    response = client.models.generate_content(
      model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
          response_modalities=['TEXT', 'IMAGE'],
          safety_settings=[
            {
              "category": "HARM_CATEGORY_HARASSMENT",
              "threshold": "BLOCK_NONE"
            },
            {
              "category": "HARM_CATEGORY_HATE_SPEECH",
              "threshold": "BLOCK_NONE"
            },
            {
              "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              "threshold": "BLOCK_NONE"
            },
            {
              "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
              "threshold": "BLOCK_NONE"
            }
          ]
        )
    )
      # Return the JSON response
    result = response.model_dump_json()
    return result
  except Exception as e : 
    return {"error": str(e)}, 500


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)