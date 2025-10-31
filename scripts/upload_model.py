import os
import argparse
from huggingface_hub import HfApi

def upload_model(model_path):
    """
    Uploads a model to the Hugging Face Hub.

    Args:
        model_path (str): The local path to the model directory.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("Hugging Face token not found. Please set the HF_TOKEN environment variable.")

    api = HfApi()
    repo_id = "santiagobasulto/lightweight-ml-termux"

    api.upload_folder(
        folder_path=model_path,
        repo_id=repo_id,
        repo_type="model",
        token=hf_token,
    )
    print(f"Model from {model_path} uploaded to {repo_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a model to the Hugging Face Hub.")
    parser.add_argument("--model_path", type=str, required=True, help="The local path to the model directory.")
    args = parser.parse_args()
    upload_model(args.model_path)
