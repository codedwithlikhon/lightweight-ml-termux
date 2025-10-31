import os
from huggingface_hub import HfApi

def upload_model(model_path="models/sentiment-model"):
    """
    Uploads a model to the Hugging Face Hub, creating the repository if it doesn't exist.

    Args:
        model_path (str): The local path to the model directory.
                          Defaults to 'models/sentiment-model'.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Hugging Face token not found. Please set the HF_TOKEN environment variable.")

    api = HfApi()
    repo_id = "santiagobasulto/lightweight-ml-termux"

    # Create the repository if it doesn't exist
    api.create_repo(
        repo_id=repo_id,
        repo_type="model",
        token=hf_token,
        private=True,
        exist_ok=True,
    )
    print(f"Repository '{repo_id}' created or already exists.")

    # Upload the model files
    api.upload_folder(
        folder_path=model_path,
        repo_id=repo_id,
        repo_type="model",
        token=hf_token,
    )
    print(f"Model from {model_path} uploaded to {repo_id}")

if __name__ == "__main__":
    upload_model()
