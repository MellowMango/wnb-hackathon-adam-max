#!/usr/bin/env python3
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
    print("\n🎉 Check your W&B dashboard to see the trace!")

if __name__ == "__main__":
    main()
