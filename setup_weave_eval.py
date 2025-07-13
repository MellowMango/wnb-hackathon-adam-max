"""
Setup Script for Adventure System with Weave Evaluation

This script helps set up the environment for running the adventure transformation
system with Weave evaluation capabilities.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    print("This may take a few minutes...")
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_environment_variables():
    """Check for required environment variables."""
    print("\n🔑 Checking environment variables...")
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for AI agents",
        "GOOGLE_API_KEY": "Google API key for Gemini models",
        "EXA_API_KEY": "EXA API key for contextual search",
        "WANDB_API_KEY": "Weights & Biases API key for Weave tracing"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"   ✅ {var}: Set")
        else:
            print(f"   ❌ {var}: Missing ({description})")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment before running evaluations.")
        return False
    
    print("✅ All required environment variables are set!")
    return True

def create_env_template():
    """Create a .env template file."""
    print("\n📝 Creating .env template...")
    
    env_template = """# Adventure System Environment Variables
# Copy this file to .env and fill in your API keys

# OpenAI API Key (for AI agents)
OPENAI_API_KEY=your_openai_api_key_here

# Google API Key (for Gemini models)
GOOGLE_API_KEY=your_google_api_key_here

# EXA API Key (for contextual search)
EXA_API_KEY=your_exa_api_key_here

# Weights & Biases API Key (for Weave tracing)
WANDB_API_KEY=your_wandb_api_key_here

# Optional: Weave Configuration
WANDB_PROJECT=adventure-system-evaluation
WEAVE_TRACE_AGENTS=true
WEAVE_TRACE_TASKS=true
WEAVE_TRACE_FLOWS=true
WEAVE_TRACE_MCP=true
"""
    
    template_file = ".env.template"
    with open(template_file, "w") as f:
        f.write(env_template)
    
    print(f"✅ Template created: {template_file}")
    print("   Copy this to .env and fill in your API keys")

def check_sample_files():
    """Check if sample files exist."""
    print("\n📄 Checking sample files...")
    
    sample_files = [
        "sample_transcript.txt"
    ]
    
    all_exist = True
    for file in sample_files:
        if os.path.exists(file):
            print(f"   ✅ {file}: Found")
        else:
            print(f"   ❌ {file}: Missing")
            all_exist = False
    
    return all_exist

def run_basic_test():
    """Run a basic test to verify the system works."""
    print("\n🧪 Running basic system test...")
    
    try:
        # Try importing key modules
        print("   Testing imports...")
        
        # Test weave import
        try:
            import weave
            print("   ✅ weave imported successfully")
        except ImportError as e:
            print(f"   ❌ weave import failed: {e}")
            return False
        
        # Test crewai import
        try:
            import crewai
            print("   ✅ crewai imported successfully")
        except ImportError as e:
            print(f"   ❌ crewai import failed: {e}")
            return False
            
        # Test our custom modules
        try:
            from weave_custom.config import get_weave_config
            from weave_custom.trace_hooks import setup_weave_tracing
            print("   ✅ Custom weave modules imported successfully")
        except ImportError as e:
            print(f"   ❌ Custom modules import failed: {e}")
            return False
            
        print("✅ Basic system test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic system test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🎯 Adventure System with Weave Evaluation Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Create environment template
    create_env_template()
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    # Check sample files
    files_ok = check_sample_files()
    
    # Run basic test
    test_ok = run_basic_test()
    
    # Summary
    print("\n📊 Setup Summary:")
    print("=" * 30)
    print(f"Dependencies: {'✅ Installed' if True else '❌ Failed'}")
    print(f"Environment: {'✅ Ready' if env_ok else '❌ Missing keys'}")
    print(f"Sample files: {'✅ Ready' if files_ok else '❌ Missing files'}")
    print(f"System test: {'✅ Passed' if test_ok else '❌ Failed'}")
    
    if env_ok and files_ok and test_ok:
        print("\n🎉 Setup Complete!")
        print("You can now run:")
        print("   python run_adventure_demo.py          # Run demo")
        print("   python evaluate_adventure_system.py   # Run evaluations")
        print("\n🔍 Check the Weave dashboard at https://wandb.ai/ for traces and metrics")
    else:
        print("\n⚠️  Setup incomplete. Please address the issues above.")
        if not env_ok:
            print("   1. Set your API keys in .env file")
        if not files_ok:
            print("   2. Make sure sample_transcript.txt exists")
        if not test_ok:
            print("   3. Check that all dependencies are installed correctly")

if __name__ == "__main__":
    main() 