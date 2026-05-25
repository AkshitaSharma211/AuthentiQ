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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # You can add image processing here, e.g., send to Gemini, etc.
            return render_template('index.html', message=f'Image {filename} uploaded successfully!')
        else:
            return render_template('index.html', error='Invalid file type')
    # GET request
    return render_template('index.html')

@app.route('/api/echo', methods=['GET'])
def api_echo():
	"""Simple GET API that echoes a `msg` query parameter as JSON.

	Example: GET /api/echo?msg=hello
	"""
	msg = request.args.get('msg', '')
	return jsonify({'echo': msg})

if __name__ == '__main__':
	app.run(debug=True)