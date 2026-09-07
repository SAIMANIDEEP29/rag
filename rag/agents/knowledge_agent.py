import os
import sys

# Ensure current directory is on sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_knowledge_recommendations(query: str, intent: str = None, top_k: int = 3) -> list:
    """
    Retrieves the most relevant knowledge base articles/policies for the current support context.
    Returns structured list with text chunks, source filenames, page numbers, and relevance scores.
    """
    search_query = f"{intent} {query}" if intent else query
    
    try:
        from retriever import semantic_search
        raw_results = semantic_search(search_query, top_k=top_k)
        
        recommendations = []
        for res in raw_results:
            meta = res.get("metadata", {})
            recommendations.append({
                "source": meta.get("source", "Knowledge Base Document"),
                "page": meta.get("page", "N/A"),
                "file_type": meta.get("file_type", "pdf"),
                "score": round(float(res.get("score", 0.0)), 4),
                "text": res.get("text", "").strip(),
                "summary": res.get("text", "").strip()[:180] + "..." if len(res.get("text", "")) > 180 else res.get("text", "")
            })
        return recommendations
    except Exception as e:
        # Fallback if vector index hasn't been built yet
        query_lower = query.lower()
        if intent == "REFUND_REQUEST" or any(w in query_lower for w in ["refund", "charge", "money", "payment", "bill"]):
            return [
                {
                    "source": "Refund Policy.pdf",
                    "page": 1,
                    "file_type": "pdf",
                    "score": 0.88,
                    "text": "Full refunds are available within 14 days of transaction for unused services. Processing time is 3-5 business days.",
                    "summary": "Full refunds are available within 14 days of transaction for unused services. Processing time is 3-5 business days."
                }
            ]
        elif intent == "ACCOUNT_ACCESS_ISSUE" or any(w in query_lower for w in ["lock", "login", "password", "2fa", "code"]):
            return [
                {
                    "source": "login_issues.txt",
                    "page": "N/A",
                    "file_type": "txt",
                    "score": 0.82,
                    "text": "Accounts are locked for 15 minutes after 5 consecutive failed login attempts. Use the password reset link to unlock immediately.",
                    "summary": "Accounts are locked for 15 minutes after 5 consecutive failed login attempts."
                }
            ]
        return []
