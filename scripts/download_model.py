from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

def download_model():
    """
    Downloads a Hugging Face model and tokenizer and saves them locally.
    """
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    output_dir = "models/sentiment-model"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created directory: {output_dir}")

    # Download and save the tokenizer
    try:
        print(f"⏳ Downloading tokenizer for '{model_name}'...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(output_dir)
        print(f"✅ Tokenizer saved to: {output_dir}")
    except Exception as e:
        print(f"❌ An error occurred while downloading the tokenizer: {e}")
        return

    # Download and save the model
    try:
        print(f"⏳ Downloading model for '{model_name}'...")
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.save_pretrained(output_dir)
        print(f"✅ Model saved to: {output_dir}")
    except Exception as e:
        print(f"❌ An error occurred while downloading the model: {e}")
        return

if __name__ == "__main__":
    download_model()
