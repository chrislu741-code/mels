#!/usr/bin/env python3
"""
APTS Launcher - Auto-installs dependencies and launches APTS
"""

import subprocess
import sys
import os

def check_and_install_dependencies():
    """Check for required packages and install if missing"""
    required_packages = ['rich', 'aiohttp', 'psutil', 'cryptography', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("🔧 Installing missing dependencies...")
        print(f"Missing packages: {', '.join(missing_packages)}")
        
        # Run the installer
        try:
            subprocess.run([sys.executable, "install_requirements.py"], check=True)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies automatically.")
            print("Please run manually: python3 install_requirements.py")
            return False
    
    return True

def main():
    print("🚀 APTS Launcher Starting...")
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        sys.exit(1)
    
    # Launch APTS
    print("🎯 Launching APTS...")
    try:
        subprocess.run([sys.executable, "apts.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch APTS: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 APTS launcher interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()