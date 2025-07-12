#!/usr/bin/env python3
"""
Minimalist setup script for W&B Weave integration
"""

import subprocess
import sys
import os

def install_weave():
    """Install the weave package"""
    print("Installing W&B Weave...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "weave"])
        print("✅ Weave installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install weave: {e}")
        sys.exit(1)

def create_example_script():
    """Create a basic example script"""
    example_content = '''#!/usr/bin/env python3
"""
Basic Weave example script
"""

import weave
import os

# Set your W&B API key as an environment variable
# export WANDB_API_KEY="your-api-key-here"

@weave.op()
def hello_weave(name: str) -> str:
    """Simple function to test weave tracking"""
    return f"Hello {name}! Weave is tracking this function."

def main():
    # Initialize weave project
    # Replace 'my-weave-project' with your desired project name
    weave.init('my-weave-project')
    
    # Call tracked function
    result = hello_weave("World")
    print(result)
    print("\\n🎉 Check your W&B dashboard to see the trace!")

if __name__ == "__main__":
    main()
'''
    
    with open("weave_example.py", "w") as f:
        f.write(example_content)
    
    print("✅ Created weave_example.py")

def create_requirements():
    """Create requirements.txt"""
    requirements = """weave>=0.50.0
"""
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✅ Created requirements.txt")

def create_readme():
    """Create basic README"""
    readme_content = """# W&B Weave Quickstart

This project demonstrates basic usage of W&B Weave for tracking LLM calls and application logic.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your W&B API key:**
   - Create account at https://wandb.ai
   - Get your API key from https://wandb.ai/authorize
   - Set it as an environment variable:
     ```bash
     export WANDB_API_KEY="your-api-key-here"
     ```

3. **Run the example:**
   ```bash
   python weave_example.py
   ```

## Next Steps

- Add `@weave.op()` decorator to functions you want to track
- Integrate with OpenAI, Anthropic, or other LLM providers
- Check the W&B dashboard to see your traces

## Documentation

- [W&B Weave Quickstart](https://weave-docs.wandb.ai/quickstart)
- [W&B Weave Documentation](https://weave-docs.wandb.ai/)
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("✅ Created README.md")

def main():
    print("🚀 Setting up W&B Weave project...")
    
    install_weave()
    create_requirements()
    create_example_script()
    create_readme()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Get your W&B API key from https://wandb.ai/authorize")
    print("2. Set it as environment variable: export WANDB_API_KEY='your-key'")
    print("3. Run: python weave_example.py")

if __name__ == "__main__":
    main() 