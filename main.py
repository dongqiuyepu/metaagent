#!/usr/bin/env python3
"""
AI Agent System with Coding, CI, and Planner agents using LangGraph
"""

from langchain_openai import ChatOpenAI
from coding_agent import CodingAgent
from ci_agent import CIAgent
from planner_agent import PlannerAgent


class AgentSystem:
    def __init__(self):
        api_key = "sk-08769ff2aa534998a0c42fe6c825d7bf"
        base_url = "https://api.deepseek.com/"
        model = "deepseek-chat"
        
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url
        )
        
        self.coding_agent = CodingAgent(self.llm)
        self.ci_agent = CIAgent(self.llm)
        self.planner_agent = PlannerAgent(self.llm, self.coding_agent, self.ci_agent)
    
    def process_request(self, request: str) -> str:
        """Process a request through the planner agent which coordinates the team"""
        try:
            return self.planner_agent.process_request(request)
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def get_coding_agent(self) -> CodingAgent:
        """Get direct access to the coding agent"""
        return self.coding_agent
    
    def get_ci_agent(self) -> CIAgent:
        """Get direct access to the CI agent"""
        return self.ci_agent
    
    def get_planner_agent(self) -> PlannerAgent:
        """Get direct access to the planner agent"""
        return self.planner_agent

def main():
    """Main function to run the AI agent system"""
    print("🤖 AI Agent System Starting...")
    print("=" * 50)
    
    print("🔧 Using DeepSeek API for LLM functionality")
    
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
