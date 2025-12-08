# Azure AI Foundry Agent Setup Guide

DocOrchestrator: asst_JPMbcPm1IMOiehO2txHnNjPE
CodeAnalyzerAgent: asst_TbPrjKrrAMVRlgngPosDyMYV
DocGeneratorAgent: asst_RJOsYKev7WWwqqGQNLXE9m6P
FormatterAgent: asst_oSAQruvGl650eWyolc1O3M33

## Overview

The `agents.py` file implements **4 specialized agents** for automated documentation generation using Azure AI Foundry's multi-agent orchestration capabilities.

---

## The 4 Agents

### 1. **DocOrchestrator** (Orchestrator)

**Role**: Master coordinator that decomposes tasks and delegates to specialized agents.

**Responsibilities**:

- Analyze user requests and codebase requirements
- Decompose tasks into: Analyze → Generate → Format
- Delegate to specialized agents
- Coordinate workflow and ensure quality
- Return final documentation package

**Connected Agents**: CodeAnalyzer, DocGenerator, Formatter

---

### 2. **CodeAnalyzerAgent** (Code Analysis)

**Role**: Senior Code & System Intelligence Engineer

**Capabilities**:

- Multi-language analysis (Python, JS/TS, Java, Go, C#)
- Architecture extraction
- Endpoint detection (REST APIs, GraphQL)
- Security vulnerability scanning
- Authentication method detection
- Output structured JSON

**Tools**: `analyze_codebase`, `analyze_codebase_advanced`

---

### 3. **DocGeneratorAgent** (Documentation Writing)

**Role**: Enterprise Documentation Architect

**Generates**:

- BRD (Business Requirements Document)
- FRD (Functional Requirements Document)
- NFRD (Non-Functional Requirements Document)
- Security & Compliance Documentation
- Architecture Overview

**Format**: Professional Markdown with tables, code examples, traceability

---

### 4. **FormatterAgent** (Document Rendering)

**Role**: Professional Document Publisher

**Outputs**:

- PDF (professional styling)
- DOCX (enterprise format)
- HTML (web view)
- Markdown (source)

**Features**: Professional typography, consistent branding, Azure Blob upload

---

## Implementation Modes

### Mode 1: Azure AI Foundry Agent SDK (Recommended)

**Requirements**:

```bash
pip install azure-ai-projects
```

**Setup**:

```python
from agents import create_foundry_agents

# Creates 4 agents in Azure AI Foundry
agents = create_foundry_agents()

# Access agents
orchestrator = agents['orchestrator']
code_analyzer = agents['code_analyzer']
doc_generator = agents['doc_generator']
formatter = agents['formatter']
```

**Benefits**:

- ✅ Multi-agent orchestration
- ✅ Built-in delegation
- ✅ Portal visibility
- ✅ Managed by Azure
- ✅ Scalable architecture

---

### Mode 2: Fallback (ChatCompletions)

**Used When**: Agent SDK not available

**Setup**:

```python
from agents import create_doc_agents

# Creates basic agents using ChatCompletions
agents = create_doc_agents()

# Access agents
code_analyzer = agents['code_analyzer']
doc_writer = agents['doc_writer']
```

**Benefits**:

- ✅ No additional dependencies
- ✅ Works immediately
- ✅ Same interface
- ⚠️ Manual orchestration required

---

## Configuration

### Environment Variables (.env):

```env
# Azure OpenAI Configuration (Required)
AZURE_OPENAI_ENDPOINT=https://canaifoundry.cognitiveservices.azure.com/openai/deployments/gpt-4o-mini
AZURE_OPENAI_API_KEY=your-api-key-here

# Azure AI Foundry Project (Required for Agent SDK)
AZURE_AI_PROJECT_ENDPOINT=https://canaifoundry.services.ai.azure.com/api/projects/multicat
AZURE_PROJECT_NAME=multicat

# Deployment Configuration
DEPLOYMENT_NAME=gpt-4o-mini
MODEL_VERSION=2024-07-18

# Azure Subscription (Optional)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=AIExplore
```

---

## Usage

### Option 1: Create Agents via Script

```bash
# Run the agents script
python agents.py
```

**Output**:

```
🤖 Creating Azure AI Foundry Agents...
   Creating DocOrchestrator...
   Creating CodeAnalyzerAgent...
   Creating DocGeneratorAgent...
   Creating FormatterAgent...
✅ All agents created successfully!
🔗 Configuring multi-agent orchestration...
✅ Multi-agent orchestration configured!
```

---

### Option 2: Create Agents via Portal

**Steps**:

1. Navigate to Azure AI Foundry Portal
2. Go to your Project → **"Agents"** section
3. Click **"+ Create"**
4. For each agent:
   - Name: `DocOrchestrator`, `CodeAnalyzerAgent`, etc.
   - Model: `gpt-4o-mini`
   - Instructions: Copy from `agents.py` agent definitions
   - Tools: Configure as specified
5. Save and note agent IDs
6. Configure "Connected Agents" for orchestrator

---

### Option 3: Use in Your Code

```python
from agents import create_foundry_agents

# Initialize agents
agents = create_foundry_agents()

# Use orchestrator
orchestrator = agents['orchestrator']['agent']

# Run documentation generation
result = orchestrator.run(
    prompt="Generate documentation for my e-commerce API",
    codebase_path="./my-project"
)

print(result)
```

---

## Multi-Agent Orchestration

### How It Works:

```
User Request
    ↓
DocOrchestrator (Coordinates)
    ↓
    ├→ CodeAnalyzerAgent (Analyzes code)
    │       ↓
    ├→ DocGeneratorAgent (Writes docs)
    │       ↓
    └→ FormatterAgent (Renders output)
```

### Benefits:

- **Specialization**: Each agent excels at one task
- **Modularity**: Agents can be updated independently
- **Scalability**: Add more agents as needed
- **Delegation**: Orchestrator routes via natural language
- **No Custom Code**: Azure handles routing automatically

---

## Agent Functions

### Helper Functions Available:

```python
# Deploy a model (SDK alternative to portal)
from agents import deploy_model_if_needed
deploy_model_if_needed("gpt-4o-mini", "gpt-4o-mini-deploy")

# List all agents
from agents import list_agents
agents = list_agents()

# Delete an agent
from agents import delete_agent
delete_agent("agent-id-here")
```

---

## Portal Integration

### View Agents in Azure Portal:

1. Navigate to: https://ai.azure.com
2. Select your project: **multicat**
3. Go to: **"My assets" → "Agents"**
4. View all created agents
5. Test agents individually
6. Configure connections and tools

### Manage Deployments:

1. Go to: **"My assets" → "Models + endpoints"**
2. View: **"Model deployments"**
3. Current deployments:
   - `gpt-4o-mini` (Primary)
   - `o3-mini` (Available)
   - `gpt-4.1` (Available)

---

## Troubleshooting

### Issue: "Agent SDK not available"

**Solution**:

```bash
pip install azure-ai-projects
```

Or use fallback mode (works without SDK)

---

### Issue: "Could not initialize Agent client"

**Solution**: Check environment variables:

```bash
# Verify configuration
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Project Endpoint:', os.getenv('AZURE_AI_PROJECT_ENDPOINT'))"
```

---

### Issue: "Agent creation failed"

**Solution**:

1. Verify model deployment exists: `gpt-4o-mini`
2. Check Azure credentials are valid
3. Ensure project endpoint is correct
4. Create agents via Portal as backup

---

## Testing

### Test Basic Functionality:

```bash
# Test agent initialization
python -c "from agents import create_doc_agents; agents = create_doc_agents(); print('✅ Agents created:', list(agents.keys()))"
```

### Test with Azure AI Foundry SDK:

```bash
# Install SDK
pip install azure-ai-projects

# Run agents script
python agents.py
```

### Test Full Pipeline:

```bash
# Run main orchestration
python main.py
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          Azure AI Foundry Project (multicat)        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │     Model Deployment: gpt-4o-mini            │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Agent 1: DocOrchestrator                     │  │
│  │  - Coordinates workflow                       │  │
│  │  - Delegates tasks                            │  │
│  └─────┬────────────────────────────────────────┘  │
│        │ Connects to ↓                              │
│        │                                             │
│  ┌─────┴─────────┬─────────────┬─────────────┐    │
│  │               │             │             │    │
│  │  Agent 2      │  Agent 3    │  Agent 4    │    │
│  │  CodeAnalyzer │  DocGen     │  Formatter  │    │
│  │               │             │             │    │
│  └───────┬───────┴──────┬──────┴──────┬──────┘    │
│          │              │             │            │
└──────────┼──────────────┼─────────────┼────────────┘
           │              │             │
           ↓              ↓             ↓
     [Tools: Code]  [AI Generation] [Rendering]
     analyze_codebase                render_docs
```

---

## Best Practices

1. **Use Agent SDK**: Install `azure-ai-projects` for full features
2. **Start with Portal**: Create agents manually to understand workflow
3. **Test Individually**: Validate each agent before orchestration
4. **Monitor Costs**: Track token usage in Azure Portal
5. **Version Control**: Keep agent instructions in code (not just portal)
6. **Backup Strategy**: Maintain fallback implementation

---

## Next Steps

1. ✅ Agents configured
2. Install Agent SDK: `pip install azure-ai-projects`
3. Run: `python agents.py` to create agents
4. Test in Portal: View agents under "My assets"
5. Run pipeline: `python main.py`
6. Monitor: Check Azure Portal for execution logs

---

## Resources

- **Azure AI Foundry**: https://ai.azure.com
- **Your Project**: https://ai.azure.com/resource/overview?wsid=/subscriptions/.../multicat
- **Agent Documentation**: https://learn.microsoft.com/azure/ai-studio/how-to/agents
- **SDK Reference**: https://learn.microsoft.com/python/api/azure-ai-projects

---

**Status**: Agents configured with fallback support! Install Agent SDK for full multi-agent orchestration. 🚀
