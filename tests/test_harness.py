import json
import os
import pytest
from agent.llm_agent import SynapseAgent

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SCENARIOS_FILE = os.path.join(BASE_DIR, "simulator", "scenarios.json")
GOLD_PLANS_FILE = os.path.join(BASE_DIR, "tests", "gold_plans.json")

# Load scenarios and gold plans
with open(SCENARIOS_FILE) as f:
    SCENARIOS = json.load(f)

with open(GOLD_PLANS_FILE) as f:
    GOLD_PLANS = json.load(f)

@pytest.mark.parametrize("scenario_key", SCENARIOS.keys())
def test_scenario_against_gold_plan(scenario_key):
    """Runs the agent and compares the final plan against gold data."""
    agent = SynapseAgent(max_iters=3)

    # Run the agent for the scenario
    result = agent.run(SCENARIOS[scenario_key])
    final_plan = result.get("final_plan")

    # Expected from gold_plans.json
    gold_entry = GOLD_PLANS[scenario_key]["final_plan"]

    # Handle both string and structured gold plan formats
    if isinstance(gold_entry, str):
        # Compare summary text
        assert isinstance(final_plan, str) or isinstance(final_plan, dict), \
            f"Unexpected final_plan type: {type(final_plan)}"
        if isinstance(final_plan, dict):
            final_plan_text = final_plan.get("summary", "")
        else:
            final_plan_text = final_plan
        assert gold_entry.lower() in final_plan_text.lower(), \
            f"Mismatch for {scenario_key}:\nExpected: {gold_entry}\nGot: {final_plan_text}"

    elif isinstance(gold_entry, dict):
        # Compare structured plan
        if "summary" in gold_entry:
            assert gold_entry["summary"].lower() in str(final_plan).lower(), \
                f"Summary mismatch for {scenario_key}"
        if "actions" in gold_entry:
            assert isinstance(final_plan, dict), \
                f"Expected structured dict final_plan for {scenario_key}, got {type(final_plan)}"
            agent_actions = final_plan.get("actions", [])
            for action in gold_entry["actions"]:
                assert action in agent_actions, \
                    f"Action '{action}' missing in {scenario_key} final_plan"

    else:
        raise ValueError(f"Unsupported gold_plans format for {scenario_key}")
