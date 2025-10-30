# Hugging Face Spaces Deployment Guide

## Quick Deploy

1. **Create Space**: Go to https://huggingface.co/spaces and create new Space
2. **Choose SDK**: Select "Gradio" or "Static"
3. **Repository**: Clone this repo to your Space
4. **Upload Model**: Ensure `models/tiny_mlp.pth` is included
5. **Dependencies**: Use `requirements-spaces.txt`

## Deployment Files

- `app.py`: Flask web application
- `requirements-spaces.txt`: Python dependencies
- `models/`: Directory containing trained models

## API Endpoints

### Web Interface
- `GET /`: Main web page with test interface

### Prediction API
- `POST /predict`: Generate predictions
  - Request: No body required (uses random data)
  - Response:
    ```json
    {
      "prediction": 3,
      "confidence": 0.92,
      "inference_time": 15,
      "model_info": {
        "size_mb": 0.20,
        "parameters": 52650,
        "architecture": "784->64->32->10"
      }
    }
    ```

## Model Information

- **Architecture**: TinyMLP (784 → 64 → 32 → 10)
- **Size**: 0.20 MB
- **Parameters**: 52,650
- **Training**: Android Termux (Mobile CPU)
- **Inference Time**: < 20ms cold start

## Local Testing

```bash
pip install -r requirements-spaces.txt
python app.py
# Visit http://localhost:7860
```

## Cost

- **CPU Basic**: Free
- **CPU Upgrade**: $0.108/hour
- **Storage**: ~1 MB

## Mobile-to-Cloud Pipeline

```
Android Termux (Training)
      ↓ (git push)
GitHub Repository
      ↓ (automatic)
Hugging Face Spaces (Deployment)
      ↓
Public API Endpoint
```