"""Name Change Agent - Standalone script for LangGraph deployment.

This module creates a name change agent with custom tools and prompts
for processing airline passenger name change requests.
"""

from datetime import datetime

from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

from name_change_agent.prompts import (
    NAME_CHANGE_AGENT_INSTRUCTIONS,
    NAME_CHANGE_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
)
from name_change_agent.tools import passenger_lookup, flight_lookup, policy_check, think_tool

# Limits
max_concurrent_verification_units = 3
max_verification_iterations = 3

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Combine orchestrator instructions (NAME_CHANGE_AGENT_INSTRUCTIONS only for sub-agents)
INSTRUCTIONS = (
    NAME_CHANGE_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_verification_units=max_concurrent_verification_units,
        max_verification_iterations=max_verification_iterations,
    )
)

# Create name change sub-agent
name_change_sub_agent = {
    "name": "name-change-agent",
    "description": "Delegate name change verification to the sub-agent. Only give this agent one verification task at a time.",
    "system_prompt": NAME_CHANGE_AGENT_INSTRUCTIONS.format(date=current_date),
    "tools": [passenger_lookup, flight_lookup, policy_check, think_tool],
}

# Model - using Claude for consistency
model = init_chat_model(model="anthropic:qwen3-max-2025-09-23", temperature=0.0, base_url="https://dashscope.aliyuncs.com/apps/anthropic")

# Create the agent
agent = create_deep_agent(
    model=model,
    tools=[passenger_lookup, flight_lookup, policy_check, think_tool],
    system_prompt=INSTRUCTIONS,
    subagents=[name_change_sub_agent],
)
