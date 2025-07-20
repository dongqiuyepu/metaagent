#!/usr/bin/env python3
"""
AI Agent System with Coding, CI, and Planner agents using LangGraph
"""

import os
from typing import Dict, Any, List
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import subprocess
import tempfile
import shutil
from pathlib import Path
import git
import json


class AgentSystem:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
        
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=api_key
        )
        
        self.coding_agent = self._create_coding_agent()
        self.ci_agent = self._create_ci_agent()
        self.planner_agent = self._create_planner_agent()
    
    def _create_coding_agent(self):
        """Create the coding agent with tools for implementing and testing code"""
        
        @tool
        def write_code_file(filename: str, content: str) -> str:
            """Write code to a file"""
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                return f"Successfully wrote code to {filename}"
            except Exception as e:
                return f"Error writing file: {str(e)}"
        
        @tool
        def write_test_file(filename: str, content: str) -> str:
            """Write test code to a file"""
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                return f"Successfully wrote test to {filename}"
            except Exception as e:
                return f"Error writing test file: {str(e)}"
        
        @tool
        def run_tests(test_file: str) -> str:
            """Run tests using pytest"""
            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", test_file, "-v"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return f"Test results:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nReturn code: {result.returncode}"
            except subprocess.TimeoutExpired:
                return "Tests timed out after 30 seconds"
            except Exception as e:
                return f"Error running tests: {str(e)}"
        
        @tool
        def run_python_code(filename: str) -> str:
            """Execute Python code file"""
            try:
                result = subprocess.run(
                    ["python", filename],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                return f"Execution results:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nReturn code: {result.returncode}"
            except subprocess.TimeoutExpired:
                return "Code execution timed out after 10 seconds"
            except Exception as e:
                return f"Error executing code: {str(e)}"
        
        tools = [write_code_file, write_test_file, run_tests, run_python_code]
        
        return create_react_agent(
            self.llm,
            tools,
            state_modifier="You are a coding agent. Your job is to implement code based on requests, write comprehensive tests, and ensure the tests pass. Always write both the implementation and tests, then run the tests to verify they work."
        )
    
    def _create_ci_agent(self):
        """Create the CI agent with tools for setting up GitHub Actions"""
        
        @tool
        def create_github_workflow(workflow_name: str, workflow_content: str) -> str:
            """Create a GitHub Actions workflow file"""
            try:
                workflow_dir = Path(".github/workflows")
                workflow_dir.mkdir(parents=True, exist_ok=True)
                
                workflow_file = workflow_dir / f"{workflow_name}.yml"
                with open(workflow_file, 'w') as f:
                    f.write(workflow_content)
                
                return f"Successfully created GitHub workflow: {workflow_file}"
            except Exception as e:
                return f"Error creating workflow: {str(e)}"
        
        @tool
        def create_dockerfile(content: str) -> str:
            """Create a Dockerfile for containerized builds"""
            try:
                with open("Dockerfile", 'w') as f:
                    f.write(content)
                return "Successfully created Dockerfile"
            except Exception as e:
                return f"Error creating Dockerfile: {str(e)}"
        
        @tool
        def create_build_script(script_name: str, content: str) -> str:
            """Create a build script"""
            try:
                with open(script_name, 'w') as f:
                    f.write(content)
                os.chmod(script_name, 0o755)  # Make executable
                return f"Successfully created build script: {script_name}"
            except Exception as e:
                return f"Error creating build script: {str(e)}"
        
        @tool
        def validate_workflow_syntax(workflow_file: str) -> str:
            """Basic validation of GitHub Actions workflow syntax"""
            try:
                import yaml
                with open(workflow_file, 'r') as f:
                    yaml.safe_load(f)
                return f"Workflow {workflow_file} has valid YAML syntax"
            except yaml.YAMLError as e:
                return f"YAML syntax error in {workflow_file}: {str(e)}"
            except Exception as e:
                return f"Error validating workflow: {str(e)}"
        
        tools = [create_github_workflow, create_dockerfile, create_build_script, validate_workflow_syntax]
        
        return create_react_agent(
            self.llm,
            tools,
            state_modifier="You are a CI/CD agent. Your job is to set up GitHub Actions workflows, create build scripts, and configure continuous integration pipelines. Focus on creating robust, production-ready CI/CD configurations."
        )
    
    def _create_planner_agent(self):
        """Create the planner agent that routes requests to appropriate agents"""
        
        @tool
        def route_to_coding_agent(request: str) -> str:
            """Route a request to the coding agent"""
            try:
                response = self.coding_agent.invoke({"messages": [HumanMessage(content=request)]})
                return f"Coding agent response: {response['messages'][-1].content}"
            except Exception as e:
                return f"Error routing to coding agent: {str(e)}"
        
        @tool
        def route_to_ci_agent(request: str) -> str:
            """Route a request to the CI agent"""
            try:
                response = self.ci_agent.invoke({"messages": [HumanMessage(content=request)]})
                return f"CI agent response: {response['messages'][-1].content}"
            except Exception as e:
                return f"Error routing to CI agent: {str(e)}"
        
        @tool
        def analyze_request_type(request: str) -> str:
            """Analyze the type of request to determine routing"""
            coding_keywords = [
                "implement", "code", "function", "class", "algorithm", "program",
                "script", "develop", "write code", "programming", "debug", "fix bug"
            ]
            
            ci_keywords = [
                "ci", "cd", "github actions", "workflow", "build", "deploy", 
                "pipeline", "continuous integration", "docker", "test automation",
                "publish", "artifact", "release"
            ]
            
            request_lower = request.lower()
            
            coding_score = sum(1 for keyword in coding_keywords if keyword in request_lower)
            ci_score = sum(1 for keyword in ci_keywords if keyword in request_lower)
            
            if ci_score > coding_score:
                return "CI_REQUEST"
            elif coding_score > 0:
                return "CODING_REQUEST"
            else:
                return "UNCLEAR_REQUEST"
        
        tools = [route_to_coding_agent, route_to_ci_agent, analyze_request_type]
        
        return create_react_agent(
            self.llm,
            tools,
            state_modifier="You are a planner agent. Your job is to analyze incoming requests and route them to the appropriate agent (coding or CI). First analyze the request type, then route accordingly. For coding requests, use route_to_coding_agent. For CI/CD requests, use route_to_ci_agent."
        )
    
    def process_request(self, request: str) -> str:
        """Process a request through the planner agent"""
        try:
            response = self.planner_agent.invoke({"messages": [HumanMessage(content=request)]})
            return response['messages'][-1].content
        except Exception as e:
            return f"Error processing request: {str(e)}"

def main():
    """Main function to run the AI agent system"""
    print("🤖 AI Agent System Starting...")
    print("=" * 50)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set your Anthropic API key:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        return
    
    try:
        agent_system = AgentSystem()
        print("✅ Agent system initialized successfully!")
        print("\nAvailable agents:")
        print("  🔧 Coding Agent - Implements code and writes tests")
        print("  🚀 CI Agent - Sets up GitHub Actions and build pipelines")
        print("  🧠 Planner Agent - Routes requests to appropriate agents")
        print("\n" + "=" * 50)
        
        while True:
            print("\nEnter your request (or 'quit' to exit):")
            user_request = input("> ").strip()
            
            if user_request.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_request:
                continue
            
            print(f"\n🤔 Processing request: {user_request}")
            print("-" * 30)
            
            response = agent_system.process_request(user_request)
            print(f"\n🤖 Response:\n{response}")
            print("\n" + "=" * 50)
            
    except Exception as e:
        print(f"❌ Error initializing agent system: {str(e)}")
        return

if __name__ == "__main__":
    main()
