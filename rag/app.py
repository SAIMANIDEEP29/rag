import streamlit as st
import json
import os
from orchestrator import CoachingOrchestrator

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------
st.set_page_config(
    page_title="AI Customer Support Coaching Console",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling the Three-Panel Console
st.markdown("""
<style>
    .reportview-container {
        background: #0F172A;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-left: 4px solid #3B82F6;
    }
    .alert-card {
        background-color: #450A0A;
        border: 1px solid #EF4444;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
        color: #FCA5A5;
    }
    .suggestion-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
    .knowledge-card {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 8px;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# INITIALIZE STATE
# --------------------------------------------------
scenarios = CoachingOrchestrator.load_scenarios()
replay_transcripts = CoachingOrchestrator.load_replay_transcripts()

if "mode" not in st.session_state:
    st.session_state.mode = "Simulator Mode"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "coaching_data" not in st.session_state:
    st.session_state.coaching_data = None

if "current_scenario" not in st.session_state and scenarios:
    st.session_state.current_scenario = scenarios[0]

if "customer_frustration" not in st.session_state:
    st.session_state.customer_frustration = 7

if "customer_mood" not in st.session_state:
    st.session_state.customer_mood = "Angry"

if "replay_index" not in st.session_state:
    st.session_state.replay_index = 0

if "selected_transcript" not in st.session_state and replay_transcripts:
    st.session_state.selected_transcript = replay_transcripts[0]

if "draft_reply" not in st.session_state:
    st.session_state.draft_reply = ""


# --------------------------------------------------
# PANEL 1: SIDEBAR (Session Config & Controls)
# --------------------------------------------------
with st.sidebar:
    st.title("🎧 Support Console")
    st.caption("AI-Powered Multi-Agent Coaching Platform")
    st.markdown("---")

    # Mode Selector
    mode = st.radio(
        "Interaction Mode",
        ["Simulator Mode", "Manual Mode", "Replay Mode"],
        index=0 if st.session_state.mode == "Simulator Mode" else (1 if st.session_state.mode == "Manual Mode" else 2)
    )

    if mode != st.session_state.mode:
        st.session_state.mode = mode
        st.session_state.messages = []
        st.session_state.coaching_data = None
        st.session_state.replay_index = 0
        st.rerun()

    st.markdown("---")

    # Mode-Specific Controls
    if st.session_state.mode == "Simulator Mode":
        st.subheader("🎯 Scenario Selection")
        scenario_titles = [s["title"] for s in scenarios]
        selected_title = st.selectbox("Choose Training Scenario", scenario_titles)
        chosen_scen = next((s for s in scenarios if s["title"] == selected_title), scenarios[0])
        
        if chosen_scen["id"] != st.session_state.current_scenario.get("id"):
            st.session_state.current_scenario = chosen_scen
            st.session_state.customer_frustration = chosen_scen["initial_frustration"]
            st.session_state.customer_mood = chosen_scen["initial_mood"]
            st.session_state.messages = [
                {"role": "customer", "content": chosen_scen["initial_message"]}
            ]
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                chosen_scen["initial_message"],
                st.session_state.messages
            )
            st.rerun()

        # Persona Details
        st.markdown(f"**Customer:** {st.session_state.current_scenario.get('customer_name')}")
        st.markdown(f"**Persona:** `{st.session_state.current_scenario.get('persona')}`")
        st.markdown(f"**Goal:** *{st.session_state.current_scenario.get('goal')}*")

        if st.button("🔄 Restart Scenario", use_container_width=True):
            st.session_state.customer_frustration = st.session_state.current_scenario["initial_frustration"]
            st.session_state.customer_mood = st.session_state.current_scenario["initial_mood"]
            st.session_state.messages = [
                {"role": "customer", "content": st.session_state.current_scenario["initial_message"]}
            ]
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                st.session_state.current_scenario["initial_message"],
                st.session_state.messages
            )
            st.rerun()

    elif st.session_state.mode == "Replay Mode":
        st.subheader("📼 Replay Library")
        transcript_titles = [t["title"] for t in replay_transcripts]
        selected_trans_title = st.selectbox("Choose Recorded Session", transcript_titles)
        chosen_trans = next((t for t in replay_transcripts if t["title"] == selected_trans_title), replay_transcripts[0])
        
        if chosen_trans["id"] != st.session_state.selected_transcript.get("id"):
            st.session_state.selected_transcript = chosen_trans
            st.session_state.replay_index = 0
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()

        st.markdown(f"**Turns:** {len(st.session_state.selected_transcript.get('turns', []))}")
        st.markdown(f"**Progress:** Step {st.session_state.replay_index} / {len(st.session_state.selected_transcript.get('turns', []))}")

        if st.button("🔄 Reset Replay", use_container_width=True):
            st.session_state.replay_index = 0
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()

    elif st.session_state.mode == "Manual Mode":
        st.subheader("✍️ Live Agent Assistant")
        st.write("Paste customer messages directly in the conversation pane to receive instant RAG recommendations, escalation risk alerts, and response suggestions.")
        if st.button("🗑️ Clear Session", use_container_width=True):
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()


# Initialize Simulator message if empty
if st.session_state.mode == "Simulator Mode" and not st.session_state.messages and scenarios:
    st.session_state.messages = [
        {"role": "customer", "content": st.session_state.current_scenario["initial_message"]}
    ]
    st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
        st.session_state.current_scenario["initial_message"],
        st.session_state.messages
    )


# --------------------------------------------------
# MAIN LAYOUT: CENTER PANEL (Chat) & RIGHT PANEL (Coaching)
# --------------------------------------------------
col_chat, col_coaching = st.columns([6, 5], gap="large")


# --------------------------------------------------
# PANEL 2: LIVE CONVERSATION CONSOLE (Center Panel)
# --------------------------------------------------
with col_chat:
    st.subheader("💬 Live Support Interaction")

    # Display Conversation Stream
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]
            if role == "customer":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"**Customer ({st.session_state.current_scenario.get('customer_name', 'Customer')}):** {content}")
            else:
                with st.chat_message("assistant", avatar="🎧"):
                    st.markdown(f"**Support Representative (You):** {content}")

    st.markdown("---")

    # Interaction Inputs based on Mode
    if st.session_state.mode == "Simulator Mode":
        # Form for sending agent reply
        with st.form(key="agent_reply_form", clear_on_submit=True):
            agent_input = st.text_area(
                "Your Response to Customer:",
                value=st.session_state.draft_reply,
                height=90,
                placeholder="Type your professional response or click a 1-Click Suggestion on the right..."
            )
            submit_agent = st.form_submit_button("Send Response 🚀", use_container_width=True)

        if submit_agent and agent_input.strip():
            # 1. Add Agent reply
            st.session_state.messages.append({"role": "agent", "content": agent_input.strip()})
            st.session_state.draft_reply = ""

            # 2. Simulate Customer Turn
            sim_result = CoachingOrchestrator.simulate_next_customer_turn(
                scenario=st.session_state.current_scenario,
                conversation_history=st.session_state.messages,
                current_frustration=st.session_state.customer_frustration,
                current_mood=st.session_state.customer_mood
            )

            st.session_state.customer_frustration = sim_result["new_frustration"]
            st.session_state.customer_mood = sim_result["new_mood"]
            st.session_state.messages.append({"role": "customer", "content": sim_result["message"]})

            # 3. Trigger Coaching Pipeline
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                sim_result["message"],
                st.session_state.messages
            )
            st.rerun()

    elif st.session_state.mode == "Manual Mode":
        with st.form(key="manual_customer_form", clear_on_submit=True):
            manual_input = st.text_area(
                "Paste Incoming Customer Message:",
                height=80,
                placeholder="Paste customer query here to analyze..."
            )
            submit_manual = st.form_submit_button("Analyze & Coach ⚡", use_container_width=True)

        if submit_manual and manual_input.strip():
            st.session_state.messages.append({"role": "customer", "content": manual_input.strip()})
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                manual_input.strip(),
                st.session_state.messages
            )
            st.rerun()

    elif st.session_state.mode == "Replay Mode":
        turns = st.session_state.selected_transcript.get("turns", [])
        curr_idx = st.session_state.replay_index
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            next_step = st.button("⏩ Play Next Message", use_container_width=True, disabled=(curr_idx >= len(turns)))
        with col_r2:
            auto_play = st.button("⏪ Reset to Start", use_container_width=True)

        if next_step and curr_idx < len(turns):
            turn_data = turns[curr_idx]
            st.session_state.messages.append({"role": turn_data["role"], "content": turn_data["message"]})
            st.session_state.replay_index += 1
            if turn_data["role"] == "customer":
                st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                    turn_data["message"],
                    st.session_state.messages
                )
            st.rerun()

        if auto_play:
            st.session_state.replay_index = 0
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()


# --------------------------------------------------
# PANEL 3: REAL-TIME COACHING & INTELLIGENCE (Right Panel)
# --------------------------------------------------
with col_coaching:
    st.subheader("💡 Real-Time Coaching & RAG")

    if st.session_state.coaching_data:
        coach = st.session_state.coaching_data
        sentiment = coach.get("sentiment", {})
        escalation = coach.get("escalation", {})
        coaching = coach.get("coaching", {})
        knowledge = coach.get("knowledge", [])

        # 1. Escalation Risk Alert Banner
        risk_score = escalation.get("escalation_risk", 20)
        risk_level = escalation.get("risk_level", "LOW")
        color_hex = escalation.get("color_hex", "#10B981")

        if escalation.get("alert_required", False):
            st.markdown(f"""
            <div class="alert-card">
                <strong>🚨 CRITICAL ESCALATION RISK ALERT ({risk_score}%)</strong><br>
                <span>{escalation.get('intervention_strategy')}</span>
            </div>
            """, unsafe_allow_html=True)

        # 2. Risk & Sentiment Dashboard Cards
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <small style="color: #94A3B8;">ESCALATION RISK</small><br>
                <strong style="font-size: 1.3rem; color: {color_hex};">{risk_score}% ({risk_level})</strong>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(1.0, risk_score / 100.0))

        with m_col2:
            frust = sentiment.get("frustration_level", 5)
            mood = sentiment.get("emotional_state", "Neutral")
            f_color = "#EF4444" if frust >= 7 else ("#F59E0B" if frust >= 4 else "#10B981")
            st.markdown(f"""
            <div class="metric-card">
                <small style="color: #94A3B8;">CUSTOMER MOOD / INTENT</small><br>
                <strong style="font-size: 1.1rem; color: {f_color};">{mood} ({frust}/10)</strong><br>
                <small style="color: #38BDF8;">Intent: {sentiment.get('intent', 'INQUIRY')}</small>
            </div>
            """, unsafe_allow_html=True)

        # 3. Real-Time Coaching Tips
        with st.container():
            st.markdown("##### 🎯 Real-Time Coaching Guidance")
            for tip in coaching.get("coaching_tips", []):
                st.info(f"💡 {tip}")

        # 4. 1-Click Response Suggestions
        st.markdown("##### ⚡ 1-Click Response Suggestions")
        suggestions = coaching.get("suggested_responses", [])
        for idx, sug in enumerate(suggestions):
            with st.expander(f"Option {idx+1}: {sug.get('label', 'Suggested Reply')}", expanded=(idx==0)):
                st.write(sug.get("text"))
                if st.button(f"Use Suggestion #{idx+1}", key=f"use_sug_{idx}"):
                    st.session_state.draft_reply = sug.get("text")
                    st.rerun()

        # 5. RAG Knowledge Recommendations
        st.markdown("##### 📚 Relevant Knowledge Base (RAG)")
        if knowledge:
            for k in knowledge:
                with st.expander(f"📄 {k.get('source')} (Page: {k.get('page')}) — Match: {int(k.get('score', 0)*100)}%"):
                    st.write(k.get("text"))
        else:
            st.caption("No specific knowledge base chunk retrieved.")

    else:
        st.info("👋 Start or select a session to see real-time coaching insights, sentiment tracking, and RAG suggestions.")