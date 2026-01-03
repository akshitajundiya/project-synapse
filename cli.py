# cli.py 
import argparse
import json
import os
from agent.llm_agent import SynapseAgent
from dotenv import load_dotenv

# Load .env early so GROQ_API_KEY is available
load_dotenv()

# Optional: color output for better readability
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, name): return ""
    Fore = Style = Dummy()


def load_scenarios(path: str):
    with open(path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Run Project Synapse Agent (Groq + LangChain)")
    parser.add_argument("--scenario", required=True, help="Scenario key from simulator/scenarios.json")
    parser.add_argument("--scenarios-file", default="simulator/scenarios.json")
    args = parser.parse_args()

    scen_file = args.scenarios_file
    if not os.path.exists(scen_file):
        print(f"{Fore.RED}Scenarios file not found: {scen_file}")
        return

    scens = load_scenarios(scen_file)

    if args.scenario not in scens:
        print(f"{Fore.RED}Scenario '{args.scenario}' not found in {scen_file}")
        return

    # Ensure GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print(f"{Fore.RED}Error: GROQ_API_KEY is not set in environment or .env file.")
        return

    # Create agent with Groq LLM through LangChain
    agent = SynapseAgent()
    print(f"{Fore.CYAN}Running scenario: {args.scenario}{Style.RESET_ALL}\n")

    result = agent.run(scens[args.scenario])

    print(f"{Fore.YELLOW}===== CHAIN OF THOUGHT ====={Style.RESET_ALL}")
    for step in result['cot']:
        print(f"{Fore.GREEN}Step {step['step']}{Style.RESET_ALL}: {step['thought']}")
        print(f"  {Fore.CYAN}Action:{Style.RESET_ALL} {step['action']}")
        print(f"  {Fore.CYAN}Input:{Style.RESET_ALL} {json.dumps(step['action_input'], indent=2)}")
        print(f"  {Fore.MAGENTA}Observation:{Style.RESET_ALL} {json.dumps(step['observation'], indent=2)}\n")

    print(f"{Fore.YELLOW}===== FINAL PLAN ====={Style.RESET_ALL}")
    print(json.dumps(result['final_plan'], indent=2))


if __name__ == "__main__":
    main()
