#!/usr/bin/env python3
"""Download sentence-transformers model to local Models folder for offline use."""

from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "Models" / "all-MiniLM-L6-v2"

print(f"Downloading {MODEL_NAME}...")
print(f"Saving to: {MODELS_DIR}")

model = SentenceTransformer(MODEL_NAME)
model.save(str(MODELS_DIR))

model_size = sum(f.stat().st_size for f in MODELS_DIR.rglob('*') if f.is_file()) / 1024 / 1024
print(f"✅ Model downloaded and saved successfully!")
print(f"Path: {MODELS_DIR}")
print(f"Size: {model_size:.1f} MB")
