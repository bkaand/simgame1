#!/usr/bin/env python3
"""
Setup script for Medieval Life Simulator
"""
import os
import sys
import subprocess

def main():
    """Install required dependencies."""
    print("Setting up Medieval Life Simulator...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
        sys.exit(1)
    
    print("\nSetup complete! You can now run the game with:")
    print("python main.py")

if __name__ == "__main__":
    main() 