import os
from huggingface_hub import snapshot_download

def download_model():
    """
    Downloads the sentiment analysis model from the Hugging Face Hub.
    """
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    local_dir = "models/sentiment-model"

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    print(f"Downloading model: {model_name} to {local_dir}")
    snapshot_download(repo_id=model_name, local_dir=local_dir, repo_type="model")
    print("Model download complete.")

if __name__ == "__main__":
    download_model()
