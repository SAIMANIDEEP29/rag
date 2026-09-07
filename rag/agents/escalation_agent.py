import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def _heuristic_escalation_risk(customer_message: str, sentiment_data: dict, turn_count: int) -> dict:
    """Deterministic calculation of escalation risk score."""
    msg_lower = customer_message.lower()
    frustration = sentiment_data.get("frustration_level", 5)
    sentiment_score = sentiment_data.get("sentiment_score", 0.0)

    base_risk = (frustration * 8) + (int((1.0 - sentiment_score) * 10))
    triggers = []

    # Check specific red flags
    if any(w in msg_lower for w in ["chargeback", "dispute with bank", "lawyer", "legal", "sue", "attorney", "consumer protection"]):
        base_risk += 30
        triggers.append("Threat of dispute, chargeback, or legal action")

    if any(w in msg_lower for w in ["manager", "supervisor", "escalate", "higher up", "someone in charge"]):
        base_risk += 20
        triggers.append("Direct request for manager / supervisor escalation")

    if any(w in msg_lower for w in ["unacceptable", "scam", "fraud", "stealing", "ridiculous", "incompetent"]):
        base_risk += 15
        triggers.append("Strong accusatory or aggressive language")

    if frustration >= 8:
        triggers.append(f"Elevated customer frustration index ({frustration}/10)")

    if turn_count >= 5 and frustration >= 6:
        base_risk += 15
        triggers.append(f"Extended conversation ({turn_count} turns) without clear resolution")

    # Clamp risk between 5% and 98%
    risk_score = min(98, max(5, base_risk))

    if risk_score >= 75:
        risk_level = "CRITICAL"
        color = "#EF4444"
        alert_required = True
        strategy = "Acknowledge frustration immediately, avoid policy defensiveness, offer priority resolution, and prepare supervisor warm transfer if needed."
    elif risk_score >= 50:
        risk_level = "MODERATE"
        color = "#F59E0B"
        alert_required = False
        strategy = "Provide clear timeline and step-by-step solution. Validate customer feelings before stating procedural constraints."
    else:
        risk_level = "LOW"
        color = "#10B981"
        alert_required = False
        strategy = "Maintain positive and concise support tone. Guide customer smoothly to standard resolution."

    if not triggers:
        triggers.append("Standard customer inquiry within normal variance")

    return {
        "escalation_risk": risk_score,
        "risk_level": risk_level,
        "color_hex": color,
        "triggers": triggers,
        "intervention_strategy": strategy,
        "alert_required": alert_required
    }


def evaluate_escalation_risk(customer_message: str, sentiment_data: dict = None, turn_count: int = 1) -> dict:
    """
    Evaluates escalation risk probability and triggers real-time alerts.
    """
    if sentiment_data is None:
        sentiment_data = {"frustration_level": 5, "sentiment_score": 0.0}

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _heuristic_escalation_risk(customer_message, sentiment_data, turn_count)

    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="openai/gpt-oss-20b", api_key=api_key, temperature=0.1)

        prompt = f"""You are an Escalation Risk Monitor Agent in a customer service coaching platform.
Assess the risk of the customer escalating the issue, requesting a supervisor, or churning.

Customer Message: "{customer_message}"
Customer Frustration Level: {sentiment_data.get('frustration_level', 5)}/10
Sentiment Score: {sentiment_data.get('sentiment_score', 0.0)}
Conversation Turns: {turn_count}

Return ONLY a JSON object with:
- "escalation_risk": integer (0 to 100)
- "risk_level": "LOW" (0-49), "MODERATE" (50-74), or "CRITICAL" (75-100)
- "triggers": array of specific risk factors identified
- "intervention_strategy": 1-2 sentence recommendation for the human agent

JSON Response:"""

        res = llm.invoke(prompt)
        text = res.content.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            risk = int(data.get("escalation_risk", 35))
            level = str(data.get("risk_level", "LOW"))
            color = "#EF4444" if level == "CRITICAL" or risk >= 75 else ("#F59E0B" if level == "MODERATE" or risk >= 50 else "#10B981")
            return {
                "escalation_risk": risk,
                "risk_level": level,
                "color_hex": color,
                "triggers": list(data.get("triggers", ["Identified risk factors"])),
                "intervention_strategy": str(data.get("intervention_strategy", "Maintain clear and empathetic communication.")),
                "alert_required": risk >= 70
            }
    except Exception:
        pass

    return _heuristic_escalation_risk(customer_message, sentiment_data, turn_count)
