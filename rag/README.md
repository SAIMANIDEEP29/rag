# AI-Powered Customer Support Coaching Assistant

## Overview

The **AI-Powered Customer Support Coaching Assistant** is an intelligent multi-agent platform designed to coach customer service representatives in real time during live text-based interactions. The system transforms reactive agent training into proactive in-session coaching, improving first-contact resolution rates and agent performance continuously.

The platform integrates a multi-agent pipeline that analyzes customer intent, tracks emotional trajectories, assesses escalation risks, retrieves verified policies via Retrieval-Augmented Generation (RAG), and generates 1-click response suggestions within a unified **Three-Panel Coaching Console**.

---

## 🏛️ System Architecture

```text
                               Session Configuration
                        (Simulator, Manual, Replay Modes)
                                       │
                                       ▼
                       Multi-Agent Orchestration Layer
                                       │
      ┌─────────────────┬──────────────┼──────────────┬─────────────────┐
      ▼                 ▼              ▼              ▼                 ▼
Customer Simulator   Intent &      Knowledge     Coaching &        Escalation
     Agent          Sentiment     Recommender     Response        Risk Monitor
  (Persona &        Analysis         (RAG)       Suggestion           Agent
   Emotions)          Agent                         Agent
      │                 │              │              │                 │
      └─────────────────┴──────────────┼──────────────┴─────────────────┘
                                       │
                                       ▼
                         Three-Panel Coaching Console
                      (Streamlit Live Support Interface)
```

---

## 🤖 Multi-Agent Architecture & Agents Implemented

| Agent Name | Role & Core Responsibilities |
|---|---|
| **Customer Simulator Agent** | Generates realistic customer replies turn by turn based on scenario context, persona traits, and dynamic emotional progression (calms down if agent is empathetic; escalates if agent is dismissive). |
| **Intent & Sentiment Analysis Agent** | Identifies customer intent (`REFUND_REQUEST`, `ACCOUNT_ACCESS_ISSUE`, `CANCELLATION_REQUEST`, etc.), emotional state, sentiment polarity ($-1.0$ to $+1.0$), and frustration level ($1-10$). |
| **Knowledge Recommendation Agent** | Connects to the local FAISS vector store to retrieve relevant policy clauses, FAQs, and troubleshooting steps with source filenames and page numbers. |
| **Coaching & Response Suggestion Agent** | Delivers real-time communication tips, tone guidance, and generates 3 customized 1-click suggested responses (*Empathetic*, *Policy-Focused*, *Actionable*). |
| **Escalation Risk Monitor Agent** | Continuously scores escalation likelihood ($0\% - 100\%$), identifies risk triggers (e.g. chargeback/legal threats), and fires critical alert overlays ($>70\%$). |

---

## 🎮 Three Interaction Modes

* 🤖 **Simulator Mode**: AI generates realistic customer messages turn by turn across pre-configured training scenarios (Refund Disputes, Locked Accounts, Payment Inquiries). The trainee practices replying and watches customer mood and risk adapt in real time.
* ✍️ **Manual Mode**: Live human representatives paste incoming customer messages to instantly receive RAG policy citations, escalation risk assessments, and 1-click recommended replies.
* 📼 **Replay Mode**: Pre-loaded support transcripts are replayed message-by-message for practice, quality assurance audits, and coaching reviews.

---

## 🖥️ Live Support Console (Three-Panel UI)

* **Left Panel (Sidebar)**: Mode Switcher (*Simulator*, *Manual*, *Replay*), scenario selector with customer persona profile & goal, and session reset controls.
* **Center Panel (Conversation Workspace)**: Live chat dialogue with distinct customer and representative avatars, real-time customer mood badge, and draft reply box with 1-click suggestion prefill.
* **Right Panel (Live Coaching & Intelligence)**:
  * 🚨 **Escalation Risk Gauge & Alert Banner**: Real-time risk percentage with emergency intervention strategies.
  * 🎭 **Intent & Sentiment Gauge**: Frustration bar ($1-10$), customer emotion, and intent chip.
  * 💡 **Real-Time Coaching Guidance**: Actionable dos and don'ts for the current turn.
  * ⚡ **1-Click Response Suggestions**: Ready-to-send responses that can be inserted into the chat with a single click.
  * 📚 **RAG Knowledge Recommendations**: Collapsible policy and troubleshooting cards with page citations and similarity match scores.

---

## 🛠️ Technologies Used

