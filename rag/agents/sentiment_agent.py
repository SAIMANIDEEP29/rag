import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def _heuristic_sentiment_analysis(message: str) -> dict:
    """Fallback rule-based sentiment and intent classifier."""
    msg_lower = message.lower()
    
    # Intent detection
    if any(w in msg_lower for w in ["thank", "thanks", "great", "resolved", "appreciate", "clarifying", "fixed"]):
        intent = "RESOLUTION_CONFIRMATION"
        entities = ["satisfaction", "resolution"]
    elif any(w in msg_lower for w in ["refund", "money back", "charged twice", "reimburse", "overcharged", "chargeback"]):
        intent = "REFUND_REQUEST"
        entities = ["refund", "payment", "billing"]
    elif any(w in msg_lower for w in ["cancel", "cancellation", "delete data", "close account", "terminate"]):
        intent = "CANCELLATION_REQUEST"
        entities = ["subscription", "cancellation", "account closure"]
    elif any(w in msg_lower for w in ["locked", "login", "password", "2fa", "otp", "access", "sms code", "reset"]):
        intent = "ACCOUNT_ACCESS_ISSUE"
        entities = ["credentials", "login", "security"]
    elif any(w in msg_lower for w in ["double charge", "charged", "invoice", "credit card", "bank statement"]):
        intent = "PAYMENT_ISSUE"
        entities = ["billing", "invoice", "card"]
    elif any(w in msg_lower for w in ["error", "crash", "not working", "bug", "broken", "failed"]):
        intent = "TECHNICAL_TROUBLESHOOTING"
        entities = ["technical issue", "system error"]
    else:
        intent = "GENERAL_INQUIRY"
        entities = ["general support"]

    # Frustration & Sentiment scoring
    frustration = 5
    sentiment_score = 0.0
    emotional_state = "Neutral"
    
    anger_words = [r"\bdemand\b", r"\bunacceptable\b", r"\bchargeback\b", r"\blawyer\b", r"\bsue\b", r"\bworst\b", r"\bhorrible\b", r"\bcheat\b", r"\bscam\b", r"\bridiculous\b", r"\bfurious\b", r"\bstole\b"]
    distress_words = [r"\burgent\b", r"\bemergency\b", r"\blocked out\b", r"\bcannot access\b", r"\bdesperate\b"]
    positive_words = [r"\bthank you\b", r"\bthanks\b", r"\bhelpful\b", r"\bsolved\b", r"\bappreciate\b", r"\bgreat\b", r"\bawesome\b", r"\bkindly\b", r"\bplease\b"]

    anger_count = sum(1 for p in anger_words if re.search(p, msg_lower))
    distress_count = sum(1 for p in distress_words if re.search(p, msg_lower))
    pos_count = sum(1 for p in positive_words if re.search(p, msg_lower))

    if pos_count > 0 and anger_count == 0:
        frustration = max(1, 3 - pos_count)
        sentiment_score = min(1.0, 0.4 + (pos_count * 0.2))
        emotional_state = "Satisfied" if pos_count >= 2 else "Calm"
    elif anger_count > 0 or distress_count > 0:
        frustration = min(10, 5 + (anger_count * 2) + distress_count)
        sentiment_score = max(-1.0, -0.2 - (anger_count * 0.25) - (distress_count * 0.15))
        emotional_state = "Angry" if anger_count >= 2 else ("Anxious" if distress_count > 0 else "Frustrated")
    
    urgency = "High" if frustration >= 7 else ("Medium" if frustration >= 4 else "Low")

    return {
        "intent": intent,
        "sentiment_score": round(sentiment_score, 2),
        "frustration_level": frustration,
        "emotional_state": emotional_state,
        "key_entities": entities,
        "urgency": urgency
    }


def analyze_sentiment(customer_message: str, conversation_history: list = None) -> dict:
    """
    Analyzes customer intent, sentiment polarity, frustration level, and emotional state.
    Uses Groq LLM if configured, otherwise falls back to deterministic heuristic parsing.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _heuristic_sentiment_analysis(customer_message)

    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="openai/gpt-oss-20b", api_key=api_key, temperature=0.0)
        
        prompt = f"""You are an expert customer support Intent & Sentiment Analysis Agent.
Analyze the following customer message and return ONLY a valid JSON object with these exact keys:
- "intent": string (e.g. "REFUND_REQUEST", "ACCOUNT_ACCESS_ISSUE", "CANCELLATION_REQUEST", "PAYMENT_ISSUE", "TECHNICAL_TROUBLESHOOTING", "GENERAL_INQUIRY", "RESOLUTION_CONFIRMATION")
- "sentiment_score": float between -1.0 (very negative) and 1.0 (very positive)
- "frustration_level": integer between 1 (completely calm) and 10 (extremely furious)
- "emotional_state": string ("Angry", "Frustrated", "Anxious", "Skeptical", "Neutral", "Satisfied", "Relieved")
- "key_entities": array of extracted strings
- "urgency": "High", "Medium", or "Low"

Customer Message: "{customer_message}"

Respond ONLY with valid JSON:"""
        
        res = llm.invoke(prompt)
        text = res.content.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return {
                "intent": str(data.get("intent", "GENERAL_INQUIRY")),
                "sentiment_score": float(data.get("sentiment_score", -0.5)),
                "frustration_level": int(data.get("frustration_level", 6)),
                "emotional_state": str(data.get("emotional_state", "Frustrated")),
                "key_entities": list(data.get("key_entities", [])),
                "urgency": str(data.get("urgency", "Medium"))
            }
    except Exception:
        pass

    return _heuristic_sentiment_analysis(customer_message)
