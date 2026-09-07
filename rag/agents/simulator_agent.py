import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def generate_simulated_customer_message(
    scenario: dict,
    conversation_history: list,
    current_frustration: int = 7,
    current_mood: str = "Angry"
) -> dict:
    """
    Simulates the customer's response based on the scenario context,
    persona, current emotional state, and support agent's last message.
    """
    api_key = os.getenv("GROQ_API_KEY")
    agent_last_reply = ""
    for msg in reversed(conversation_history):
        if msg.get("role") == "agent":
            agent_last_reply = msg.get("content", "")
            break

    # Default heuristic progression if LLM is unavailable
    if not api_key:
        turn_count = len([m for m in conversation_history if m.get("role") == "customer"])
        if turn_count == 0:
            return {
                "message": scenario.get("initial_message", "Hello, I need help with an urgent issue."),
                "new_frustration": scenario.get("initial_frustration", 7),
                "new_mood": scenario.get("initial_mood", "Angry"),
                "reasoning": "Starting conversation with scenario baseline emotions."
            }
        
        # Check if agent reply was empathetic/helpful
        agent_lower = agent_last_reply.lower()
        if any(w in agent_lower for w in ["understand", "apologize", "sorry", "refund", "glad", "help", "resolved"]):
            new_frust = max(1, current_frustration - 2)
            new_mood = "Calming Down" if new_frust > 3 else "Satisfied"
            msg = f"Thank you for clarifying. Does this mean the issue is being handled now?"
        elif any(w in agent_lower for w in ["cannot", "not possible", "policy does not allow", "your fault"]):
            new_frust = min(10, current_frustration + 2)
            new_mood = "Furious"
            msg = f"This is ridiculous! I want to speak with your manager immediately. That is unacceptable!"
        else:
            new_frust = max(1, current_frustration - 1)
            new_mood = "Skeptical"
            msg = f"Alright, but how long is this going to take? I need a clear answer."
            
        return {
            "message": msg,
            "new_frustration": new_frust,
            "new_mood": new_mood,
            "reasoning": "Progressed mood based on support agent tone and clarity."
        }

    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="openai/gpt-oss-20b", api_key=api_key, temperature=0.7)

        history_summary = "\n".join([
            f"{m.get('role').upper()}: {m.get('content')}"
            for m in conversation_history[-6:]
        ])

        prompt = f"""You are a Customer Simulator Agent for support training.
You play the role of a realistic customer contacting customer support.

Scenario Details:
- Title: {scenario.get('title')}
- Customer Persona: {scenario.get('persona')}
- Customer Name: {scenario.get('customer_name', 'Customer')}
- Background Context: {scenario.get('context')}
- Current Frustration Level (1-10): {current_frustration}
- Current Mood: {current_mood}

Recent Conversation History:
{history_summary if history_summary else "(Beginning of conversation)"}

Support Agent's Last Reply:
"{agent_last_reply}"

Instructions:
1. Stay strictly in character as the customer.
2. If the agent was empathetic, helpful, and followed correct policy, reduce frustration and soften tone.
3. If the agent was dismissive, vague, or argumentative, increase frustration and escalate.
4. Keep the response natural, concise (1-3 sentences), and conversational.

Return ONLY a valid JSON object with:
- "message": the customer's next spoken message
- "new_frustration": integer (1 to 10)
- "new_mood": string (e.g. "Angry", "Frustrated", "Skeptical", "Calming Down", "Satisfied")
- "reasoning": brief explanation of emotional shift

JSON Response:"""

        res = llm.invoke(prompt)
        text = res.content.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return {
                "message": str(data.get("message", "Could you provide an update on this?")),
                "new_frustration": int(data.get("new_frustration", current_frustration)),
                "new_mood": str(data.get("new_mood", current_mood)),
                "reasoning": str(data.get("reasoning", "Emotional progression updated."))
            }
    except Exception:
        pass

    return {
        "message": "I need this resolved as soon as possible. What are the next steps?",
        "new_frustration": max(1, current_frustration - 1),
        "new_mood": current_mood,
        "reasoning": "Fallback response generated."
    }
