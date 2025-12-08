"""
Main Orchestration Script for Documentation Agent Workflow
Orchestrates the 4-agent system: DocOrchestrator → CodeAnalyzer → DocGenerator → Formatter
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

# Import agent utilities
from agents import create_foundry_agents, get_agent_client, AGENT_SDK_AVAILABLE
from tools import analyze_codebase_advanced, render_documents_advanced

# Check SDK availability
if AGENT_SDK_AVAILABLE:
    from azure.ai.agents import AgentsClient
    from azure.ai.agents.models import ThreadMessage, MessageRole
else:
    AgentsClient = None  # type: ignore
    ThreadMessage = None  # type: ignore
    MessageRole = None  # type: ignore


def run_docagent_workflow(prompt: str, codebase_path: str | None = None):
    """
    Run the complete documentation generation workflow.
    
    Args:
        prompt: User request describing what documentation to generate
        codebase_path: Path to the codebase to analyze (optional)
        
    Returns:
        dict: Results containing generated documentation and metadata
    """
    print("\n" + "=" * 70)
    print("🚀 Documentation Agent Workflow - Starting")
    print("=" * 70)
    
    if not AGENT_SDK_AVAILABLE:
        print("\n⚠️  Azure AI Foundry Agent SDK not available.")
        print("   Falling back to direct tool execution...\n")
        return run_fallback_workflow(prompt, codebase_path)
    
    # Initialize agents
    print("\n📋 Step 1: Initializing Agents...")
    agents = create_foundry_agents()
    
    if not isinstance(agents, dict) or 'orchestrator' not in agents:
        print("⚠️  Could not initialize agents. Using fallback.")
        return run_fallback_workflow(prompt, codebase_path)
    
    agent_client = get_agent_client()
    if not agent_client:
        print("⚠️  Could not connect to Agent client. Using fallback.")
        return run_fallback_workflow(prompt, codebase_path)
    
    orchestrator_id = agents['orchestrator']['id']
    
    try:
        # Step 2: Create thread and process run (polls automatically until complete)
        print("\n💬 Step 2: Creating thread and running agent (auto-polling)...")
        
        user_message = f"""{prompt}

Codebase: {codebase_path or 'Template mode - no codebase provided'}

Generate comprehensive documentation with BRD, FRD, NFRD, Security docs, and Architecture overview."""
        
        print(f"   Using agent: DocOrchestrator ({orchestrator_id})")
        
        # Use create_thread_and_process_run - it creates thread, adds message, runs agent, and polls
        from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions
        
        thread_options = AgentThreadCreationOptions(
            messages=[ThreadMessageOptions(role="user", content=user_message)]
        )
        
        # This method handles everything: thread creation, message, run, and polling
        run = agent_client.create_thread_and_process_run(
            agent_id=orchestrator_id,
            thread=thread_options
        )
        
        print(f"   Thread: {run.thread_id}")
        print(f"   Run: {run.id}")
        print(f"   Status: {run.status}")
        
        if run.status != "completed":
            print(f"\n⚠️  Run did not complete. Status: {run.status}")
            if hasattr(run, 'last_error') and run.last_error:
                print(f"   Error: {run.last_error}")
            return {"status": "failed", "error": run.status}
        
        # Step 3: Retrieve messages from completed thread
        print("\n📥 Step 3: Retrieving documentation...")
        
        # Get the last assistant message
        last_message_obj = agent_client.messages.get_last_message_text_by_role(
            thread_id=run.thread_id,
            role="assistant"  # type: ignore
        )
        
        if not last_message_obj:
            print("⚠️  No assistant response found")
            return {"status": "no_output"}
        
        # Extract text - it's a MessageTextContent with .text attribute
        if hasattr(last_message_obj, 'text'):
            text_obj = last_message_obj.text  # type: ignore
            doc = text_obj.value if hasattr(text_obj, 'value') else str(text_obj)
        else:
            doc = str(last_message_obj)
        
        print(f"   ✅ Retrieved {len(doc)} chars")
        print(f"\n📄 Preview:\n{'-'*70}\n{doc[:300]}...\n{'-'*70}")
        
        # Step 4: Render documents
        rendered = []
        print("\n🎨 Step 4: Rendering documents...")
        try:
            rendered = render_documents_advanced(doc, "./outputs")
            print(f"   ✅ Rendered {len(rendered)} file(s)")
            for f in rendered:
                print(f"      - {f}")
        except Exception as e:
            print(f"   ⚠️  Render error: {e}")
        
        print("\n" + "=" * 70)
        print("✅ Documentation Complete!")
        print("=" * 70)
        
        return {
            "status": "success",
            "thread_id": run.thread_id,
            "run_id": run.id,
            "documentation": doc,
            "rendered_files": rendered,
            "preview": doc[:500]
        }
        
    except Exception as e:
        print(f"\n❌ Error in workflow: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}


def run_fallback_workflow(prompt: str, codebase_path: str | None = None):
    """
    Fallback workflow when Agent SDK is not available.
    Uses direct tool calls instead of agent orchestration.
    """
    print("=" * 70)
    print("📋 Running Fallback Workflow (Direct Tool Execution)")
    print("=" * 70)
    
    results = {
        "status": "success_fallback",
        "documentation": "",
        "analysis": None,
        "rendered_files": []
    }
    
    try:
        # Step 1: Analyze codebase
        if codebase_path and os.path.exists(codebase_path):
            print(f"\n🔍 Step 1: Analyzing codebase at {codebase_path}...")
            analysis = analyze_codebase_advanced(codebase_path)
            analysis_dict = analysis if isinstance(analysis, dict) else {}
            results["analysis"] = analysis
            print(f"   ✅ Analysis complete: {len(analysis_dict.get('files', []))} files analyzed")
        else:
            print("\n⏩ Step 1: Skipping codebase analysis (no path provided)")
            analysis_dict = {"files": [], "structure": {}, "security_findings": []}
        
        # Step 2: Generate documentation
        print("\n📝 Step 2: Generating documentation...")
        documentation = f"""# Documentation Package

