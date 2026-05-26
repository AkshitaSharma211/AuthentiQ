from flask import Flask, render_template ,request, jsonify
from google import genai
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    image = request.files.get('image')

    if not image:
        return jsonify({"error": "No image provided"}), 400


    return jsonify({"message": "Image received"}) 

if __name__ == '__main__':
    app.run(debug=True)