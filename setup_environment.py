#!/usr/bin/env python3
"""
Setup script for Sandvik LH410 Failure Predictive Maintenance Web App
This script sets up the virtual environment and installs all dependencies.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    print("🔄 Creating virtual environment...")
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_virtual_environment():
    """Activate virtual environment"""
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    print(f"🔄 Activating virtual environment: {activate_script}")
    return True

def install_backend_dependencies():
    """Install backend Python dependencies"""
    return run_command("pip install -r backend/requirements.txt", "Installing backend dependencies")

def install_data_dependencies():
    """Install data processing dependencies"""
    return run_command("pip install -r data/requirements.txt", "Installing data processing dependencies")

def install_frontend_dependencies():
    """Install frontend Node.js dependencies"""
    if not os.path.exists("frontend/node_modules"):
        os.chdir("frontend")
        success = run_command("npm install", "Installing frontend dependencies")
        os.chdir("..")
        return success
    else:
        print("✅ Frontend dependencies already installed")
        return True

def verify_installation():
    """Verify that all key packages are installed"""
    print("\n🔍 Verifying installation...")
    
    # Test Python packages
    test_imports = [
        "fastapi", "motor", "pydantic", "sklearn", "xgboost", 
        "pandas", "numpy", "matplotlib", "seaborn", "joblib"
    ]
    
    for package in test_imports:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
            return False
    
    # Test Node.js packages
    if os.path.exists("frontend/node_modules"):
        print("✅ Node.js dependencies")
    else:
        print("❌ Node.js dependencies - NOT FOUND")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Sandvik LH410 Failure Predictive Maintenance Web App")
    print("=" * 70)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Activate virtual environment (informational)
    activate_virtual_environment()
    
    # Install dependencies
    if not install_backend_dependencies():
        sys.exit(1)
    
    if not install_data_dependencies():
        sys.exit(1)
    
    if not install_frontend_dependencies():
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Some dependencies failed to install. Please check the errors above.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run data preprocessing:")
    print("   cd data && python preprocess_alarm_data.py")
    print("3. Train the model:")
    print("   python train_models.py")
    print("4. Start the backend:")
    print("   cd backend && uvicorn main:app --reload")
    print("5. Start the frontend:")
    print("   cd frontend && npm run dev")

if __name__ == "__main__":
    main() 