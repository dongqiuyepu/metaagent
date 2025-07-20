#!/usr/bin/env python3
"""
Test script to verify the coding agent functionality
"""

import os
import tempfile
import shutil
from pathlib import Path

def test_coding_agent():
    """Test the coding agent with a simple coding request"""
    print("🧪 Testing Coding Agent...")
    
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
        
        coding_request = """
        Implement a Python function called 'fibonacci' that takes a number n and returns the nth fibonacci number.
        Also write comprehensive tests for this function and run them to make sure they pass.
        """
        
        print("📝 Sending coding request to planner agent...")
        response = agent_system.process_request(coding_request)
        
        print("✅ Coding agent test completed!")
        print(f"Response length: {len(response)} characters")
        print(f"Response preview: {response[:200]}...")
        
        py_files = list(Path('.').glob('*.py'))
        print(f"📄 Python files created: {[f.name for f in py_files]}")
        
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Coding agent test failed: {str(e)}")
        try:
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)
        except:
            pass
        return False

if __name__ == "__main__":
    success = test_coding_agent()
    exit(0 if success else 1)
