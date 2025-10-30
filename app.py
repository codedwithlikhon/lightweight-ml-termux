"""
Hugging Face Spaces Deployment
Simple web app to serve the TinyMLP model

Features:
- Model loading from models/tiny_mlp.pth
- Simple web interface
- Fast inference (< 3 seconds cold start)
"""

import torch
import torch.nn as nn
import numpy as np
from flask import Flask, request, jsonify, render_template_string
import os
import time

# Model architecture (must match training)
class TinyMLP(nn.Module):
    def __init__(self, input_size=784, hidden1=64, hidden2=32, num_classes=10):
        super(TinyMLP, self).__init__()
        self.features = nn.Sequential(
            nn.Linear(input_size, hidden1),
            nn.ReLU(),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
        )
        self.classifier = nn.Linear(hidden2, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.features(x)
        x = self.classifier(x)
        return x

app = Flask(__name__)

# Global model variable (loaded once)
model = None
device = torch.device('cpu')

def load_model():
    """Load model once at startup"""
    global model
    if model is None:
        model_path = "models/tiny_mlp.pth"
        if os.path.exists(model_path):
            model = TinyMLP()
            model.load_state_dict(torch.load(model_path, map_location='cpu'))
            model.eval()
            print(f"✅ Model loaded: {model_path}")
        else:
            print(f"❌ Model not found: {model_path}")

@app.route('/')
def home():
    """Simple web interface"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TinyMLP - Ultra-Lightweight ML</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .box { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
            button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #2980b9; }
            #result { margin-top: 20px; padding: 10px; display: none; }
        </style>
    </head>
    <body>
        <h1>🤖 TinyMLP - Ultra-Lightweight Model</h1>
        <div class="box">
            <h3>About</h3>
            <p>Model size: <strong>0.20 MB</strong></p>
            <p>Parameters: <strong>52,650</strong></p>
            <p>Architecture: <strong>784 → 64 → 32 → 10</strong></p>
            <p>Trained on: <strong>Android Termux (Mobile CPU)</strong></p>
        </div>

        <div class="box">
            <h3>Test Prediction</h3>
            <button onclick="predict()">Generate Random Prediction</button>
            <div id="result"></div>
        </div>

        <script>
            async function predict() {
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '⏳ Predicting...';

                try {
                    const response = await fetch('/predict', { method: 'POST' });
                    const data = await response.json();
                    resultDiv.innerHTML = `
                        <h4>Prediction Result</h4>
                        <p><strong>Predicted class:</strong> ${data.prediction}</p>
                        <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
                        <p><strong>Response time:</strong> ${data.inference_time}ms</p>
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
    """API endpoint for predictions"""
    if model is None:
        load_model()

    # Generate random input (28x28 = 784 features)
    x = torch.randn(1, 784)

    # Predict
    start_time = time.time()
    with torch.no_grad():
        outputs = model(x)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = torch.max(probabilities).item()
    inference_time = int((time.time() - start_time) * 1000)

    return jsonify({
        'prediction': predicted_class,
        'confidence': confidence,
        'inference_time': inference_time,
        'model_info': {
            'size_mb': 0.20,
            'parameters': 52650,
            'architecture': '784->64->32->10'
        }
    })

if __name__ == '__main__':
    load_model()
    print("\n" + "="*50)
    print("🚀 TinyMLP Server Starting...")
    print("="*50)
    print("📍 URL: http://localhost:7860")
    print("📱 Model: 0.20 MB | 52,650 params")
    print("="*50 + "\n")

    # Run on port 7860 (Gradio/HF Spaces standard)
    app.run(host='0.0.0.0', port=7860, debug=False)