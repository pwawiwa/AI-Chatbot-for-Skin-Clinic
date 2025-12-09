#!/usr/bin/env python
"""
Main entry point — interactive LLM chat testing
"""
import sys
from pathlib import Path
# Ensure project root is on sys.path so `src` can be imported when running script directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.main import main


if __name__ == "__main__":
    main()
