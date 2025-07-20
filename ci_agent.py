#!/usr/bin/env python3
"""
CI Agent - Sets up GitHub Actions workflows, creates build scripts, and configures CI/CD pipelines
"""

from typing import List
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pathlib import Path
import os


class CIAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self):
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
        
        @tool
        def create_requirements_file(content: str) -> str:
            """Create or update requirements.txt file"""
            try:
                with open("requirements.txt", 'w') as f:
                    f.write(content)
                return "Successfully created/updated requirements.txt"
            except Exception as e:
                return f"Error creating requirements file: {str(e)}"
        
        @tool
        def create_setup_py(content: str) -> str:
            """Create setup.py for package distribution"""
            try:
                with open("setup.py", 'w') as f:
                    f.write(content)
                return "Successfully created setup.py"
            except Exception as e:
                return f"Error creating setup.py: {str(e)}"
        
        @tool
        def list_workflow_files() -> str:
            """List existing GitHub workflow files"""
            try:
                workflow_dir = Path(".github/workflows")
                if not workflow_dir.exists():
                    return "No .github/workflows directory found"
                
                workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
                if not workflow_files:
                    return "No workflow files found in .github/workflows"
                
                return f"Existing workflow files: {[f.name for f in workflow_files]}"
            except Exception as e:
                return f"Error listing workflow files: {str(e)}"
        
        tools = [create_github_workflow, create_dockerfile, create_build_script, 
                validate_workflow_syntax, create_requirements_file, create_setup_py, list_workflow_files]
        
        return create_react_agent(
            self.llm,
            tools
        )
    
    def process_request(self, request: str) -> str:
        """Process a CI/CD request"""
        try:
            from langchain_core.messages import HumanMessage
            response = self.agent.invoke({"messages": [HumanMessage(content=request)]})
            return response['messages'][-1].content
        except Exception as e:
            return f"Error processing CI request: {str(e)}"
