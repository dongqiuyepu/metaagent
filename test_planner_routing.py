#!/usr/bin/env python3
"""
Test script to verify the planner agent routing functionality
"""

import os

def test_planner_routing():
    """Test the planner agent's routing logic"""
    print("🧠 Testing Planner Agent Routing...")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set - skipping agent test")
        return False
    
    try:
        from main import AgentSystem
        
        agent_system = AgentSystem()
        
        test_cases = [
            {
                "request": "Implement a function to calculate prime numbers",
                "expected_agent": "coding",
                "description": "Should route to coding agent"
            },
            {
                "request": "Set up GitHub Actions for continuous integration",
                "expected_agent": "ci",
                "description": "Should route to CI agent"
            },
            {
                "request": "Create a workflow that builds and deploys the application",
                "expected_agent": "ci", 
                "description": "Should route to CI agent"
            },
            {
                "request": "Write a Python script to parse JSON files",
                "expected_agent": "coding",
                "description": "Should route to coding agent"
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test Case {i}: {test_case['description']}")
            print(f"Request: {test_case['request']}")
            
            try:
                response = agent_system.process_request(test_case['request'])
                
                response_lower = response.lower()
                
                if "coding agent" in response_lower or "implement" in response_lower:
                    detected_agent = "coding"
                elif "ci agent" in response_lower or "workflow" in response_lower or "github" in response_lower:
                    detected_agent = "ci"
                else:
                    detected_agent = "unknown"
                
                success = detected_agent == test_case['expected_agent']
                results.append(success)
                
                print(f"Expected: {test_case['expected_agent']} agent")
                print(f"Detected: {detected_agent} agent")
                print(f"Result: {'✅ PASS' if success else '❌ FAIL'}")
                print(f"Response preview: {response[:150]}...")
                
            except Exception as e:
                print(f"❌ Test case failed: {str(e)}")
                results.append(False)
        
        passed = sum(results)
        total = len(results)
        print(f"\n📊 Routing Test Summary: {passed}/{total} tests passed")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Planner routing test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_planner_routing()
    exit(0 if success else 1)
