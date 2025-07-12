# W&B Weave Quickstart

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
