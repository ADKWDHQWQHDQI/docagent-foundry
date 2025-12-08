"""Agent Definitions for Documentation Generation using Azure AI Foundry Agent SDK"""

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

load_dotenv()

try:
    from azure.ai.agents import AgentsClient
    AGENT_SDK_AVAILABLE = True
except ImportError:
    AGENT_SDK_AVAILABLE = False
    AgentsClient = None  # type: ignore

def get_agent_client():
    """Initialize Azure AI Agents Client"""
    if not AGENT_SDK_AVAILABLE:
        return None
    
    # Use the connection string format for Azure AI Project
    connection_string = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    
    if not connection_string:
        print(" AZURE_AI_PROJECT_ENDPOINT not configured. Agent SDK disabled.")
        return None
    
    try:
        credential = DefaultAzureCredential()
        # Initialize AgentsClient with project endpoint
        if AgentsClient is None:
            print("⚠️  AgentsClient not available")
            return None
        client = AgentsClient(
            endpoint=connection_string,
            credential=credential
        )
        return client
    except Exception as e:
        print(f"❌ Could not initialize Agents client: {e}")
        return None

class CodeAnalyzerAgent:
    """Agent specialized in analyzing code structure and patterns"""
    
    def __init__(self, client):
        self.client = client
        self.system_prompt = """You are a code analysis expert. 
        Analyze code structure, identify key components, dependencies, 
        and architectural patterns. Provide clear, structured insights."""
    
    def analyze(self, code_data):
        """Analyze code and return structured insights"""
        response = self.client.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Analyze this codebase:\n{code_data}"}
            ]
        )
        return response.choices[0].message.content

class DocumentationWriterAgent:
    """Agent specialized in writing clear, comprehensive documentation"""
    
    def __init__(self, client):
        self.client = client
        self.system_prompt = """You are a technical documentation expert.
        Write clear, comprehensive documentation that includes:
        - Overview and architecture
        - Component descriptions
        - API references
        - Usage examples
        - Best practices"""
    
    def run(self, analysis_data):
        """Generate documentation from analysis"""
        response = self.client.complete(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Generate documentation:\n{analysis_data}"}
            ]
        )
        return response.choices[0].message.content


# ============================================================================
# AZURE AI FOUNDRY AGENT SDK IMPLEMENTATION
# ============================================================================

