"""Shared test fixtures and path setup."""
import sys
import os
from pathlib import Path

# Add scripts/ to path so we can import sleep modules and distill
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
