import os
import sys

# Ensure project root is on sys.path so `src` can be imported when executed by Vercel
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the Flask app from src/main.py
from src.main import app  # noqa: F401  (Vercel detects module-level `app` as WSGI entrypoint)


