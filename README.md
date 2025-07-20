# AI Agent System

A multi-agent system built with LangGraph that includes:

1. **Coding Agent**: Takes coding requests, implements code, writes tests, and ensures tests run successfully
2. **CI Agent**: Sets up GitHub Actions pipeline, builds codebase, and publishes artifacts to GitHub central repository  
3. **Planner Agent**: Routes requests to the appropriate agent (coding or CI)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. Run the system:
```bash
python main.py
```

## Usage

The system accepts natural language requests and automatically routes them to the appropriate agent:

- Coding requests: "Implement a function to calculate fibonacci numbers"
- CI requests: "Set up GitHub Actions for this Python project"

## Architecture

The system uses LangGraph's high-level agent API with three specialized agents that coordinate through a planner agent.
