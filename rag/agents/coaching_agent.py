import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def _heuristic_coaching(customer_message: str, intent_data: dict, knowledge_items: list) -> dict:
    """Deterministic fallback for coaching advice and suggested replies."""
    intent = intent_data.get("intent", "GENERAL_INQUIRY")
    frustration = intent_data.get("frustration_level", 5)

    knowledge_context = " ".join([item.get("text", "") for item in knowledge_items[:2]])

    if intent == "REFUND_REQUEST":
        tips = [
            "Validate customer frustration before explaining policy timelines.",
            "Confirm order details and assure them that eligible refunds take 3-5 business days.",
            "Never promise an instant bank transfer as processing depends on card issuers."
        ]
        suggestions = [
            {
                "label": "Empathetic & Immediate Help",
                "text": "I completely understand your frustration with this charge, and I am here to help get this resolved. Let me check your account details right now to initiate your refund."
            },
            {
                "label": "Policy-Focused & Clear Timeline",
                "text": "Under our policy, all unused subscription charges are fully refundable within 14 days. I have reviewed your account and can confirm you are eligible. Your refund will process within 3-5 business days."
            },
            {
                "label": "Verification & Next Steps",
                "text": "To ensure I process this for the exact transaction, could you please confirm the email address associated with your account? I will handle the refund request immediately upon confirmation."
            }
        ]
    elif intent in ["ACCOUNT_ACCESS_ISSUE", "TECHNICAL_TROUBLESHOOTING"]:
        tips = [
            "Reassure the customer that account security lockouts are temporary (15 minutes).",
            "Never ask for customer passwords or secret SMS verification codes in chat.",
            "Provide the direct password reset email alternative as the fastest resolution."
        ]
        suggestions = [
            {
                "label": "Reassuring & Step-by-Step",
                "text": "I know how urgent it is to access your files. For security, temporary lockouts lift automatically after 15 minutes. In the meantime, I can trigger a secure password reset link to your verified email."
            },
            {
                "label": "Technical Troubleshooting",
                "text": "If SMS codes are delayed due to carrier latency, please check your email spam folder for the backup verification code or click 'Forgot Password' to create a new secure credential."
            },
            {
                "label": "Direct Assistance",
                "text": "Let me assist you in unlocking your access. Please verify the primary email on the account, and I will dispatch a direct recovery authentication token."
            }
        ]
    else:
        # General / Out-of-Domain Inquiries
        tips = [
            "Politely clarify our customer support scope (account access, billing, refunds, and troubleshooting).",
            "Maintain a helpful, courteous tone and invite the customer to ask about their account or services.",
            "Avoid hallucinating answers to external or unrelated topics."
        ]
        suggestions = [
            {
                "label": "Polite Scope Redirection",
                "text": "Hello! I am a customer support assistant. While I cannot answer questions outside of our service, I would be happy to help with any account, billing, policy, or troubleshooting questions. How can I assist you today?"
            },
            {
                "label": "Friendly Assistance Offer",
                "text": "Thank you for reaching out! I specialize in customer support for our services. If you have an inquiry regarding your account or subscriptions, please let me know!"
            },
            {
                "label": "Service Scope Clarification",
                "text": "I specialize in supporting customer accounts, payments, and product troubleshooting. Please let me know if you need assistance with any of these areas!"
            }
        ]

    return {
        "coaching_tips": tips,
        "suggested_responses": suggestions,
        "recommended_tone": "Empathetic & Calm" if frustration >= 7 else "Helpful & Professional"
    }


def generate_coaching(
    customer_message: str,
    intent_data: dict,
    knowledge_items: list,
    conversation_history: list = None
) -> dict:
    """
    Generates real-time coaching tips and 1-click suggested responses for the support agent.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _heuristic_coaching(customer_message, intent_data, knowledge_items)

    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="openai/gpt-oss-20b", api_key=api_key, temperature=0.3)

        context_str = "\n".join([f"- {k.get('source')}: {k.get('text')}" for k in knowledge_items[:3]])

        prompt = f"""You are an expert AI Support Coaching Agent.
Your role is to guide human support representatives during live conversations to improve satisfaction, maintain policy compliance, and de-escalate tension.

Customer Message: "{customer_message}"
Customer Intent: {intent_data.get('intent')}
Frustration Level: {intent_data.get('frustration_level')}/10
Emotional State: {intent_data.get('emotional_state')}

Available Knowledge Base Context:
{context_str}

Generate:
1. 3 concise real-time coaching bullet points (tips for the agent on tone, policy, and empathy).
2. 3 diverse, high-quality suggested replies the agent can send directly:
   - Option 1: Empathetic & De-escalating
   - Option 2: Direct Policy & Resolution
   - Option 3: Actionable Next Steps / Verification
3. Recommended tone.

Return ONLY a JSON object with:
- "coaching_tips": array of 3 strings
- "suggested_responses": array of 3 objects with "label" (string) and "text" (string)
- "recommended_tone": string

JSON Response:"""

        res = llm.invoke(prompt)
        text = res.content.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return {
                "coaching_tips": list(data.get("coaching_tips", [])),
                "suggested_responses": list(data.get("suggested_responses", [])),
                "recommended_tone": str(data.get("recommended_tone", "Empathetic & Professional"))
            }
    except Exception:
        pass

    return _heuristic_coaching(customer_message, intent_data, knowledge_items)
