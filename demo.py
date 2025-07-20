#!/usr/bin/env python3
"""
Demo script to showcase the AI Agent System capabilities
"""

import os
import sys
from main import AgentSystem

def run_demo():
    """Run a demonstration of the AI Agent System"""
    print("🎯 AI Agent System Demo")
    print("=" * 50)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set your Anthropic API key to run the demo:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        return False
    
    try:
        print("🚀 Initializing agent system...")
        agent_system = AgentSystem()
        print("✅ Agent system ready!")
        
        demo_requests = [
            {
                "type": "Coding Request",
                "request": "Implement a Python function to calculate the fibonacci sequence up to n terms, and write tests for it",
                "description": "This should be routed to the coding agent"
            },
            {
                "type": "CI Request", 
                "request": "Create a GitHub Actions workflow that runs Python tests and publishes the package to PyPI",
                "description": "This should be routed to the CI agent"
            }
        ]
        
        for i, demo in enumerate(demo_requests, 1):
            print(f"\n📋 Demo {i}: {demo['type']}")
            print(f"Description: {demo['description']}")
            print(f"Request: {demo['request']}")
            print("-" * 50)
            
            print("🤖 Processing...")
            response = agent_system.process_request(demo['request'])
            
            print(f"📤 Response:\n{response}")
            print("\n" + "=" * 50)
        
        print("✅ Demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
