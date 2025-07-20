#!/usr/bin/env python3
"""
Coding Agent - Implements code based on requests, writes tests, and ensures tests pass
"""

from typing import List
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import subprocess
import os


class CodingAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self):
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
        
        @tool
        def list_files(directory: str = ".") -> str:
            """List files in a directory"""
            try:
                files = os.listdir(directory)
                return f"Files in {directory}: {', '.join(files)}"
            except Exception as e:
                return f"Error listing files: {str(e)}"
        
        @tool
        def read_file(filename: str) -> str:
            """Read contents of a file"""
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                return f"Contents of {filename}:\n{content}"
            except Exception as e:
                return f"Error reading file: {str(e)}"
        
        tools = [write_code_file, write_test_file, run_tests, run_python_code, list_files, read_file]
        
        return create_react_agent(
            self.llm,
            tools
        )
    
    def process_request(self, request: str) -> str:
        """Process a coding request"""
        try:
            from langchain_core.messages import HumanMessage
            response = self.agent.invoke({"messages": [HumanMessage(content=request)]})
            return response['messages'][-1].content
        except Exception as e:
            return f"Error processing coding request: {str(e)}"
