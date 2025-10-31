"""
Hugging Face Spaces Deployment
Simple web app to serve the TinyMLP model

Features:
- Model loading from models/tiny_mlp.pth
- Simple web interface
- Fast inference (< 3 seconds cold start)
"""

import torch
import numpy as np
from flask import Flask, request, jsonify, render_template_string
import os
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)

# Global pipeline variables (loaded once)
tokenizer = None
model = None
device = torch.device('cpu')

def load_pipeline():
    """Load model and tokenizer once at startup"""
    global tokenizer, model
    if tokenizer is None or model is None:
        model_path = "models/sentiment-model"
        if os.path.exists(model_path):
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            model.to(device)
            model.eval()
            print(f"✅ Pipeline loaded from: {model_path}")
        else:
            print(f"❌ Model directory not found: {model_path}")
            # As a fallback, try to download the model if it's not present locally
            from scripts.download_model import download_model
            download_model()
            load_pipeline() # Retry loading after download

@app.route('/')
def home():
    """Simple web interface"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment Analysis - Lightweight ML</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .box { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
            textarea { width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc; min-height: 80px; }
            button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #2980b9; }
            #result { margin-top: 20px; padding: 10px; display: none; }
        </style>
    </head>
    <body>
        <h1>🧠 Sentiment Analysis with Transformers</h1>
        <div class="box">
            <h3>About the Model</h3>
            <p>Model: <strong>distilbert-base-uncased-finetuned-sst-2-english</strong></p>
            <p>This is a lightweight and fast model for sentiment analysis.</p>
        </div>

        <div class="box">
            <h3>Analyze Text</h3>
            <textarea id="text-input" placeholder="Enter some text to analyze..."></textarea>
            <br><br>
            <button onclick="analyze()">Analyze Sentiment</button>
            <div id="result"></div>
        </div>

        <script>
            async function analyze() {
                const textInput = document.getElementById('text-input').value;
                if (!textInput) {
                    alert('Please enter some text to analyze.');
                    return;
                }

                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '⏳ Analyzing...';

                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ text: textInput })
                    });
                    const data = await response.json();
                    resultDiv.innerHTML = `
                        <h4>Analysis Result</h4>
                        <p><strong>Sentiment:</strong> ${data.prediction}</p>
                        <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
                        <p><strong>Response time:</strong> ${data.inference_time_ms}ms</p>
                    `;
                } catch (error) {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${error}</p>`;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for sentiment analysis"""
    if tokenizer is None or model is None:
        load_pipeline()

    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    start_time = time.time()

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the prediction and confidence
    probabilities = torch.softmax(outputs.logits, dim=1)
    confidence, predicted_class_idx = torch.max(probabilities, dim=1)
    predicted_class = model.config.id2label[predicted_class_idx.item()]

    inference_time = int((time.time() - start_time) * 1000)

    return jsonify({
        'prediction': predicted_class,
        'confidence': confidence.item(),
        'inference_time_ms': inference_time
    })

if __name__ == '__main__':
    load_pipeline()
    print("\n" + "="*50)
    print("🚀 Sentiment Analysis Server Starting...")
    print("="*50)
    print("📍 URL: http://localhost:7860")
    print("📱 Model: distilbert-base-uncased-finetuned-sst-2-english")
    print("="*50 + "\n")

    # Run on port 7860 (Gradio/HF Spaces standard)
    app.run(host='0.0.0.0', port=7860, debug=False)