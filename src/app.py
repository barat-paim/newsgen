from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from image_generator_2 import generate_cartoon
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        article_text = request.json['article_text']
        result = generate_cartoon(article_text)
        return jsonify(result)
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True)

print("This line should not be reached if the app is running correctly.")