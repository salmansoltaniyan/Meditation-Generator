#!/usr/bin/env python3
"""
Main entry point for the Guided Meditation Generator
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main application
from meditation_generator import main

if __name__ == "__main__":
    main()
