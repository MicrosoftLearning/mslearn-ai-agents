"""
Writer Agent Service - Port 5002
Runs writer agent as an HTTP service for A2A communication
"""

from agent_service import AgentService

def main():
    print("=" * 70)
    print("  WRITER AGENT SERVICE")
    print("=" * 70)
    
    agent = AgentService(
        agent_name="writer-agent-a2a",
        instructions="""You are a Writer Agent specializing in content creation.
        
        Your role:
        - Take research data and create polished content
        - Write 2-3 clear, engaging paragraphs
        - Maintain professional tone
        - Synthesize key points effectively
        
        Return publication-ready content.""",
        port=5002
    )
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down writer agent...")
        agent.cleanup()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
