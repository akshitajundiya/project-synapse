
---

## Execution Flow

1. **Load Scenario**
   - CLI loads `simulator/scenarios.json` and picks the given scenario.

2. **Prompt Construction**
   - `agent/prompts.py` provides a system prompt + few-shot examples.
   - The agent adds scenario details to build the initial context.

3. **LLM Reasoning Loop**
   - Groq LLM produces JSON:
     ```json
     {
       "thought": "...",
       "action": "tool_name | finish | ask_human",
       "action_input": { ... }
     }
     ```
   - The agent executes the `action` using `tools.py`.

4. **Observation Feedback**
   - Tool results are appended to the prompt for the next LLM step.

5. **Termination**
   - The loop stops when the LLM outputs `"action": "finish"` or `"ask_human"`.

---

## Tools Available
- **check_traffic**  
- **get_merchant_status**  
- **get_nearby_merchants**  
- **re_route_driver**  
- **notify_customer**  
- **initiate_mediation_flow**  
- **collect_evidence**  
- **analyze_evidence**  
- **issue_instant_refund**  
- **exonerate_driver**  
- **log_merchant_packaging_feedback**  
- **contact_recipient_via_chat**  
- **find_nearby_locker**

---

## Testing
- Run all tests:
  ```bash
  pytest -q
