"""
Deploy TinyMLP to Hugging Face Spaces
Automatically creates and configures a Space
"""

import os
import sys
from huggingface_hub import HfApi
import subprocess

def create_space():
    """Create and upload to Hugging Face Spaces"""

    print("🚀 Starting Hugging Face Spaces Deployment")
    print("="*60)

    # Initialize HF API (uses gh token)
    api = HfApi()
    print("✅ Hugging Face API initialized")

    # Space configuration
    space_id = "tiny-mlp-ultra-lightweight"
    username = "codedwithlikhon"
    repo_id = f"{username}/{space_id}"
    private = False  # Public space for easy access

    print(f"\n📦 Space Details:")
    print(f"   ID: {space_id}")
    print(f"   Repository: {repo_id}")
    print(f"   Visibility: {'Private' if private else 'Public'}")

    # Check if Space already exists
    print("\n🔍 Checking if Space exists...")
    try:
        api.repo_info(repo_id=repo_id)
        print("⚠️  Space already exists!")
        print(f"   URL: https://huggingface.co/spaces/{repo_id}")
        choice = input("   Do you want to update it? (y/n): ")
        if choice.lower() != 'y':
            print("❌ Deployment cancelled")
            return
    except Exception as e:
        print(f"✅ Space does not exist, will create new one")

    # Create Space
    print("\n🏗️  Creating Space...")
    try:
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            private=private,
            space_sdk="gradio"  # We'll use Gradio
        )
        print(f"✅ Space created: {repo_id}")
    except Exception as e:
        print(f"❌ Failed to create Space: {e}")
        return

    # Create Space-specific files
    print("\n📝 Creating Space configuration...")

    # app.py is already created
    # requirements.txt is already created
    # Create README.md for Space
    readme_content = """# TinyMLP - Ultra-Lightweight ML

🤖 **Ultra-Lightweight Neural Network (0.20 MB)**

Trained entirely on Android Termux!

## Model Info
- **Architecture**: Multi-Layer Perceptron (784 → 64 → 32 → 10)
- **Parameters**: 52,650
- **Model Size**: 0.20 MB
- **Training**: Mobile CPU (Android Termux)
- **Inference Time**: < 50ms

## Live Demo
Visit the app tab above to test predictions!

## API
```bash
curl https://huggingface.co/spaces/{repo_id}/predict -X POST
```

## Training Details
- Framework: PyTorch 2.6.0
- Dataset: Synthetic (28x28 features)
- Optimizer: Adam (lr=0.01)
- Training Time: ~3 seconds
- Memory: Minimal (CPU, batch size 32)

## Philosophy
> "Beautiful is better than ugly. Simple is better than complex."

Built for mobile-first ML deployment with zero vendor lock-in.

## Cost
- CPU Basic: **FREE** ✅
- Storage: ~1 MB
- Inference: $0

---
*Deployed from Android Termux* 📱
"""

    # Write README
    with open("README_spaces.md", "w") as f:
        f.write(readme_content)

    # Upload files
    print("\n📤 Uploading files to Space...")

    files_to_upload = [
        "app.py",
        "requirements-spaces.txt",
        "models/tiny_mlp.pth",
        "models/tiny_mlp_metadata.yaml",
        "README_spaces.md"
    ]

    for file_path in files_to_upload:
        if os.path.exists(file_path):
            api.upload_file(
                path_or_fileobj=open(file_path, "rb").read(),
                path_in_repo=file_path,
                repo_id=repo_id
            )
            print(f"   ✅ Uploaded: {file_path}")
        else:
            print(f"   ⚠️  Not found: {file_path}")

    print("\n" + "="*60)
    print("🎉 Deployment Complete!")
    print("="*60)
    print(f"🌐 Space URL: https://huggingface.co/spaces/{repo_id}")
    print(f"📱 Your ultra-lightweight model is now live!")
    print("="*60)

if __name__ == "__main__":
    create_space()