| Technology / Library | Version / Specification | Purpose in Project |
|---|---|---|
| **Python** | `3.10+` | Core programming language & multi-agent orchestration |
| **Streamlit** | `1.30.0+` | Interactive Three-Panel Live Support Console UI |
| **FAISS (CPU)** | `faiss-cpu` | High-performance vector database for dense retrieval & cosine similarity |
| **Sentence Transformers** | `all-MiniLM-L6-v2` | Embedding model generating 384-dimensional dense text vectors |
| **LangChain & Groq** | `langchain-groq` | Fast LLM inference (`openai/gpt-oss-20b` / `llama-3.3-70b-versatile`) |
| **PyPDF** | `pypdf` | Parsing policy PDFs with page-level metadata preservation |
| **NumPy** | `numpy` | Vector transformations and matrix normalization |
| **Python-Dotenv** | `python-dotenv` | Secure API key and environment variable management |

---

## 📂 Project Structure

```
gencoders/
├── README.md                           # Master project documentation
└── rag/
    ├── app.py                          # Streamlit Three-Panel Live Coaching Console
    ├── orchestrator.py                 # Multi-Agent Orchestration Layer
    ├── build_index.py                  # Script to build the FAISS vector database
    ├── chunker.py                      # Text chunking logic
    ├── document_loader.py              # PDF and text document loader
    ├── embeddings.py                   # Embedding model configuration
    ├── retriever.py                    # Vector retrieval logic
    ├── text_cleaner.py                 # Text preprocessing & normalization
    ├── vector_store.py                 # FAISS vector store manager
    ├── requirements.txt                # Python dependencies
    ├── README.md                       # Submodule documentation
    ├── agents/
    │   ├── __init__.py
    │   ├── simulator_agent.py          # Customer Simulator Agent
    │   ├── sentiment_agent.py          # Intent & Sentiment Analysis Agent
    │   ├── knowledge_agent.py          # Knowledge Recommendation Agent (RAG)
    │   ├── coaching_agent.py           # Coaching & Response Suggestion Agent
    │   └── escalation_agent.py         # Escalation Risk Monitor Agent
    └── data/
        ├── knowledge_base/
        │   ├── policies/               # Cancellation, Privacy, & Refund PDFs
        │   └── troubleshooting/        # App, Login, & Payment issue guides
        └── scenarios/
            ├── scenarios.json          # Pre-built customer training scenarios
            └── replay_transcripts.json # Recorded support transcripts
```

---

## 📥 Prerequisites & System Requirements

* **Operating System**: Windows 10/11, macOS, or Linux
* **Python**: Python `3.10` or higher ([Download Python](https://www.python.org/downloads/))
* **Git**: Installed and accessible from your terminal ([Download Git](https://git-scm.com/))
* **Groq API Key (Optional)**: Get a free API key from [Groq Console](https://console.groq.com/). *(The system also includes a built-in offline heuristic simulation engine if no API key is provided).*

---

## ⚡ Installation & Execution Commands

### Step 1: Clone the Repository
```bash
git clone https://github.com/Gencoders2026/gencoders.git
cd gencoders/rag
```

---

### Step 2: Create and Activate Virtual Environment

* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

* **Windows (Command Prompt / CMD):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

*(Dependencies installed: `streamlit`, `faiss-cpu`, `sentence-transformers`, `langchain-groq`, `pypdf`, `numpy`, `python-dotenv`, `requests`)*

---

### Step 4: Configure Environment Variables (Optional)
Create a `.env` file in the `rag/` folder:
```ini
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

### Step 5: Build the Knowledge Base Vector Index
Ingest and index all PDFs and troubleshooting guides into FAISS:
```bash
python build_index.py
```

Expected output:
```text
============================================================
Building Knowledge Base
============================================================
Found 6 documents.
Loaded 6 document sections.
Creating chunks...
Created 24 chunks.
Generating embeddings...
Embeddings generated successfully.
Creating FAISS vector database...
Knowledge Base Created Successfully!
```

---

### Step 6: Launch the Three-Panel Live Support Console
```bash
streamlit run app.py
```
Your default browser will automatically open:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## 🧪 Testing & Verification Commands

### 1. Test All Agents & Orchestrator via CLI:
```powershell
python -c "import sys; sys.path.append('.'); from orchestrator import CoachingOrchestrator; res = CoachingOrchestrator.process_customer_turn('You stole my money! I will sue your company and contact my bank to chargeback right now!'); print('Risk:', res['escalation']['escalation_risk'], '% | Alert:', res['escalation']['alert_required'], '| Intent:', res['sentiment']['intent'])"
```

Expected Output:
```text
Risk: 98 % | Alert: True | Intent: REFUND_REQUEST
```

### 2. Verify Positive Resolution Query:
```powershell
python -c "import sys; sys.path.append('.'); from orchestrator import CoachingOrchestrator; res = CoachingOrchestrator.process_customer_turn('Thank you for clarifying. Does this mean the issue is being handled now?'); print('Risk:', res['escalation']['escalation_risk'], '% | Mood:', res['sentiment']['emotional_state'])"
```

Expected Output:
```text
Risk: 50 % | Mood: Calm
```
