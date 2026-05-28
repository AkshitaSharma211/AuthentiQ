from flask import Flask, request, jsonify, render_template
from google import genai
from dotenv import load_dotenv
import os
import base64

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a luxury goods authentication expert with 20 years of experience.
Analyze the provided image and return exactly this structure:

1. Brand Name: [brand]
2. Exact Product Name and Model: [specific model name]
3. Authenticity Score (X%) with Reasoning: [score and why]
4. Estimated Market Price if Authentic: [price in USD]
5. Estimated Price if Counterfeit: [price in USD]

Be specific and concise. No extra commentary."""

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

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "parts": [
                        {"text": f"Category: {category}\n\n{SYSTEM_PROMPT}"},
                        {"inline_data": {
                            "mime_type": image.mimetype,
                            "data": base64.b64encode(image_bytes).decode()
                        }}
                    ]
                }
            ],
            config={"temperature": 0}
        )
        return jsonify({"message": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)