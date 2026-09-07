import os
import json
from agents.sentiment_agent import analyze_sentiment
from agents.knowledge_agent import get_knowledge_recommendations
from agents.escalation_agent import evaluate_escalation_risk
from agents.coaching_agent import generate_coaching
from agents.simulator_agent import generate_simulated_customer_message

class CoachingOrchestrator:
    """
    Coordinates the multi-agent coaching workflow for each conversational turn.
    """

    @staticmethod
    def load_scenarios() -> list:
        path = os.path.join(os.path.dirname(__file__), "data", "scenarios", "scenarios.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    @staticmethod
    def load_replay_transcripts() -> list:
        path = os.path.join(os.path.dirname(__file__), "data", "scenarios", "replay_transcripts.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    @staticmethod
    def process_customer_turn(
        customer_message: str,
        conversation_history: list = None,
        top_k: int = 3
    ) -> dict:
        """
        Executes the full real-time coaching pipeline for an incoming customer message:
        1. Intent & Sentiment Analysis
        2. Escalation Risk Assessment
        3. RAG Knowledge Retrieval
        4. Coaching Tips & Response Suggestions
        """
        if conversation_history is None:
            conversation_history = []

        turn_count = len([m for m in conversation_history if m.get("role") == "customer"]) + 1

        # 1. Intent & Sentiment
        sentiment_data = analyze_sentiment(customer_message, conversation_history)

        # 2. Escalation Risk
        escalation_data = evaluate_escalation_risk(customer_message, sentiment_data, turn_count)

        # 3. RAG Knowledge Recommendations
        knowledge_items = get_knowledge_recommendations(
            query=customer_message,
            intent=sentiment_data.get("intent"),
            top_k=top_k
        )

        # 4. Coaching & Suggestions
        coaching_data = generate_coaching(
            customer_message=customer_message,
            intent_data=sentiment_data,
            knowledge_items=knowledge_items,
            conversation_history=conversation_history
        )

        return {
            "sentiment": sentiment_data,
            "escalation": escalation_data,
            "knowledge": knowledge_items,
            "coaching": coaching_data,
            "turn_count": turn_count
        }

    @staticmethod
    def simulate_next_customer_turn(
        scenario: dict,
        conversation_history: list,
        current_frustration: int,
        current_mood: str
    ) -> dict:
        """
        Invokes the Customer Simulator Agent to produce the next customer turn.
        """
        return generate_simulated_customer_message(
            scenario=scenario,
            conversation_history=conversation_history,
            current_frustration=current_frustration,
            current_mood=current_mood
        )
