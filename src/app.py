from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from image_generator import generate_cartoon
import logging
import os
# Create Flask app and set up CORS
app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Serve the frontend build (React app)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API route for generating cartoons
@app.route('/api/generate_cartoon', methods=['POST', 'OPTIONS'])
def generate_cartoon_route():
    app.logger.debug(f"Received {request.method} request to /api/generate_cartoon")
    app.logger.debug(f"Request headers: {request.headers}")
    app.logger.debug(f"Request body: {request.get_data()}")

    if request.method == 'OPTIONS':
        # Handles preflight requests
        return ('', 204)

    # POST request handling to generate cartoons
    try:
        article_text = request.json.get('article_text', '')
        if not article_text:
            return jsonify({"error": "No article text provided"}), 400

        # Call the generate_cartoon function from image_generator.py
        result = generate_cartoon(article_text)
        app.logger.debug(f"Generated result: {result}")
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error generating cartoon: {str(e)}")
        return jsonify({"error": str(e)}), 500

# CORS configuration for frontend access
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ["http://localhost:3000", "http://127.0.0.1:3000"]:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)