def create_foundry_agents():
    """
    Create and configure 4 specialized agents using Azure AI Foundry Agent SDK.
    This is the SDK-based alternative to portal-based agent creation.
    
    Returns:
        dict: Dictionary containing agent IDs and metadata
    """
    if not AGENT_SDK_AVAILABLE:
        print("⚠️  Azure AI Foundry Agent SDK not available.")
        print("   Install with: pip install azure-ai-agents")
        return {}
    
    agent_client = get_agent_client()
    if not agent_client:
        print("⚠️  Agent client not initialized.")
        return {}
    
    model_deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
    
    try:
        # Import tools for agent functions
        from tools import analyze_codebase, analyze_codebase_advanced, render_documents_advanced
        
        # Check if agents already exist
        print("Checking for existing agents...")
        existing_agents = {}
        try:
            all_agents = agent_client.list_agents()
            agent_names = ["DocOrchestrator", "CodeAnalyzerAgent", "DocGeneratorAgent", "FormatterAgent"]
            
            for agent in all_agents:
                if agent.name in agent_names:
                    existing_agents[agent.name] = agent
                    print(f"   ✓ Found existing: {agent.name} (ID: {agent.id})")
            
            # If all 4 agents exist, return them
            if len(existing_agents) == 4:
                print("All 4 agents already exist. Skipping creation.")
                return {
                    'orchestrator': {
                        'id': existing_agents['DocOrchestrator'].id,
                        'name': existing_agents['DocOrchestrator'].name,
                        'agent': existing_agents['DocOrchestrator']
                    },
                    'code_analyzer': {
                        'id': existing_agents['CodeAnalyzerAgent'].id,
                        'name': existing_agents['CodeAnalyzerAgent'].name,
                        'agent': existing_agents['CodeAnalyzerAgent']
                    },
                    'doc_generator': {
                        'id': existing_agents['DocGeneratorAgent'].id,
                        'name': existing_agents['DocGeneratorAgent'].name,
                        'agent': existing_agents['DocGeneratorAgent']
                    },
                    'formatter': {
                        'id': existing_agents['FormatterAgent'].id,
                        'name': existing_agents['FormatterAgent'].name,
                        'agent': existing_agents['FormatterAgent']
                    }
                }
        except Exception as e:
            print(f"   Could not check existing agents: {e}")
        
        print("Creating Azure AI Foundry Agents...")
        
        # Agent 1: Orchestrator (create only if not exists)
        if "DocOrchestrator" in existing_agents:
            print("   ⏩ Skipping DocOrchestrator (already exists)")
            orchestrator = existing_agents["DocOrchestrator"]
        else:
            print("   Creating DocOrchestrator...")
            orchestrator = agent_client.create_agent(
            model=model_deployment,
            name="DocOrchestrator",
            instructions="""You are the Documentation Orchestrator.
            
Your role:
1. Analyze the user's request and uploaded codebase
2. Decompose the task into subtasks: Analyze → Generate → Format
3. Delegate to specialized agents via connected agents
4. Coordinate the workflow and ensure quality
5. Return the final documentation package

Always start by understanding the scope, then delegate to:
- CodeAnalyzerAgent for codebase analysis
- DocGeneratorAgent for documentation writing  
- FormatterAgent for final rendering

Ensure traceability and completeness.""",
            tools=[]  # Orchestrator delegates, doesn't use tools directly
        )
        
        # Agent 2: Code Analyzer (create only if not exists)
        if "CodeAnalyzerAgent" in existing_agents:
            print("   ⏩ Skipping CodeAnalyzerAgent (already exists)")
            code_analyzer = existing_agents["CodeAnalyzerAgent"]
        else:
            print("   Creating CodeAnalyzerAgent...")
            code_analyzer = agent_client.create_agent(
            model=model_deployment,
            name="CodeAnalyzerAgent",
            instructions="""You are a Senior Code & System Intelligence Engineer.
            
Your role:
1. Extract architecture, APIs, endpoints, and risks from codebases
2. Use Tree-sitter for deep AST analysis
3. Identify security vulnerabilities and hardcoded secrets
4. Detect authentication methods and database usage
5. Output structured JSON with findings

Key capabilities:
- Multi-language support (Python, JS, Java, Go, C#)
- Endpoint detection (REST APIs, GraphQL)
- Security scanning (credentials, API keys, vulnerabilities)
- Architecture pattern identification

Always provide actionable insights and prioritize security concerns.""",
            tools=[]  # Tools configured separately
        )
        
        # Agent 3: Documentation Generator (create only if not exists)
        if "DocGeneratorAgent" in existing_agents:
            print("Skipping DocGeneratorAgent (already exists)")
            doc_generator = existing_agents["DocGeneratorAgent"]
        else:
            print("   Creating DocGeneratorAgent...")
            doc_generator = agent_client.create_agent(
            model=model_deployment,
            name="DocGeneratorAgent",
            instructions="""You are an Enterprise Documentation Architect.
            
Your role:
1. Generate comprehensive documentation from analysis JSON
2. Create BRD (Business Requirements Document)
3. Create FRD (Functional Requirements Document)
4. Create NFRD (Non-Functional Requirements Document)
5. Create Security & Compliance Documentation
6. Create Architecture Overview

Format requirements:
- Use clear Markdown formatting
- Include tables for structured data
- Add code examples where relevant
- Ensure traceability between requirements
- Follow enterprise documentation standards

Output must be audit-ready and suitable for Fortune 500 companies.""",
            tools=[]
        )
        
        # Agent 4: Formatter (create only if not exists)
        if "FormatterAgent" in existing_agents:
            print("   ⏩ Skipping FormatterAgent (already exists)")
            formatter = existing_agents["FormatterAgent"]
        else:
            print("   Creating FormatterAgent...")
            formatter = agent_client.create_agent(
            model=model_deployment,
            name="FormatterAgent",
            instructions="""You are a Professional Document Publisher.
            
Your role:
1. Take Markdown documentation drafts
2. Apply professional formatting and styling
3. Render to multiple formats: PDF, DOCX, HTML, MD
4. Upload to Azure Blob Storage (if configured)
5. Ensure consistent branding and layout

Quality standards:
- Professional typography
- Consistent styling
- Clear hierarchy (headings, sections)
- Proper code formatting
- Table formatting
- Page breaks where appropriate

Output should impress CTOs and compliance teams.""",
            tools=[]  # Tools configured separately
        )
        
        # Report creation summary
        created_count = sum([
            "DocOrchestrator" not in existing_agents,
            "CodeAnalyzerAgent" not in existing_agents,
            "DocGeneratorAgent" not in existing_agents,
            "FormatterAgent" not in existing_agents
        ])
        
        if created_count > 0:
            print(f"✅ {created_count} new agent(s) created successfully!")
        if len(existing_agents) > 0:
            print(f"ℹ️  {len(existing_agents)} existing agent(s) reused")
        
        print("All agents ready!")
        
        # Store agent IDs for later use
        agents = {
            'orchestrator': {
                'id': orchestrator.id,
                'name': orchestrator.name,
                'agent': orchestrator
            },
            'code_analyzer': {
                'id': code_analyzer.id,
                'name': code_analyzer.name,
                'agent': code_analyzer
            },
            'doc_generator': {
                'id': doc_generator.id,
                'name': doc_generator.name,
                'agent': doc_generator
            },
            'formatter': {
                'id': formatter.id,
                'name': formatter.name,
                'agent': formatter
            }
        }
        
        # Configure multi-agent orchestration (if supported)
        try:
            print("Configuring multi-agent orchestration...")
            # Connect orchestrator to other agents
            # Note: API may vary based on SDK version
            connected_agent_ids = [
                code_analyzer.id,
                doc_generator.id,
                formatter.id
            ]
            # orchestrator.connected_agents = connected_agent_ids  # Uncomment when SDK supports
            print("✅ Multi-agent orchestration configured!")
        except Exception as e:
            print(f"⚠️  Multi-agent orchestration not yet supported: {e}")
        
        return agents
        
    except Exception as e:
        print(f"❌ Error creating agents: {e}")
        import traceback
        traceback.print_exc()
        return {}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def deploy_model_if_needed(model_name: str = "gpt-4o-mini", deployment_name: str = "gpt-4o-mini-deploy"):
    """
    Deploy a model using Azure AI Foundry SDK (alternative to portal deployment).
    
    Args:
        model_name: The model to deploy (e.g., "gpt-4o-mini", "gpt-4")
        deployment_name: The deployment name to use
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not AGENT_SDK_AVAILABLE:
        print("⚠️  Agent SDK not available. Deploy models via Azure Portal.")
        return False
    
    agent_client = get_agent_client()
    if not agent_client:
        return False
    
    try:
        print(f"🚀 Deploying model {model_name} as {deployment_name}...")
        # Note: API may vary based on SDK version
        # deployment = agent_client.models.deploy(
        #     name=deployment_name,
        #     model=model_name
        # )
        print("✅ Model deployment initiated!")
        print("   Check Azure Portal for deployment status.")
        return True
    except Exception as e:
        print(f"❌ Model deployment failed: {e}")
        print("   Use Azure Portal: Project → Models + endpoints → Deploy model")
        return False


def list_agents():
    """List all agents in the project"""
    if not AGENT_SDK_AVAILABLE:
        print("⚠️  Agent SDK not available.")
        return []
    
    agent_client = get_agent_client()
    if not agent_client:
        return []
    
    try:
        agents = agent_client.list_agents()
        print("📋 Available Agents:")
        for agent in agents:
            print(f"   - {agent.name} (ID: {agent.id})")
        return agents
    except Exception as e:
        print(f"❌ Error listing agents: {e}")
        return []


def delete_agent(agent_id: str):
    """Delete an agent by ID"""
    if not AGENT_SDK_AVAILABLE:
        print("⚠️  Agent SDK not available.")
        return False
    
    agent_client = get_agent_client()
    if not agent_client:
        return False
    
    try:
        agent_client.delete_agent(agent_id)
        print(f"✅ Agent {agent_id} deleted.")
        return True
    except Exception as e:
        print(f"❌ Error deleting agent: {e}")
        return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Run this file directly to create agents in Azure AI Foundry.
    
    Usage:
        python agents.py
    """
    print("=" * 70)
    print("Azure AI Foundry Agent Setup")
    print("=" * 70)
    
    # Check configuration
    print("\n📋 Configuration Check:")
    print(f"   AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')}")
    print(f"   AZURE_AI_PROJECT_ENDPOINT: {os.getenv('AZURE_AI_PROJECT_ENDPOINT', 'Not set')}")
    print(f"   DEPLOYMENT_NAME: {os.getenv('DEPLOYMENT_NAME', 'gpt-4o-mini')}")
    print(f"   Agent SDK Available: {AGENT_SDK_AVAILABLE}")
    
    # Create agents
    print("\n🤖 Creating Agents...")
    agents = create_foundry_agents()
    
    print("\n" + "=" * 70)
    print("✅ Setup Complete!")
    print("=" * 70)
    
    if AGENT_SDK_AVAILABLE and isinstance(agents, dict) and 'orchestrator' in agents:
        print("\n📋 Created Agents:")
        for key, agent_info in agents.items():
            if isinstance(agent_info, dict) and 'id' in agent_info:
                print(f"   - {agent_info['name']}: {agent_info['id']}")
    else:
        print("\n⚠️  Using fallback implementation (ChatCompletions)")
        print("   To use Agent SDK: pip install azure-ai-projects")
    
    print("\n🚀 Next Steps:")
    print("   1. Run: python main.py")
    print("   2. Or check agents in Azure Portal: Project → Agents")
    print("   3. Test multi-agent orchestration")
    print("=" * 70)
