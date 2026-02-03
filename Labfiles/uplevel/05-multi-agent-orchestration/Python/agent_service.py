"""
Generic Agent Service for A2A Communication
Wraps a Foundry agent as an HTTP service using Flask
"""

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()

class AgentService:
    def __init__(self, agent_name, instructions, port):
        """Initialize agent service."""
        self.agent_name = agent_name
        self.instructions = instructions
        self.port = port
        
        # Connect to Foundry
        self.project_endpoint = os.getenv("PROJECT_ENDPOINT")
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
        
        print(f"🔌 Connecting to Foundry...")
        self.credential = DefaultAzureCredential()
        self.project_client = AIProjectClient(
            credential=self.credential,
            endpoint=self.project_endpoint
        )
        self.openai_client = self.project_client.get_openai_client()
        
        # Create agent version
        print(f"🤖 Creating agent: {agent_name}")
        self.agent = self.openai_client.agents.create_version(
            agent_name=agent_name,
            definition={
                "kind": "prompt",
                "model": self.model_deployment,
                "instructions": instructions
            }
        )
        print(f"✅ Agent ready (v{self.agent.version})")
        
        # Create Flask app
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup HTTP routes."""
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return jsonify({
                "status": "healthy",
                "agent": self.agent_name,
                "version": self.agent.version
            })
        
        @self.app.route('/invoke', methods=['POST'])
        def invoke():
            """Invoke agent with a task."""
            try:
                data = request.json
                task = data.get('task', '')
                
                if not task:
                    return jsonify({"error": "No task provided"}), 400
                
                print(f"\n📨 Received task: {task[:50]}...")
                
                # Create conversation
                conversation = self.openai_client.conversations.create(
                    items=[{
                        "type": "message",
                        "role": "user",
                        "content": task
                    }]
                )
                
                # Get response
                response = self.openai_client.responses.create(
                    conversation=conversation.id,
                    extra_body={
                        "agent": {
                            "type": "agent_reference",
                            "name": self.agent.name,
                            "version": self.agent.version
                        }
                    }
                )
                
                # Extract result
                result = ""
                for item in response.output:
                    if item.type == "message":
                        for content in item.content:
                            if hasattr(content, 'text'):
                                result = content.text
                                break
                
                print(f"✅ Task complete")
                
                return jsonify({
                    "status": "success",
                    "agent": self.agent_name,
                    "result": result
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                return jsonify({
                    "status": "error",
                    "error": str(e)
                }), 500
    
    def run(self):
        """Start the Flask service."""
        print(f"\n🚀 Starting {self.agent_name} on port {self.port}")
        print(f"📍 Endpoints:")
        print(f"   • Health: http://localhost:{self.port}/health")
        print(f"   • Invoke: http://localhost:{self.port}/invoke")
        print(f"\nPress Ctrl+C to stop\n")
        
        self.app.run(host='0.0.0.0', port=self.port, debug=False)
    
    def cleanup(self):
        """Cleanup agent version."""
        try:
            self.openai_client.agents.delete_version(
                agent_name=self.agent.name,
                version=self.agent.version
            )
            print(f"✅ Cleaned up {self.agent_name}")
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")

def main():
    """Main entry point - not used directly, see research_service.py and writer_service.py"""
    print("This is a base class. Use research_service.py or writer_service.py instead.")

if __name__ == "__main__":
    main()
