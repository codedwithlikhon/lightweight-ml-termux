# AI Agent Instructions

This document provides instructions for AI coding agents to work on this project.

## Project Overview

The goal of this project is to build and deploy lightweight machine learning models from a Termux environment on Android to multiple cloud platforms. The philosophy is to maintain simplicity and minimalism while maximizing functionality.

## Core Technologies

- **Backend:** Flask, Gunicorn
- **Machine Learning:** Hugging Face Transformers
- **Testing:** Pytest

## Project Structure

```
.
├── models/          # Lightweight model architectures
├── data/           # Training and test datasets
├── deployments/    # Multi-cloud deployment configs
├── scripts/        # Automation and utility scripts
├── docs/           # Documentation
├── tests/          # Test suites
└── notebooks/      # Jupyter notebooks for exploration
```

- `app.py`: The main Flask application that serves the sentiment analysis model.
- `tests/`: Contains the test suite for the application.
- `scripts/download_model.py`: A script to download the Hugging Face model.
- `models/`: This directory stores the downloaded model files and is excluded from Git.
- `Procfile`: Defines the command to run the application in production using Gunicorn.
- `requirements.txt`: The main dependency file.
- `requirements-spaces.txt`: A minimal dependency file for Hugging Face Spaces deployment.

## Setup and Dependencies

To set up the project, install the dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the Flask server for local development, use the following command:

```bash
python app.py
```

## Running Tests

To run the test suite, execute the following command from the project root:

```bash
python -m pytest
```

## Model Information

The project uses the `distilbert-base-uncased-finetuned-sst-2-english` model from Hugging Face for sentiment analysis. To download the model, run the following script:

```bash
python scripts/download_model.py
```

## Deployment

The application is deployed to Hugging Face Spaces. The `Procfile` contains the Gunicorn command used for production:

```
web: gunicorn app:app
```
