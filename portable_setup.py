#!/usr/bin/env python3
"""
Portable Setup Script for Auto Lip Sync Plugin
"""

import os
import sys
import subprocess
from pathlib import Path

def create_portable_environment():
    plugin_dir = Path(__file__).parent
    portable_env = plugin_dir / "portable_env"
    
    print("Creating portable environment...")
    
    # Create portable environment
    subprocess.run([
        sys.executable, "-m", "venv", str(portable_env)
    ], check=True)
    
    # Get pip path
    if os.name == 'nt':  # Windows
        pip_path = portable_env / "Scripts" / "pip.exe"
        python_path = portable_env / "Scripts" / "python.exe"
    else:
        pip_path = portable_env / "bin" / "pip"
        python_path = portable_env / "bin" / "python"
    
    # Install packages
    subprocess.run([str(pip_path), "install", "montreal-forced-aligner==3.2.3"])
    subprocess.run([str(pip_path), "install", "spacy-pkuseg", "dragonmapper", "hanziconv"])
    
    print(f"Portable environment created in: {portable_env}")

if __name__ == "__main__":
    create_portable_environment() 