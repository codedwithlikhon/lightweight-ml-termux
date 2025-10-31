import os
from huggingface_hub import HfApi

def upload_model():
    """
    Uploads the sentiment analysis model to the Hugging Face Hub.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Hugging Face token not found. Please set the HF_TOKEN environment variable.")

    api = HfApi()
    repo_id = "santiagobasulto/lightweight-ml-termux"
    model_path = "models/sentiment-model"

    api.upload_folder(
        folder_path=model_path,
        repo_id=repo_id,
        repo_type="model",
        token=hf_token,
    )
    print(f"Model uploaded to {repo_id}")

if __name__ == "__main__":
    upload_model()
