"""
Ultra-Lightweight MLP for Mobile ML

A tiny neural network designed for:
- Mobile devices (Android/Termux)
- Quick training (under 2 hours)
- Small model size (< 50MB)
- Minimal memory footprint

Architecture:
- Input: 784 (28x28 MNIST-like)
- Hidden1: 64 neurons (ReLU)
- Hidden2: 32 neurons (ReLU)
- Output: 10 classes (LogSoftmax)
- Total parameters: ~51,000
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from tqdm import tqdm
import os

class TinyMLP(nn.Module):
    """Ultra-compact Multi-Layer Perceptron"""

    def __init__(self, input_size=784, hidden1=64, hidden2=32, num_classes=10):
        super(TinyMLP, self).__init__()

        # Single responsibility: transform input to output
        self.features = nn.Sequential(
            nn.Linear(input_size, hidden1),
            nn.ReLU(),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
        )

        # Classifier head
        self.classifier = nn.Linear(hidden2, num_classes)

    def forward(self, x):
        # Flatten input if needed (for images)
        x = x.view(x.size(0), -1)
        x = self.features(x)
        x = self.classifier(x)
        return x

def create_synthetic_data(num_samples=1000):
    """Generate synthetic dataset for quick testing"""
    print(f"📊 Creating synthetic dataset: {num_samples} samples")

    # Generate random input data (28x28 = 784 features)
    X = torch.randn(num_samples, 784)

    # Generate random labels
    y = torch.randint(0, 10, (num_samples,))

    return X, y

def train_model(model, train_loader, epochs=5, lr=0.01):
    """Train the model with mobile-optimized settings"""

    device = torch.device('cpu')  # Mobile devices use CPU
    model = model.to(device)

    # Mobile-optimized: smaller learning rate, fewer epochs
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    print(f"\n🚀 Starting training on {device}")
    print(f"📚 Epochs: {epochs} | Learning rate: {lr}")
    print("-" * 50)

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}")

        for batch_x, batch_y in progress_bar:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            # Forward pass
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)

            # Backward pass
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            # Update progress
            avg_loss = total_loss / (progress_bar.n + 1)
            progress_bar.set_postfix({'loss': f'{avg_loss:.4f}'})

        avg_epoch_loss = total_loss / len(train_loader)
        print(f"✅ Epoch {epoch+1}/{epochs} - Avg Loss: {avg_epoch_loss:.4f}")

    print("\n🎉 Training complete!")
    return model

def evaluate_model(model, test_loader):
    """Quick evaluation"""
    device = next(model.parameters()).device
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            outputs = model(batch_x)
            _, predicted = torch.max(outputs.data, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()

    accuracy = 100 * correct / total
    print(f"\n📊 Test Accuracy: {accuracy:.2f}%")
    return accuracy

def save_model(model, path="models/tiny_mlp.pth"):
    """Save model with metadata"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save model weights
    torch.save(model.state_dict(), path)

    # Save metadata
    metadata = {
        'model_size_mb': os.path.getsize(path) / (1024 * 1024),
        'total_params': sum(p.numel() for p in model.parameters()),
        'architecture': 'TinyMLP',
        'device': 'cpu'
    }

    metadata_path = path.replace('.pth', '_metadata.yaml')
    import yaml
    with open(metadata_path, 'w') as f:
        yaml.dump(metadata, f)

    print(f"\n💾 Model saved: {path}")
    print(f"   Size: {metadata['model_size_mb']:.2f} MB")
    print(f"   Parameters: {metadata['total_params']:,}")
    print(f"   Metadata: {metadata_path}")

def load_model(path="models/tiny_mlp.pth"):
    """Load saved model"""
    model = TinyMLP()
    model.load_state_dict(torch.load(path, map_location='cpu'))
    return model

def main():
    """Main training pipeline"""
    print("=" * 60)
    print("🤖 Ultra-Lightweight ML Training (Mobile-Optimized)")
    print("=" * 60)

    # Create model
    print("\n🔧 Creating TinyMLP model...")
    model = TinyMLP()
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Generate synthetic data
    X_train, y_train = create_synthetic_data(1000)
    X_test, y_test = create_synthetic_data(200)

    # Create data loaders (small batches for mobile)
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32)

    # Train model
    model = train_model(model, train_loader, epochs=3, lr=0.01)

    # Evaluate
    accuracy = evaluate_model(model, test_loader)

    # Save model
    save_model(model)

    print("\n" + "=" * 60)
    print("✨ Training pipeline complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()