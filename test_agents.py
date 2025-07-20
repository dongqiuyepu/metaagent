#!/usr/bin/env python3
"""
Test suite for the AI Agent System
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from main import AgentSystem

class TestAgentSystem:
    """Test cases for the AI Agent System"""
    
    @pytest.fixture
    def agent_system(self):
        """Create an agent system instance for testing"""
        if not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("ANTHROPIC_API_KEY not set")
        
        return AgentSystem()
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
    
    def test_agent_system_initialization(self, agent_system):
        """Test that the agent system initializes correctly"""
        assert agent_system.coding_agent is not None
        assert agent_system.ci_agent is not None
        assert agent_system.planner_agent is not None
    
    def test_coding_request_routing(self, agent_system, temp_dir):
        """Test that coding requests are routed correctly"""
        request = "Implement a simple function to add two numbers"
        response = agent_system.process_request(request)
        
        assert "coding" in response.lower() or "function" in response.lower()
        assert response is not None
        assert len(response) > 0
    
    def test_ci_request_routing(self, agent_system, temp_dir):
        """Test that CI requests are routed correctly"""
        request = "Set up a GitHub Actions workflow for Python testing"
        response = agent_system.process_request(request)
        
        assert "workflow" in response.lower() or "github" in response.lower() or "ci" in response.lower()
        assert response is not None
        assert len(response) > 0
    
    def test_request_analysis(self, agent_system):
        """Test the request analysis functionality"""
        coding_request = "Write a Python function to calculate factorial"
        ci_request = "Create a GitHub Actions workflow for continuous integration"
        
        coding_response = agent_system.process_request(coding_request)
        ci_response = agent_system.process_request(ci_request)
        
        assert coding_response is not None
        assert ci_response is not None
        assert len(coding_response) > 0
        assert len(ci_response) > 0

def test_basic_functionality():
    """Basic test that doesn't require API key"""
    from main import AgentSystem
    from coding_agent import CodingAgent
    from ci_agent import CIAgent
    from planner_agent import PlannerAgent
    
    assert hasattr(AgentSystem, '__init__')
    assert hasattr(AgentSystem, 'process_request')
    assert hasattr(AgentSystem, 'get_coding_agent')
    assert hasattr(AgentSystem, 'get_ci_agent')
    assert hasattr(AgentSystem, 'get_planner_agent')
    
    assert hasattr(CodingAgent, '__init__')
    assert hasattr(CodingAgent, 'process_request')
    assert hasattr(CIAgent, '__init__')
    assert hasattr(CIAgent, 'process_request')
    assert hasattr(PlannerAgent, '__init__')
    assert hasattr(PlannerAgent, 'process_request')
    
    print("✅ Refactored AgentSystem structure is correct")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
