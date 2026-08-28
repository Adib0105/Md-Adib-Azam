# Responsible AI Checklist

Evaluate an AI workflow for transparency, privacy, bias and human oversight.

## Validate prompt construction (no model required)

    python ../workflow_runner.py . --dry-run

## Run with local Ollama

    ollama pull llama3.2
    python ../workflow_runner.py .

No API key or secret is required. The sample data is synthetic; review model output before use.
