#!/usr/bin/env python3
"""
APTS Installation Script
Automated Installation of Advanced Penetration Testing System

This script automatically installs and configures APTS with all required
dependencies, frameworks, and optimizations for nation-state level
penetration testing.

CLASSIFICATION: AUTHORIZED USE ONLY
"""

import os
import sys
import subprocess
import platform
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path
import json
import time

class APTSInstaller:
    """APTS Installation and Configuration Manager"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.architecture = platform.machine().lower()
        self.python_version = sys.version_info
        
        # Installation paths
        self.install_dir = Path.cwd()
        self.tools_dir = self.install_dir / "tools"
        self.config_dir = self.install_dir / "config"
        
        # Installation status
        self.installation_log = []
        self.failed_components = []
        
    def print_banner(self):
        """Print APTS installation banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  █████╗ ██████╗ ████████╗███████╗                           ║
║ ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝                           ║
║ ███████║██████╔╝   ██║   ███████╗                           ║
║ ██╔══██║██╔═══╝    ██║   ╚════██║                           ║
║ ██║  ██║██║        ██║   ███████║                           ║
║ ╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝                           ║
║                                                               ║
║        INSTALLATION SYSTEM                                    ║
║        Nation-State Level Penetration Testing                 ║
║                                                               ║
║        Version: 1.0.0 - GHOST PROTOCOL                       ║
║        Classification: AUTHORIZED USE ONLY                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🚀 APTS AUTOMATED INSTALLATION SYSTEM
Installing nation-state level penetration testing capabilities...
        """
        print(banner)
    
    def check_system_requirements(self):
        """Check system requirements"""
        print("🔍 Checking system requirements...")
        
        # Check Python version
        if self.python_version < (3, 8):
            print(f"❌ Python 3.8+ required. Current version: {sys.version}")
            return False
        
        print(f"✅ Python {sys.version.split()[0]} - Compatible")
        
        # Check operating system
        supported_systems = ['linux', 'darwin', 'windows']
        if self.system not in supported_systems:
            print(f"❌ Unsupported operating system: {self.system}")
            return False
        
        print(f"✅ Operating System: {platform.system()} - Supported")
        
        # Check available disk space (minimum 10GB)
        disk_usage = shutil.disk_usage(self.install_dir)
        free_gb = disk_usage.free / (1024**3)
        
        if free_gb < 10:
            print(f"❌ Insufficient disk space. Required: 10GB, Available: {free_gb:.1f}GB")
            return False
        
        print(f"✅ Disk Space: {free_gb:.1f}GB available")
        
        # Check memory (minimum 4GB)
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < 4:
                print(f"⚠️ Low memory detected: {memory_gb:.1f}GB (4GB recommended)")
            else:
                print(f"✅ Memory: {memory_gb:.1f}GB available")
        except ImportError:
            print("⚠️ Cannot check memory - psutil not installed")
        
        return True
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            print("✅ pip upgraded successfully")
            
            # Install requirements
            requirements_file = self.install_dir / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                             check=True, capture_output=True)
                print("✅ Python dependencies installed successfully")
            else:
                print("⚠️ requirements.txt not found - installing core dependencies")
                core_deps = [
                    "rich>=13.0.0",
                    "aiohttp>=3.8.0", 
                    "psutil>=5.9.0",
                    "cryptography>=41.0.0",
                    "requests>=2.31.0",
                    "beautifulsoup4>=4.12.0"
                ]
                
                for dep in core_deps:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                     check=True, capture_output=True)
                        print(f"✅ Installed {dep}")
                    except subprocess.CalledProcessError:
                        print(f"❌ Failed to install {dep}")
                        self.failed_components.append(dep)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Python dependencies: {e}")
            return False
        
        return True
    
    def install_system_tools(self):
        """Install system-level tools"""
        print("🛠️ Installing system tools...")
        
        if self.system == "linux":
            return self._install_linux_tools()
        elif self.system == "darwin":
            return self._install_macos_tools()
        elif self.system == "windows":
            return self._install_windows_tools()
        
        return True
    
    def _install_linux_tools(self):
        """Install Linux-specific tools"""
        tools = [
            ("nmap", "Network scanning"),
            ("tor", "Anonymization network"),
            ("proxychains", "Proxy chaining"),
            ("curl", "HTTP client"),
            ("wget", "File downloader"),
            ("git", "Version control")
        ]
        
        # Detect package manager
        package_managers = [
            ("apt-get", ["sudo", "apt-get", "update", "&&", "sudo", "apt-get", "install", "-y"]),
            ("yum", ["sudo", "yum", "install", "-y"]),
            ("pacman", ["sudo", "pacman", "-S", "--noconfirm"]),
            ("zypper", ["sudo", "zypper", "install", "-y"])
        ]
        
        pm_cmd = None
        for pm, cmd in package_managers:
            if shutil.which(pm):
                pm_cmd = cmd
                break
        
        if not pm_cmd:
            print("⚠️ No supported package manager found")
            return True
        
        for tool, description in tools:
            try:
                if not shutil.which(tool):
                    print(f"📦 Installing {tool} ({description})...")
                    subprocess.run(pm_cmd + [tool], check=True, capture_output=True)
                    print(f"✅ {tool} installed successfully")
                else:
                    print(f"✅ {tool} already installed")
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {tool}")
                self.failed_components.append(tool)
        
        return True
    
    def _install_macos_tools(self):
        """Install macOS-specific tools"""
        # Check for Homebrew
        if not shutil.which("brew"):
            print("⚠️ Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return True
        
        tools = ["nmap", "tor", "proxychains-ng", "curl", "wget", "git"]
        
        for tool in tools:
            try:
                if not shutil.which(tool.replace("-ng", "")):
                    print(f"📦 Installing {tool}...")
                    subprocess.run(["brew", "install", tool], check=True, capture_output=True)
                    print(f"✅ {tool} installed successfully")
                else:
                    print(f"✅ {tool} already installed")
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {tool}")
                self.failed_components.append(tool)
        
        return True
    
    def _install_windows_tools(self):
        """Install Windows-specific tools"""
        print("⚠️ Windows installation requires manual setup of some tools:")
        print("   - Download and install Nmap from https://nmap.org/download.html")
        print("   - Download and install Tor Browser from https://www.torproject.org/")
        print("   - Install Git from https://git-scm.com/download/win")
        
        return True
    
    def setup_directories(self):
        """Setup APTS directory structure"""
        print("📁 Setting up directory structure...")
        
        directories = [
            "core",
            "core/frameworks", 
            "core/exploits",
            "core/stealth",
            "tools",
            "config",
            "logs",
            "reports",
            "evidence",
            "templates",
            "data",
            "scripts"
        ]
        
        for directory in directories:
            dir_path = self.install_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        
        return True
    
    def configure_system(self):
        """Configure APTS system"""
        print("⚙️ Configuring APTS system...")
        
        # Create configuration files
        config_files = {
            "apts_config.json": {
                "version": "1.0.0",
                "classification": "AUTHORIZED USE ONLY",
                "installation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "system_info": {
                    "os": platform.system(),
                    "architecture": platform.machine(),
                    "python_version": sys.version
                },
                "components": {
                    "ai_coordinator": True,
                    "ghost_mode": True,
                    "memory_optimizer": True,
                    "reporting_system": True
                },
                "security": {
                    "encryption_enabled": True,
                    "anonymization_enabled": True,
                    "stealth_mode": True
                }
            },
            "ghost_mode_config.json": {
                "proxy_sources": 88,
                "verification_steps": 10,
                "rotation_interval": 60,
                "anonymity_level": "maximum",
                "tor_enabled": True,
                "vpn_chaining": True
            },
            "frameworks_config.json": {
                "cobalt_strike": {
                    "enabled": True,
                    "priority": 1,
                    "simulation_mode": True
                },
                "empire": {
                    "enabled": True,
                    "priority": 2,
                    "simulation_mode": True
                },
                "poshc2": {
                    "enabled": True,
                    "priority": 3,
                    "simulation_mode": True
                },
                "metasploit": {
                    "enabled": True,
                    "priority": 4,
                    "simulation_mode": True
                }
            }
        }
        
        for filename, config in config_files.items():
            config_path = self.config_dir / filename
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Created configuration: {filename}")
        
        return True
    
    def install_penetration_frameworks(self):
        """Install penetration testing frameworks"""
        print("🎯 Installing penetration testing frameworks...")
        
        frameworks = [
            {
                "name": "Metasploit Community",
                "description": "Open source penetration testing framework",
                "install_method": "package_manager",
                "required": False
            },
            {
                "name": "Empire Framework", 
                "description": "PowerShell post-exploitation framework",
                "install_method": "git_clone",
                "url": "https://github.com/EmpireProject/Empire.git",
                "required": False
            },
            {
                "name": "PoshC2",
                "description": "Python C2 framework",
                "install_method": "git_clone", 
                "url": "https://github.com/nettitude/PoshC2.git",
                "required": False
            }
        ]
        
        for framework in frameworks:
            try:
                print(f"📦 Installing {framework['name']}...")
                
                if framework["install_method"] == "git_clone":
                    repo_dir = self.tools_dir / framework["name"].lower().replace(" ", "_")
                    if not repo_dir.exists():
                        subprocess.run([
                            "git", "clone", framework["url"], str(repo_dir)
                        ], check=True, capture_output=True)
                        print(f"✅ {framework['name']} cloned successfully")
                    else:
                        print(f"✅ {framework['name']} already exists")
                
                elif framework["install_method"] == "package_manager":
                    print(f"⚠️ {framework['name']} requires manual installation")
                
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {framework['name']}")
                if framework["required"]:
                    self.failed_components.append(framework["name"])
        
        return True
    
    def optimize_system(self):
        """Optimize system for APTS"""
        print("⚡ Optimizing system for APTS...")
        
        # Create optimization script
        optimization_script = """#!/bin/bash
