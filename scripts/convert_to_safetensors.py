import torch
from safetensors.torch import save_file
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import TinyMLP

def convert_model():
    """
    Loads a .pth model and saves it as a .safetensors file.
    """
    # Define paths
    pth_path = "models/tiny_mlp.pth"
    safetensors_path = "models/tiny_mlp.safetensors"

    # Initialize model
    model = TinyMLP()

    # Load the state dict from the .pth file
    try:
        state_dict = torch.load(pth_path, map_location="cpu")
        model.load_state_dict(state_dict)
        print(f"✅ Successfully loaded model from: {pth_path}")
    except FileNotFoundError:
        print(f"❌ Error: Model file not found at {pth_path}")
        return
    except Exception as e:
        print(f"❌ An error occurred while loading the model: {e}")
        return

    # Save the state dict to the .safetensors file
    try:
        save_file(model.state_dict(), safetensors_path)
        print(f"✅ Successfully saved model to: {safetensors_path}")
    except Exception as e:
        print(f"❌ An error occurred while saving the model: {e}")
        return

if __name__ == "__main__":
    convert_model()
