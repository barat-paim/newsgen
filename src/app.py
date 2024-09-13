from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from image_generator import generate_cartoon
import logging
import os

# Create Flask app and set up CORS
app = Flask(__name__, static_folder='../frontend/build')

# Update CORS configuration
CORS(app, resources={r"/api/*": {"origins": ["https://newsgen.onrender.com"]}})

# Set up logging
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.ERROR)
else:
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
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error generating cartoon: {str(e)}")
        return jsonify({"error": "An error occurred while generating the cartoon"}), 500

# Remove the after_request function as CORS is now handled by the Flask-CORS extension

# Run the Flask app
if __name__ == '__main__':
    # Use environment variable to determine if we're in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    app.run(debug=not is_production)