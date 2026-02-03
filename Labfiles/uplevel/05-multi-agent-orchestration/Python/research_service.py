"""
Research Agent Service - Port 5001
Runs research agent as an HTTP service for A2A communication
"""

from agent_service import AgentService

def main():
    print("=" * 70)
    print("  RESEARCH AGENT SERVICE")
    print("=" * 70)
    
    agent = AgentService(
        agent_name="research-agent-a2a",
        instructions="""You are a Research Agent specializing in gathering information.
        
        Your role:
        - Research topics thoroughly
        - Identify 5-7 key findings
        - Provide structured, bulleted research data
        - Focus on facts and insights
        
        Return your research as a clear, bulleted list.""",
        port=5001
    )
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down research agent...")
        agent.cleanup()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
