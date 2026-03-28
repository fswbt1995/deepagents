# ✈️ Airline Name Change Agent

## 🚀 Quickstart

**Prerequisites**: Install [uv](https://docs.astral.sh/uv/) package manager:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ensure you are in the `name_change` directory:

```bash
cd examples/name_change
```

Install packages:

```bash
uv sync
```

Set your API keys in your environment:

```bash
export ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Required for Claude model
export OPENAI_API_KEY=your_openai_api_key_here        # Optional, for additional features
export LANGSMITH_API_KEY=your_langsmith_api_key_here  # [LangSmith API key](https://smith.langchain.com/settings) (free to sign up)
```

## Usage Options

You can run this example in two ways:

### Option 1: Jupyter Notebook

Run the interactive notebook to step through the name change agent:

```bash
uv run jupyter notebook name_change_agent.ipynb
```

### Option 2: LangGraph Server

Run a local [LangGraph server](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/) with a web interface:

```bash
langgraph dev
```

LangGraph server will open a new browser window with the Studio interface, which you can submit your name change request to:

<img width="2869" height="1512" alt="Screenshot 2025-11-17 at 11 42 59 AM" src="https://github.com/user-attachments/assets/03090057-c199-42fe-a0f7-769704c2124b" />

You can also connect the LangGraph server to a [UI specifically designed for deepagents](https://github.com/langchain-ai/deep-agents-ui):

```bash
git clone https://github.com/langchain-ai/deep-agents-ui.git
cd deep-agents-ui
yarn install
yarn dev
```

Then follow the instructions in the [deep-agents-ui README](https://github.com/langchain-ai/deep-agents-ui?tab=readme-ov-file#connecting-to-a-langgraph-server) to connect the UI to the running LangGraph server.

This provides a user-friendly chat interface and visualization of files in state.

<img width="2039" height="1495" alt="Screenshot 2025-11-17 at 1 11 27 PM" src="https://github.com/user-attachments/assets/d559876b-4c90-46fb-8e70-c16c93793fa8" />

## 📚 Resources

- **[Deep Agents Course](https://academy.langchain.com/courses/deep-research-with-langgraph)** - Full course on deep agents with LangGraph

### Custom Model

By default, `deepagents` uses `"claude-sonnet-4-5-20250929"`. You can customize this by passing any [LangChain model object](https://python.langchain.com/docs/integrations/chat/). See the Deep Agents package [README](https://github.com/langchain-ai/deepagents?tab=readme-ov-file#model) for more details.

```python
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

# Using Claude
model = init_chat_model(model="anthropic:claude-sonnet-4-5-20250929", temperature=0.0)

agent = create_deep_agent(
    model=model,
)
```

### Custom Instructions

The name change agent uses custom instructions defined in `name_change_agent/prompts.py` that complement (rather than duplicate) the default middleware instructions. You can modify these in any way you want.

| Instruction Set | Purpose |
|----------------|---------|
| `NAME_CHANGE_WORKFLOW_INSTRUCTIONS` | Defines the 5-step name change workflow: save request → plan with TODOs → delegate to sub-agents → synthesize → respond. Includes name change-specific planning guidelines like batching similar verification tasks and scaling rules for different request types. |
| `SUBAGENT_DELEGATION_INSTRUCTIONS` | Provides concrete delegation strategies with examples: simple requests use 1 sub-agent, multi-passenger requests use 1 per passenger, complex cases use 1 per aspect. Sets limits on parallel execution (max 3 concurrent) and iteration rounds (max 3). |
| `NAME_CHANGE_AGENT_INSTRUCTIONS` | Guides individual verification sub-agents to conduct focused checks. Includes hard limits (2-3 checks for simple requests, max 5 for complex), emphasizes using `think_tool` after each verification for strategic reflection, and defines stopping criteria. |

### Custom Tools

The name change agent adds the following custom tools beyond the built-in deepagent tools. You can also use your own tools, including via MCP servers. See the Deep Agents package [README](https://github.com/langchain-ai/deepagents?tab=readme-ov-file#mcp) for more details.

| Tool Name | Description |
|-----------|-------------|
| `passenger_lookup` | Mock passenger verification tool that checks booking references and passenger details against a simulated database. |
| `flight_lookup` | Mock flight information tool that retrieves flight schedules, status, and change eligibility windows. |
| `policy_check` | Airline policy reference tool that provides name change fees, deadlines, and processing requirements. |
| `think_tool` | Strategic reflection mechanism that helps the agent pause and assess progress between verifications, analyze findings, identify gaps, and plan next steps. |

### Demo Data

This agent uses mock data for demonstration purposes:

- **Passengers**: ABC123 (John Smith), XYZ789 (Jane Doe), DEF456 (Bob Johnson)
- **Flights**: AA101 (JFK-LAX), UA202 (ORD-SFO), DL303 (ATL-MIA)
- **Policies**: $75 fee for name changes, 24-hour deadline before departure

Try requests like:
- "Change the name on booking ABC123 from John Smith to John Doe"
- "I need to correct the spelling on my ticket XYZ789"
- "Update passenger name for flight DL303"</content>
<parameter name="filePath">/Users/bruce_work/Documents/GitHub/deepagent/deepagents/examples/name_change/README.md