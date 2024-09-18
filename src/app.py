from flask import Flask, request, jsonify, send_from_directory, make_response, current_app
from flask_cors import CORS
from image_generator import generate_cartoon
import logging
import os
from datetime import datetime, timedelta

# Create Flask app and set up CORS
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
app.root_path = os.path.dirname(os.path.abspath(__file__))

# Set up CORS for all routes
CORS(app)

# Set up logging
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.ERROR)
else:
    logging.basicConfig(level=logging.DEBUG)

# Route to serve images (Place this route before the catch-all route)
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'images'), filename)

# API route for generating cartoons
@app.route('/api/generate_cartoon', methods=['POST', 'OPTIONS'])
def generate_cartoon_route():
    if request.method == 'OPTIONS':
        # Handles preflight requests
        return ('', 204)

    # POST request handling to generate cartoons
    try:
        article_text = request.json.get('article_text', '')
        if not article_text:
            return jsonify({"error": "No article text provided"}), 400

        result = generate_cartoon(article_text, app)
        # Make sure 'image_url' and 'caption' keys are present in the result
        if 'image_url' not in result or 'caption' not in result:
            return jsonify({"error": "Invalid response from image generator"}), 500
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error generating cartoon: {str(e)}")
        return jsonify({"error": "An error occurred while generating the cartoon"}), 500

# Serve the frontend build (React app)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        response = make_response(send_from_directory(app.static_folder, path))
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Run the Flask app
if __name__ == '__main__':
    # Use environment variable to determine if we're in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    app.run(debug=not is_production)