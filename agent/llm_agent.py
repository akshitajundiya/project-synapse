import os
import json
import re
from typing import Any, Dict, List, Tuple
from dotenv import load_dotenv
from groq import Groq
from simulator import tools
from .prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES

load_dotenv()

class GroqLLM:
    def __init__(self, model="llama-3.1-8b-instant", temperature=0):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in .env file")
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def _extract_json(self, text: str) -> str:
        text = re.sub(r"```(?:json)?", "", text).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)
        return text

    def generate(self, prompt: str) -> str:
        for attempt in range(2):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            content = response.choices[0].message.content
            json_str = self._extract_json(content)
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                if attempt == 0:
                    prompt += "\nIMPORTANT: Respond ONLY with valid JSON per schema."
                else:
                    raise ValueError(f"Groq LLM output is not valid JSON after retries: {content}")

class SynapseAgent:
    def __init__(self, llm=None, max_iters: int = 8, repeat_limit: int = 2):
        self.llm = llm or GroqLLM()
        self.max_iters = max_iters
        self.repeat_limit = repeat_limit
        self.chain_of_thought: List[Dict[str, Any]] = []
        self.seen_actions: Dict[Tuple[str, str], int] = {}

    def build_prompt(self, scenario: Dict) -> str:
        p = SYSTEM_PROMPT + "\n\n" + "Scenario: " + scenario.get("description", "") + "\n"
        for ex in FEW_SHOT_EXAMPLES:
            p += "USER: " + ex["user"] + "\n"
            p += "ASSISTANT: " + json.dumps(ex["assistant"]) + "\n"
            p += "TOOL_OBSERVATION: " + json.dumps(ex["tool_observation"]) + "\n"
            p += "ASSISTANT_NEXT: " + json.dumps(ex["assistant_next"]) + "\n"
        return p

    def parse_response(self, llm_text: str) -> Dict:
        try:
            parsed = json.loads(llm_text)
            if not all(k in parsed for k in ("thought", "action", "action_input")):
                raise ValueError("Invalid keys in LLM response")
            return parsed
        except Exception:
            return {
                "thought": "ask_human",
                "action": "ask_human",
                "action_input": {"reason": "invalid LLM output", "raw": llm_text}
            }

    def call_tool(self, action: str, action_input: Dict) -> Dict:
        mapping = {
            "check_traffic": tools.check_traffic,
            "get_merchant_status": tools.get_merchant_status,
            "get_nearby_merchants": tools.get_nearby_merchants,
            "re_route_driver": tools.re_route_driver,
            "notify_customer": tools.notify_customer,
            "initiate_mediation_flow": tools.initiate_mediation_flow,
            "collect_evidence": tools.collect_evidence,
            "analyze_evidence": tools.analyze_evidence,
            "issue_instant_refund": tools.issue_instant_refund,
            "exonerate_driver": tools.exonerate_driver,
            "log_merchant_packaging_feedback": tools.log_merchant_packaging_feedback,
            "contact_recipient_via_chat": tools.contact_recipient_via_chat,
            "find_nearby_locker": tools.find_nearby_locker,
        }
        func = mapping.get(action)
        if not func:
            return {"error": "unknown_action"}
        try:
            if isinstance(action_input, dict):
                return func(**action_input)
            else:
                return func(action_input)
        except TypeError:
            return func(action_input)

    def run(self, scenario: Dict) -> Dict:
        prompt = self.build_prompt(scenario)
        final_plan = None
        recent_actions = []

        for i in range(self.max_iters):
            llm_text = self.llm.generate(prompt)
            parsed = self.parse_response(llm_text)

            action_name = parsed.get("action", "").strip()
            if "| finish" in action_name.lower() or "|finish" in action_name.lower():
                action_name = "finish"
            parsed["action"] = action_name

            action_key = (action_name, json.dumps(parsed.get("action_input"), sort_keys=True))
            self.seen_actions[action_key] = self.seen_actions.get(action_key, 0) + 1
            recent_actions.append(action_name)

            if self.seen_actions[action_key] > self.repeat_limit or (
                len(recent_actions) >= 3 and all(a == action_name for a in recent_actions[-3:])
            ):
                final_plan = {"status": "incomplete", "reason": "repeated_action_loop"}
                break

            cot_entry = {
                "step": i + 1,
                "thought": parsed.get("thought"),
                "action": action_name,
                "action_input": parsed.get("action_input"),
                "observation": None
            }

            if action_name == "finish":
                final_plan_text = parsed.get("action_input", {}).get("final_plan", "").strip()
                if not final_plan_text:
                    final_plan_text = "Final plan generated but was empty — please check scenario setup."
                final_plan = {"status": "complete", "final_plan": final_plan_text}
                self.chain_of_thought.append(cot_entry)
                break

            if action_name == "ask_human":
                cot_entry["observation"] = {"escalated": True, "reason": parsed.get("action_input")}
                self.chain_of_thought.append(cot_entry)
                final_plan = {"status": "escalated", "reason": parsed.get("action_input")}
                break

            obs = self.call_tool(action_name, parsed.get("action_input", {}))
            cot_entry["observation"] = obs
            self.chain_of_thought.append(cot_entry)

            prompt += "\nTOOL_RESULT: " + json.dumps({"action": action_name, "result": obs}) + "\n"

        if not final_plan:
            final_plan = {"status": "incomplete", "reason": "max_iters_reached"}

        return {"cot": self.chain_of_thought, "final_plan": final_plan}

if __name__ == "__main__":
    scenfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), "simulator", "scenarios.json")
    with open(scenfile) as f:
        scenarios = json.load(f)

    agent = SynapseAgent()
    res = agent.run(scenarios["overloaded_restaurant"])
    print(json.dumps(res, indent=2))
