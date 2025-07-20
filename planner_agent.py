#!/usr/bin/env python3
"""
Planner Agent - Routes requests to appropriate agents and coordinates the team
"""

from typing import List, TYPE_CHECKING
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

if TYPE_CHECKING:
    from coding_agent import CodingAgent
    from ci_agent import CIAgent


class PlannerAgent:
    def __init__(self, llm: ChatOpenAI, coding_agent: 'CodingAgent', ci_agent: 'CIAgent'):
        self.llm = llm
        self.coding_agent = coding_agent
        self.ci_agent = ci_agent
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the planner agent that routes requests to appropriate agents"""
        
        @tool
        def route_to_coding_agent(request: str) -> str:
            """Route a request to the coding agent"""
            try:
                response = self.coding_agent.process_request(request)
                return f"Coding agent response: {response}"
            except Exception as e:
                return f"Error routing to coding agent: {str(e)}"
        
        @tool
        def route_to_ci_agent(request: str) -> str:
            """Route a request to the CI agent"""
            try:
                response = self.ci_agent.process_request(request)
                return f"CI agent response: {response}"
            except Exception as e:
                return f"Error routing to CI agent: {str(e)}"
        
        @tool
        def analyze_request_type(request: str) -> str:
            """Analyze the type of request to determine routing"""
            coding_keywords = [
                "implement", "code", "function", "class", "algorithm", "program",
                "script", "develop", "write code", "programming", "debug", "fix bug",
                "create function", "write script", "python code", "test", "unit test"
            ]
            
            ci_keywords = [
                "ci", "cd", "github actions", "workflow", "build", "deploy", 
                "pipeline", "continuous integration", "docker", "test automation",
                "publish", "artifact", "release", "deployment", "devops", "automation"
            ]
            
            request_lower = request.lower()
            
            coding_score = sum(1 for keyword in coding_keywords if keyword in request_lower)
            ci_score = sum(1 for keyword in ci_keywords if keyword in request_lower)
            
            analysis = f"Request analysis:\n"
            analysis += f"- Coding keywords found: {coding_score}\n"
            analysis += f"- CI/CD keywords found: {ci_score}\n"
            
            if ci_score > coding_score:
                analysis += "- Recommendation: Route to CI Agent"
                return "CI_REQUEST"
            elif coding_score > 0:
                analysis += "- Recommendation: Route to Coding Agent"
                return "CODING_REQUEST"
            else:
                analysis += "- Recommendation: Unclear request type"
                return "UNCLEAR_REQUEST"
        
        @tool
        def coordinate_agents(request: str) -> str:
            """Coordinate multiple agents for complex requests"""
            try:
                request_lower = request.lower()
                
                needs_coding = any(keyword in request_lower for keyword in 
                                 ["implement", "code", "function", "script", "program"])
                needs_ci = any(keyword in request_lower for keyword in 
                              ["ci", "workflow", "deploy", "pipeline", "build"])
                
                if needs_coding and needs_ci:
                    coding_response = self.coding_agent.process_request(request)
                    ci_response = self.ci_agent.process_request(request)
                    
                    return f"Coordinated response:\n\nCoding Agent:\n{coding_response}\n\nCI Agent:\n{ci_response}"
                else:
                    return "Single agent coordination not needed for this request"
                    
            except Exception as e:
                return f"Error coordinating agents: {str(e)}"
        
        tools = [route_to_coding_agent, route_to_ci_agent, analyze_request_type, coordinate_agents]
        
        return create_react_agent(
            self.llm,
            tools
        )
    
    def process_request(self, request: str) -> str:
        """Process a request through the planner agent"""
        try:
            from langchain_core.messages import HumanMessage
            response = self.agent.invoke({"messages": [HumanMessage(content=request)]})
            return response['messages'][-1].content
        except Exception as e:
            return f"Error processing request: {str(e)}"
