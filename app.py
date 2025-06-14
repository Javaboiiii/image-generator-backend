from flask import Flask, request
from google import genai
from google.genai import types
from flask_cors import CORS 

app = Flask(__name__) 
CORS(app)

# Gemini configuration
client = genai.Client(api_key="AIzaSyDqqQhZZt4PkstxS_t7noqcwxUZVOV2gKc")


@app.route('/api/generate_image', methods = ['POST'])  
def generate_image() : 
  print("Executed the POST request")
  try :    
    data = request.get_json() 
    print("Received request with data:", data)

    contents = (f"{data['content']}") 
    print("Generating image with prompt:", contents)
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
    print("Successfully generated image")
    return result
  except Exception as e : 
    print("Error generating image:", e)
    return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)