from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from image_generator_2 import generate_cartoon  
import os
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "supports_credentials": True}})

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/generate_cartoon', methods=['GET', 'POST', 'OPTIONS'])
def generate_cartoon_route():
    app.logger.debug(f"Received {request.method} request to /api/generate_cartoon")
    app.logger.debug(f"Request headers: {request.headers}")
    app.logger.debug(f"Request body: {request.get_data()}")

    if request.method == 'OPTIONS':
        # Handles preflight requests
        headers = {
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    if request.method == 'GET':
        # Handle GET request (for testing purposes)
        return jsonify({"message": "GET request received. Use POST to generate a cartoon."}), 200

    # POST request handling
    try:
        article_text = request.json['article_text']
        result = generate_cartoon(article_text)
        app.logger.debug(f"Generated result: {result}")
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    except Exception as e:
        app.logger.error(f"Error generating cartoon: {str(e)}")
        error_response = jsonify({"error": str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        error_response.headers.add('Access-Control-Allow-Credentials', 'true')
        return error_response, 500

if __name__ == '__main__':
    app.run(debug=True)



# changes made: version 2
# 1. added static_folder and static_url_path to the Flask app initialization
# 2. modified the index route to serve the index.html file from the frontend build directory
# 3. added a new route for generating cartoons
# 4. updated the package.json file to include the necessary resolutions for serve-static and send