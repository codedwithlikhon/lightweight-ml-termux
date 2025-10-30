# Manual Deployment to Hugging Face Spaces

## Step 1: Create Space (Browser)

1. **Go to**: https://huggingface.co/spaces
2. **Click**: "+ Create new Space"
3. **Fill in**:
   - **Space name**: `tiny-mlp-ultra-lightweight`
   - **Owner**: `codedwithlikhon` (your username)
   - **License**: `apache-2.0`
   - **SDK**: `Gradio`
   - **Hardware**: `CPU basic`
   - **Visibility**: `Public`
4. **Click**: "Create a Space"

## Step 2: Upload Files (Terminal)

Once Space is created, run these commands:

```bash
# Clone your Space (replace USERNAME)
git clone https://huggingface.co/spaces/codedwithlikhon/tiny-mlp-ultra-lightweight
cd tiny-mlp-ultra-lightweight

# Copy your model files
cp /path/to/lightweight/app.py ./
cp /path/to/lightweight/requirements-spaces.txt ./requirements.txt
cp /path/to/lightweight/models/tiny_mlp.pth ./models/
cp /path/to/lightweight/models/tiny_mlp_metadata.yaml ./models/

# Create README
cat > README.md << 'EOF'
# TinyMLP - Ultra-Lightweight ML

🤖 **Ultra-Lightweight Neural Network (0.20 MB)**

Trained entirely on Android Termux!

## Model Info
- Architecture: MLP (784 → 64 → 32 → 10)
- Parameters: 52,650
- Model Size: 0.20 MB
- Training: Mobile CPU (Android Termux)
- Inference Time: < 50ms

## Live Demo
Visit the app tab above to test predictions!

## API
\`\`\`bash
curl https://huggingface.co/spaces/codedwithlikhon/tiny-mlp-ultra-lightweight/predict -X POST
\`\`\`

---
*Deployed from Android Termux* 📱
EOF

# Add, commit, and push
git add .
git commit -m "feat: Deploy TinyMLP to Spaces

- Ultra-lightweight model: 0.20 MB | 52,650 params
- Trained on Android Termux
- Fast inference: < 50ms
- Free hosting on CPU basic"
git push origin main
```

## Step 3: Verify Deployment

After pushing:
1. Visit: https://huggingface.co/spaces/codedwithlikhon/tiny-mlp-ultra-lightweight
2. Wait 2-3 minutes for build to complete
3. Click "App" tab to test
4. Test prediction button

## Step 4: API Testing

```bash
# Test the prediction API
curl https://huggingface.co/spaces/codedwithlikhon/tiny-mlp-ultra-lightweight/predict \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}'
```

Expected response:
```json
{
  "prediction": 5,
  "confidence": 0.92,
  "inference_time": 31,
  "model_info": {
    "size_mb": 0.20,
    "parameters": 52650,
    "architecture": "784->64->32->10"
  }
}
```

## Cost

- **CPU Basic**: FREE ✅
- **Storage**: ~1 MB
- **Bandwidth**: Included in free tier

## Total Deployment Time: ~5 minutes

---

**Alternative**: If you prefer, you can upload files directly through the browser at https://huggingface.co/spaces/codedwithlikhon/tiny-mlp-ultra-lightweight/tree/main