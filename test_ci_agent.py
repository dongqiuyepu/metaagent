#!/usr/bin/env python3
"""
Test script to verify the CI agent functionality
"""

import os
import tempfile
import shutil
from pathlib import Path

def test_ci_agent():
    """Test the CI agent with a GitHub Actions setup request"""
    print("🚀 Testing CI Agent...")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set - skipping agent test")
        return False
    
    try:
        from main import AgentSystem
        
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        print(f"📁 Testing in directory: {temp_dir}")
        
        agent_system = AgentSystem()
        
        ci_request = """
        Set up a GitHub Actions workflow for a Python project that:
        1. Runs on push and pull requests
        2. Tests the code with pytest
        3. Builds the package
        4. Publishes to PyPI on release
        Create the workflow file and any necessary build scripts.
        """
        
        print("📝 Sending CI request to planner agent...")
        response = agent_system.process_request(ci_request)
        
        print("✅ CI agent test completed!")
        print(f"Response length: {len(response)} characters")
        print(f"Response preview: {response[:200]}...")
        
        github_dir = Path('.github/workflows')
        if github_dir.exists():
            workflow_files = list(github_dir.glob('*.yml'))
            print(f"📄 Workflow files created: {[f.name for f in workflow_files]}")
        else:
            print("📄 No .github/workflows directory found")
        
        other_files = [f for f in Path('.').iterdir() if f.is_file()]
        print(f"📄 Other files created: {[f.name for f in other_files]}")
        
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ CI agent test failed: {str(e)}")
        try:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)
        except:
            pass
        return False

if __name__ == "__main__":
    success = test_ci_agent()
    exit(0 if success else 1)
