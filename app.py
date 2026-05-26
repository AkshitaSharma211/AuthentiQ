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
    category = request.form.get('category', 'accessories')

    if not image:
        return jsonify({"error": "No image provided"}), 400

    image_bytes = image.read()
    prompt = f"""You are a luxury goods authentication expert. Analyze this {category} image and provide:
1. Brand name
2. Exact product name and model  
3. Authenticity score (0-100%) with reasoning
4. Estimated market price if authentic
5. Estimated price if counterfeit

Be specific and professional. Format your response clearly."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": image.mimetype, "data": __import__('base64').b64encode(image_bytes).decode()}}
                ]
            }
        ]
    )

    return jsonify({"message": response.text}) 

if __name__ == '__main__':
    app.run(debug=True)