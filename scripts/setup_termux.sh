#!/bin/bash
# Termux Environment Setup Script
# Phase 1: Foundation

set -e  # Exit on error

echo "🚀 Setting up Termux environment for Lightweight ML..."

# Update packages
pkg update -y

# Install core dependencies
echo "📦 Installing core packages..."
pkg install -y \
    python \
    python-dev \
    git \
    curl \
    wget \
    nano \
    vim \
    tmux \
    openssh

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Setup tmux
echo "🖥️ Setting up tmux session..."
tmux new-session -d -s ml-workspace
tmux send-keys -t ml-workspace "source venv/bin/activate" Enter
tmux send-keys -t ml-workspace "echo 'Environment ready!'" Enter

echo "✅ Termux setup complete!"
echo "💡 Run 'tmux attach -t ml-workspace' to continue"

# Save environment info
echo "Lightweight ML Termux Environment" > environment.txt
date >> environment.txt
uname -a >> environment.txt
python --version >> environment.txt