#!/usr/bin/env python3
"""
APTS Auto-Installer
Automatically installs all required dependencies and frameworks
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ {description} - Warning: {e}")
        return False

def install_python_packages():
    """Install required Python packages"""
    packages = [
        "rich",
        "aiohttp", 
        "psutil",
        "cryptography",
        "numpy",
        "requests",
        "beautifulsoup4",
        "lxml",
        "dnspython",
        "python-whois",
        "stem",
        "lz4",
        "zstandard",
        "blosc",
        "PyJWT",
        "loguru"
    ]
    
    print("📦 Installing Python packages...")
    for package in packages:
        run_command(f"{sys.executable} -m pip install --user {package}", f"Installing {package}")

def create_directories():
    """Create required directories"""
    dirs = ["logs", "reports", "data", "frameworks"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 Created directory: {dir_name}")

def main():
    print("🚀 APTS Auto-Installer Starting...")
    print("=" * 50)
    
    # Install Python packages
    install_python_packages()
    
    # Create directories
    create_directories()
    
    print("=" * 50)
    print("✅ APTS installation complete!")
    print("🎯 You can now run: python3 apts.py")

if __name__ == "__main__":
    main()