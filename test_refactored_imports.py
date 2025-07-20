#!/usr/bin/env python3
"""
Test script to verify the refactored agent system imports and works correctly
"""

def test_imports():
    """Test that all agent classes can be imported successfully"""
    print("🔍 Testing imports...")
    
    try:
        from coding_agent import CodingAgent
        print("✅ CodingAgent imported successfully")
    except Exception as e:
        print(f"❌ Failed to import CodingAgent: {e}")
        return False
    
    try:
        from ci_agent import CIAgent
        print("✅ CIAgent imported successfully")
    except Exception as e:
        print(f"❌ Failed to import CIAgent: {e}")
        return False
    
    try:
        from planner_agent import PlannerAgent
        print("✅ PlannerAgent imported successfully")
    except Exception as e:
        print(f"❌ Failed to import PlannerAgent: {e}")
        return False
    
    try:
        from main import AgentSystem
        print("✅ AgentSystem imported successfully")
    except Exception as e:
        print(f"❌ Failed to import AgentSystem: {e}")
        return False
    
    return True

def test_system_initialization():
    """Test that the agent system can be initialized"""
    print("\n🚀 Testing system initialization...")
    
    try:
        from main import AgentSystem
        agent_system = AgentSystem()
        print("✅ AgentSystem initialized successfully")
        
        coding_agent = agent_system.get_coding_agent()
        ci_agent = agent_system.get_ci_agent()
        planner_agent = agent_system.get_planner_agent()
        
        print("✅ All agents accessible through AgentSystem")
        print(f"✅ Coding agent type: {type(coding_agent).__name__}")
        print(f"✅ CI agent type: {type(ci_agent).__name__}")
        print(f"✅ Planner agent type: {type(planner_agent).__name__}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize AgentSystem: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Refactored Agent System...")
    print("=" * 50)
    
    import_success = test_imports()
    init_success = test_system_initialization()
    
    if import_success and init_success:
        print("\n🎉 All tests passed! Refactored system works correctly.")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        exit(1)