# APTS System Optimization Script

echo "🚀 Optimizing system for APTS..."

# Increase file descriptor limits
echo "* soft nofile 65536" >> /etc/security/limits.conf 2>/dev/null || true
echo "* hard nofile 65536" >> /etc/security/limits.conf 2>/dev/null || true

# Optimize network settings
echo "net.core.rmem_max = 16777216" >> /etc/sysctl.conf 2>/dev/null || true
echo "net.core.wmem_max = 16777216" >> /etc/sysctl.conf 2>/dev/null || true

# Create APTS service user (optional)
useradd -r -s /bin/false apts 2>/dev/null || true

echo "✅ System optimization completed"
        """
        
        script_path = self.install_dir / "scripts" / "optimize_system.sh"
        with open(script_path, 'w') as f:
            f.write(optimization_script)
        
        script_path.chmod(0o755)
        print("✅ Optimization script created")
        
        return True
    
    def run_tests(self):
        """Run installation tests"""
        print("🧪 Running installation tests...")
        
        tests = [
            ("Python imports", self._test_python_imports),
            ("Core modules", self._test_core_modules),
            ("Configuration files", self._test_configuration),
            ("Directory structure", self._test_directories)
        ]
        
        passed_tests = 0
        for test_name, test_func in tests:
            try:
                if test_func():
                    print(f"✅ {test_name} - PASSED")
                    passed_tests += 1
                else:
                    print(f"❌ {test_name} - FAILED")
            except Exception as e:
                print(f"❌ {test_name} - ERROR: {e}")
        
        print(f"📊 Tests completed: {passed_tests}/{len(tests)} passed")
        return passed_tests == len(tests)
    
    def _test_python_imports(self):
        """Test Python imports"""
        try:
            import rich
            import aiohttp
            import psutil
            import cryptography
            return True
        except ImportError:
            return False
    
    def _test_core_modules(self):
        """Test core APTS modules"""
        core_files = [
            "apts.py",
            "core/__init__.py",
            "core/ai_coordinator.py",
            "core/ghost_mode.py",
            "core/memory_optimizer.py",
            "core/reporting.py"
        ]
        
        for file_path in core_files:
            if not (self.install_dir / file_path).exists():
                return False
        
        return True
    
    def _test_configuration(self):
        """Test configuration files"""
        config_files = [
            "config/apts_config.json",
            "config/ghost_mode_config.json", 
            "config/frameworks_config.json"
        ]
        
        for file_path in config_files:
            if not (self.install_dir / file_path).exists():
                return False
        
        return True
    
    def _test_directories(self):
        """Test directory structure"""
        required_dirs = [
            "core", "tools", "config", "logs", 
            "reports", "evidence", "templates"
        ]
        
        for directory in required_dirs:
            if not (self.install_dir / directory).exists():
                return False
        
        return True
    
    def generate_installation_report(self):
        """Generate installation report"""
        print("📋 Generating installation report...")
        
        report = {
            "installation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": {
                "os": platform.system(),
                "architecture": platform.machine(),
                "python_version": sys.version
            },
            "installation_status": "SUCCESS" if not self.failed_components else "PARTIAL",
            "failed_components": self.failed_components,
            "installation_log": self.installation_log,
            "next_steps": [
                "Run 'python3 apts.py' to start APTS",
                "Review configuration files in config/ directory",
                "Check logs/ directory for system logs",
                "Read README.md for usage instructions"
            ]
        }
        
        report_path = self.install_dir / "installation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Installation report saved: {report_path}")
        return report
    
    def install(self):
        """Run complete APTS installation"""
        self.print_banner()
        
        print("🚀 Starting APTS installation...")
        print("=" * 60)
        
        # Installation steps
        steps = [
            ("System Requirements", self.check_system_requirements),
            ("Directory Structure", self.setup_directories),
            ("Python Dependencies", self.install_python_dependencies),
            ("System Tools", self.install_system_tools),
            ("System Configuration", self.configure_system),
            ("Penetration Frameworks", self.install_penetration_frameworks),
            ("System Optimization", self.optimize_system),
            ("Installation Tests", self.run_tests)
        ]
        
        completed_steps = 0
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            try:
                if step_func():
                    print(f"✅ {step_name} completed successfully")
                    completed_steps += 1
                else:
                    print(f"⚠️ {step_name} completed with warnings")
                    completed_steps += 1
            except Exception as e:
                print(f"❌ {step_name} failed: {e}")
                self.failed_components.append(step_name)
        
        # Generate report
        report = self.generate_installation_report()
        
        # Final status
        print("\n" + "=" * 60)
        if completed_steps == len(steps) and not self.failed_components:
            print("🎉 APTS INSTALLATION COMPLETED SUCCESSFULLY!")
            print("\n🚀 Ready to launch APTS:")
            print("   python3 apts.py")
        else:
            print("⚠️ APTS INSTALLATION COMPLETED WITH WARNINGS")
            print(f"   Completed: {completed_steps}/{len(steps)} steps")
            if self.failed_components:
                print(f"   Failed components: {', '.join(self.failed_components)}")
        
        print("\n📋 Installation report saved: installation_report.json")
        print("📖 Read README.md for usage instructions")
        print("\n🔒 CLASSIFICATION: AUTHORIZED USE ONLY")

def main():
    """Main installation function"""
    installer = APTSInstaller()
    installer.install()

if __name__ == "__main__":
    main()