## Project Overview
Generated based on: {prompt}

## Business Requirements Document (BRD)

### Executive Summary
This document outlines the business requirements for the system.

### Stakeholders
- Development Team
- Product Management
- Quality Assurance
- Security Team

### Business Objectives
1. Deliver high-quality documentation
2. Ensure comprehensive coverage
3. Maintain security standards
4. Enable efficient onboarding

## Functional Requirements Document (FRD)

### System Architecture
{"Architecture based on analyzed codebase" if analysis_dict.get('files') else "Template architecture - customize based on your system"}

### Core Features
1. **Feature 1**: Description
2. **Feature 2**: Description
3. **Feature 3**: Description

### API Endpoints
{f"Detected {len(analysis_dict.get('api_endpoints', []))} API endpoints" if analysis_dict.get('api_endpoints') else "Define your API endpoints here"}

## Non-Functional Requirements Document (NFRD)

### Performance Requirements
- Response Time: < 200ms for API calls
- Throughput: 1000 requests/second
- Availability: 99.9% uptime

### Security Requirements
- Authentication: OAuth 2.0 / JWT
- Authorization: Role-Based Access Control (RBAC)
- Encryption: TLS 1.3 for data in transit
- Data Protection: AES-256 for data at rest

{"### Security Findings" if analysis_dict.get('security_findings') else ""}
{chr(10).join([f"- {finding}" for finding in analysis_dict.get('security_findings', [])[:5]])}

### Scalability
- Horizontal scaling capability
- Load balancing
- Caching strategy

## Compliance & Standards
- GDPR compliance
- SOC 2 Type II
- ISO 27001

## Architecture Overview

### Technology Stack
{"Python: " + str(len([f for f in analysis_dict.get('files', []) if f.endswith('.py')])) + " files" if analysis_dict.get('files') else "Define your tech stack"}

### Deployment Architecture
- Cloud Platform: Azure
- Container Orchestration: Kubernetes
- CI/CD: GitHub Actions

---
Generated by Azure AI Foundry Documentation Agent
Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        results["documentation"] = documentation
        print(f"   ✅ Generated {len(documentation)} characters")
        
        # Step 3: Render documents
        print("\n🎨 Step 3: Rendering documents...")
        output_dir = "./outputs"
        rendered_files = render_documents_advanced(
            markdown_content=documentation,
            output_dir=output_dir
        )
        results["rendered_files"] = rendered_files
        print(f"   ✅ Rendered {len(rendered_files)} file(s)")
        
        print("\n" + "=" * 70)
        print("✅ Fallback Workflow Complete!")
        print("=" * 70)
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error in fallback workflow: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}


def main():
    """Main entry point for the documentation agent"""
    print("""
    ╔════════════════════════════════════════════════════════════════════╗
    ║        Azure AI Foundry - Documentation Agent System              ║
    ║                    Multi-Agent Orchestration                       ║
    ╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Example usage scenarios
    print("\n📚 Example Usage Scenarios:\n")
    
    # Scenario 1: Generate docs for a specific codebase
    print("1️⃣  Scenario: Generate comprehensive docs for authentication API")
    codebase_path = "./textdocagent"  # Example codebase
    
    if os.path.exists(codebase_path):
        prompt = "Generate comprehensive FRD, BRD, NFRD, and Security documentation for this authentication API codebase"
        result = run_docagent_workflow(prompt, codebase_path)
        
        if result.get("status") in ["success", "success_fallback"]:
            print(f"\n✅ Success! Generated documentation:")
            print(f"   Preview: {result.get('preview', 'N/A')[:200]}...")
            
            if result.get("rendered_files"):
                print(f"\n📁 Output files:")
                for file in result["rendered_files"]:
                    print(f"   - {file}")
        else:
            print(f"\n⚠️  Status: {result.get('status')}")
            print(f"   Error: {result.get('error', 'Unknown')}")
    else:
        print(f"   ⚠️  Codebase path not found: {codebase_path}")
        print("   Generating template documentation instead...")
        prompt = "Generate template documentation structure for a REST API project"
        result = run_docagent_workflow(prompt, None)
    
    print("\n" + "=" * 70)
    print("🎉 Documentation Agent - Execution Complete!")
    print("=" * 70)
    print("\n💡 Tips:")
    print("   - Check ./outputs/ directory for generated files")
    print("   - View agents in Azure Portal: https://ai.azure.com")
    print("   - Customize prompts for specific documentation needs")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
