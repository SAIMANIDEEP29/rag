import streamlit as st
import json
import os
from datetime import datetime
from orchestrator import CoachingOrchestrator

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Support Console",
    page_icon="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/icons/headphones.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# ENTERPRISE B2B DESIGN SYSTEM & CSS
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global reset & typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #F7F8FA !important;
        color: #111827 !important;
    }

    /* Remove Streamlit default top decoration */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        height: 0px !important;
    }
    .stApp > header {
        display: none;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Top Navigation Bar */
    .top-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 52px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 0 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .top-navbar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 15px;
        font-weight: 600;
        color: #111827;
    }
    .top-navbar-center {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #6B7280;
    }
    .top-navbar-center strong {
        color: #111827;
        font-weight: 600;
    }
    .top-navbar-status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        font-weight: 500;
        color: #16A34A;
        background: #F0FDF4;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #DCFCE7;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #16A34A;
    }

    /* Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
        padding-top: 1rem !important;
        width: 260px !important;
    }
    .nav-section-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9CA3AF;
        margin-top: 16px;
        margin-bottom: 8px;
        padding-left: 8px;
    }
    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        color: #4B5563;
        text-decoration: none;
        margin-bottom: 2px;
        transition: all 150ms ease;
    }
    .nav-item:hover {
        background-color: #F3F4F6;
        color: #111827;
    }
    .nav-item.active {
        background-color: #EFF6FF;
        color: #2563EB;
        font-weight: 600;
    }

    /* Customer Header Component */
    .customer-header-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .customer-info-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .customer-avatar {
        width: 36px;
        height: 36px;
        border-radius: 6px;
        background: #F3F4F6;
        color: #4B5563;
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #E5E7EB;
    }
    .customer-name {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
        margin: 0;
        line-height: 1.2;
    }
    .customer-subtext {
        font-size: 12px;
        color: #6B7280;
        margin-top: 2px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 12px;
        font-weight: 500;
        padding: 3px 8px;
        border-radius: 4px;
    }
    .pill-danger { background: #FEF2F2; color: #DC2626; border: 1px solid #FEE2E2; }
    .pill-warning { background: #FFFBEB; color: #D97706; border: 1px solid #FEF3C7; }
    .pill-success { background: #F0FDF4; color: #16A34A; border: 1px solid #DCFCE7; }
    .pill-neutral { background: #F3F4F6; color: #4B5563; border: 1px solid #E5E7EB; }

    /* Surface & Container Panels */
    .saas-panel {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        margin-bottom: 16px;
    }
    .panel-header {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9CA3AF;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Message Stream */
    .message-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 16px;
    }
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 13.5px;
        line-height: 1.5;
        border: 1px solid #E5E7EB;
    }
    .customer-bubble {
        background: #FFFFFF;
        border-left: 3px solid #6B7280;
    }
    .agent-bubble {
        background: #F9FAFB;
        border-left: 3px solid #2563EB;
    }
    .bubble-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 12px;
        color: #6B7280;
    }
    .bubble-sender {
        font-weight: 600;
        color: #111827;
    }

    /* Copilot Signal Row */
    .signal-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #F3F4F6;
        font-size: 13px;
    }
    .signal-label {
        color: #6B7280;
        font-weight: 500;
    }
    .signal-val {
        font-weight: 600;
        color: #111827;
    }

    /* Action & Suggestion Cards */
    .action-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 12px;
    }
    .action-title {
        font-size: 13px;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .action-desc {
        font-size: 12.5px;
        color: #475569;
        line-height: 1.4;
    }

    .suggestion-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 8px;
        transition: border-color 150ms ease;
    }
    .suggestion-card:hover {
        border-color: #CBD5E1;
    }
    .suggestion-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }
    .suggestion-badge {
        font-size: 11px;
        font-weight: 600;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .suggestion-text {
        font-size: 12.5px;
        color: #374151;
        line-height: 1.45;
        margin-bottom: 8px;
    }

    /* Progress bar custom styling */
    .stProgress > div > div > div > div {
        background-color: #2563EB !important;
    }

    /* Button overrides */
    .stButton > button {
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 6px 14px !important;
        border: 1px solid #E5E7EB !important;
        transition: all 150ms ease !important;
    }
    .stButton > button:hover {
        border-color: #D1D5DB !important;
        background-color: #F9FAFB !important;
    }
    .primary-btn button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
    }
    .primary-btn button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    /* Textareas & Inputs */
    .stTextArea textarea {
        border-radius: 6px !important;
        border: 1px solid #E5E7EB !important;
        font-size: 13.5px !important;
        padding: 10px 12px !important;
        color: #111827 !important;
        background: #FFFFFF !important;
    }
    .stTextArea textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 1px #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# STATE INITIALIZATION
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

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Live Simulator"


# --------------------------------------------------
# SIDEBAR NAVIGATION (Enterprise Structure)
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding: 4px 8px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
            <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
        </svg>
        <span style="font-size: 15px; font-weight: 600; color: #111827;">Support Console</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">Workspace</div>', unsafe_allow_html=True)
    
    # Mode mapping
    mode_options = ["Live Simulator", "Manual Analysis", "Replay Library"]
    current_mode_idx = 0 if st.session_state.mode == "Simulator Mode" else (1 if st.session_state.mode == "Manual Mode" else 2)
    
    selected_nav = st.radio(
        "Workspace View",
        mode_options,
        index=current_mode_idx,
        label_visibility="collapsed"
    )

    # Sync navigation to internal mode
    target_mode = "Simulator Mode" if selected_nav == "Live Simulator" else ("Manual Mode" if selected_nav == "Manual Analysis" else "Replay Mode")
    if target_mode != st.session_state.mode:
        st.session_state.mode = target_mode
        st.session_state.messages = []
        st.session_state.coaching_data = None
        st.session_state.replay_index = 0
        st.rerun()

    st.markdown('<div class="nav-section-label">Training</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 2px; padding-left: 4px;">
        <div class="nav-item">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"></path></svg>
            <span>Knowledge Base</span>
        </div>
        <div class="nav-item">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"></path><path d="m19 9-5 5-4-4-3 3"></path></svg>
            <span>Performance</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">System</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding-left: 4px;">
        <div class="nav-item">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            <span>Settings</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Compact Context Selector inside Sidebar
    if st.session_state.mode == "Simulator Mode":
        st.markdown('<div class="nav-section-label">Scenario Configuration</div>', unsafe_allow_html=True)
        scenario_titles = [s["title"] for s in scenarios]
        selected_title = st.selectbox("Scenario", scenario_titles, label_visibility="collapsed")
        chosen_scen = next((s for s in scenarios if s["title"] == selected_title), scenarios[0])
        
        if chosen_scen["id"] != st.session_state.current_scenario.get("id"):
            st.session_state.current_scenario = chosen_scen
            st.session_state.customer_frustration = chosen_scen["initial_frustration"]
            st.session_state.customer_mood = chosen_scen["initial_mood"]
            st.session_state.messages = [{"role": "customer", "content": chosen_scen["initial_message"]}]
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                chosen_scen["initial_message"],
                st.session_state.messages
            )
            st.rerun()

        if st.button("Reset Scenario", use_container_width=True):
            st.session_state.customer_frustration = st.session_state.current_scenario["initial_frustration"]
            st.session_state.customer_mood = st.session_state.current_scenario["initial_mood"]
            st.session_state.messages = [{"role": "customer", "content": st.session_state.current_scenario["initial_message"]}]
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                st.session_state.current_scenario["initial_message"],
                st.session_state.messages
            )
            st.rerun()

    elif st.session_state.mode == "Replay Mode":
        st.markdown('<div class="nav-section-label">Recorded Session</div>', unsafe_allow_html=True)
        transcript_titles = [t["title"] for t in replay_transcripts]
        selected_trans_title = st.selectbox("Transcript", transcript_titles, label_visibility="collapsed")
        chosen_trans = next((t for t in replay_transcripts if t["title"] == selected_trans_title), replay_transcripts[0])
        
        if chosen_trans["id"] != st.session_state.selected_transcript.get("id"):
            st.session_state.selected_transcript = chosen_trans
            st.session_state.replay_index = 0
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()

        if st.button("Reset Timeline", use_container_width=True):
            st.session_state.replay_index = 0
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
# TOP HEADER BAR (52px Enterprise Navigation)
# --------------------------------------------------
case_label = "Training Simulation" if st.session_state.mode == "Simulator Mode" else ("Manual Analysis" if st.session_state.mode == "Manual Mode" else "Replay Session")
sub_label = st.session_state.current_scenario.get("title", "Active Session") if st.session_state.mode == "Simulator Mode" else (st.session_state.selected_transcript.get("title", "Transcript") if st.session_state.mode == "Replay Mode" else "Live Ad-hoc Query")

st.markdown(f"""
<div class="top-navbar">
    <div class="top-navbar-brand">
        <span>Support Console</span>
    </div>
    <div class="top-navbar-center">
        <span>{case_label}</span>
        <span style="color: #D1D5DB;">/</span>
        <strong>{sub_label}</strong>
    </div>
    <div class="top-navbar-status">
        <div class="status-dot"></div>
        <span>Session Active</span>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MAIN DESKTOP LAYOUT (Center Conversation & Right Copilot)
# --------------------------------------------------
col_chat, col_copilot = st.columns([6, 4], gap="medium")


# --------------------------------------------------
# CENTER PANEL: CONVERSATION WORKSPACE
# --------------------------------------------------
with col_chat:
    
    # 1. Customer Context Header
    cust_name = st.session_state.current_scenario.get("customer_name", "Marcus Vance") if st.session_state.mode == "Simulator Mode" else ("Analyst Workspace" if st.session_state.mode == "Manual Mode" else "Recorded Transcript")
    cust_plan = st.session_state.current_scenario.get("category", "Support Case") if st.session_state.mode == "Simulator Mode" else "General Support"
    
    frust = st.session_state.customer_frustration if st.session_state.mode == "Simulator Mode" else 5
    if st.session_state.coaching_data and "sentiment" in st.session_state.coaching_data:
        frust = st.session_state.coaching_data["sentiment"].get("frustration_level", frust)
        mood_str = st.session_state.coaching_data["sentiment"].get("emotional_state", "Neutral")
    else:
        mood_str = st.session_state.customer_mood

    pill_class = "pill-danger" if frust >= 7 else ("pill-warning" if frust >= 4 else "pill-success")

    st.markdown(f"""
    <div class="customer-header-card">
        <div class="customer-info-left">
            <div class="customer-avatar">{cust_name[:2].upper()}</div>
            <div>
                <h4 class="customer-name">{cust_name}</h4>
                <div class="customer-subtext">{cust_plan} · Case #{hash(cust_name) % 9000 + 1000}</div>
            </div>
        </div>
        <div>
            <span class="status-pill {pill_class}">● {mood_str} ({frust}/10)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Conversation Message Stream
    st.markdown('<div class="panel-header">Conversation</div>', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for idx, msg in enumerate(st.session_state.messages):
            is_cust = (msg["role"] == "customer")
            sender = cust_name if is_cust else "You (Support Agent)"
            role_label = "Customer" if is_cust else "Agent"
            bubble_class = "customer-bubble" if is_cust else "agent-bubble"
            
            st.markdown(f"""
            <div class="chat-bubble {bubble_class}">
                <div class="bubble-meta">
                    <span class="bubble-sender">{sender}</span>
                    <span>{role_label}</span>
                </div>
                <div style="color: #1F2937;">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 24px; text-align: center; color: #6B7280; font-size: 13px; background: #FFFFFF; border: 1px dashed #E5E7EB; border-radius: 8px;">
            No messages in this session yet.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 3. Response Composer / Interaction Toolbar
    if st.session_state.mode == "Simulator Mode":
        st.markdown('<div class="panel-header">Your Response</div>', unsafe_allow_html=True)
        with st.form(key="agent_composer_form", clear_on_submit=True):
            agent_input = st.text_area(
                "Response Composer",
                value=st.session_state.draft_reply,
                height=95,
                placeholder="Type your response to the customer...",
                label_visibility="collapsed"
            )
            c1, c2 = st.columns([7, 3])
            with c1:
                st.caption("Press Send Response to submit and progress customer simulation.")
            with c2:
                submit_agent = st.form_submit_button("Send Response", use_container_width=True)

        if submit_agent and agent_input.strip():
            # Add Agent Reply
            st.session_state.messages.append({"role": "agent", "content": agent_input.strip()})
            st.session_state.draft_reply = ""

            # Simulate Next Customer Turn
            sim_result = CoachingOrchestrator.simulate_next_customer_turn(
                scenario=st.session_state.current_scenario,
                conversation_history=st.session_state.messages,
                current_frustration=st.session_state.customer_frustration,
                current_mood=st.session_state.customer_mood
            )

            st.session_state.customer_frustration = sim_result["new_frustration"]
            st.session_state.customer_mood = sim_result["new_mood"]
            st.session_state.messages.append({"role": "customer", "content": sim_result["message"]})

            # Run Coaching Pipeline
            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                sim_result["message"],
                st.session_state.messages
            )
            st.rerun()

    elif st.session_state.mode == "Manual Mode":
        st.markdown('<div class="panel-header">Customer Message</div>', unsafe_allow_html=True)
        with st.form(key="manual_input_form", clear_on_submit=True):
            manual_input = st.text_area(
                "Customer Input",
                height=90,
                placeholder="Paste incoming customer query here to analyze...",
                label_visibility="collapsed"
            )
            submit_manual = st.form_submit_button("Analyze Message", use_container_width=True)

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
        
        st.markdown('<div class="panel-header">Timeline Navigation</div>', unsafe_allow_html=True)
        r_col1, r_col2, r_col3 = st.columns([3, 4, 3])
        with r_col1:
            prev_step = st.button("Previous Turn", use_container_width=True, disabled=(curr_idx <= 0))
        with r_col2:
            st.markdown(f"<div style='text-align: center; font-size: 13px; font-weight: 600; color: #4B5563; padding-top: 6px;'>Step {curr_idx} of {len(turns)}</div>", unsafe_allow_html=True)
        with r_col3:
            next_step = st.button("Next Turn", use_container_width=True, disabled=(curr_idx >= len(turns)))

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

        if prev_step and curr_idx > 0:
            st.session_state.messages = st.session_state.messages[:-1]
            st.session_state.replay_index -= 1
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "customer":
                st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                    st.session_state.messages[-1]["content"],
                    st.session_state.messages
                )
            st.rerun()


# --------------------------------------------------
# RIGHT PANEL: AGENT COPILOT
# --------------------------------------------------
with col_copilot:
    st.markdown('<div class="panel-header">Agent Copilot</div>', unsafe_allow_html=True)

    if st.session_state.coaching_data:
        coach = st.session_state.coaching_data
        sentiment = coach.get("sentiment", {})
        escalation = coach.get("escalation", {})
        coaching = coach.get("coaching", {})
        knowledge = coach.get("knowledge", [])

        # 1. Customer Signals Card
        st.markdown("""
        <div class="saas-panel">
            <div class="panel-header">Customer Signals</div>
        """, unsafe_allow_html=True)

        sent_score = sentiment.get("sentiment_score", 0.0)
        sent_mood = sentiment.get("emotional_state", "Neutral")
        frust_level = sentiment.get("frustration_level", 5)
        intent_str = sentiment.get("intent", "General Inquiry").replace("_", " ").title()
        
        esc_score = escalation.get("escalation_risk", 25)
        esc_level = escalation.get("risk_level", "LOW").capitalize()

        st.markdown(f"""
            <div class="signal-row">
                <span class="signal-label">Sentiment</span>
                <span class="signal-val">{sent_mood} ({frust_level}/10)</span>
            </div>
            <div class="signal-row">
                <span class="signal-label">Intent</span>
                <span class="signal-val">{intent_str}</span>
            </div>
            <div class="signal-row" style="border-bottom: none;">
                <span class="signal-label">Escalation Risk</span>
                <span class="signal-val">{esc_level} ({esc_score}%)</span>
            </div>
        """, unsafe_allow_html=True)

        # Restrained progress indicator
        st.progress(min(1.0, esc_score / 100.0))
        st.markdown("</div>", unsafe_allow_html=True)

        # Critical escalation notice if alert is required
        if escalation.get("alert_required", False):
            st.markdown(f"""
            <div style="background: #FEF2F2; border: 1px solid #FEE2E2; border-left: 3px solid #DC2626; border-radius: 6px; padding: 10px 12px; margin-bottom: 14px; font-size: 12.5px; color: #991B1B;">
                <strong>Escalation Risk Notice:</strong> {escalation.get('intervention_strategy')}
            </div>
            """, unsafe_allow_html=True)

        # 2. Next Best Action (Coaching)
        st.markdown("""
        <div class="saas-panel">
            <div class="panel-header">Next Best Action</div>
        """, unsafe_allow_html=True)

        tips = coaching.get("coaching_tips", [])
        if tips:
            st.markdown(f"""
            <div class="action-card">
                <div class="action-title">Recommended Guidance</div>
                <div class="action-desc">{tips[0]}</div>
            </div>
            """, unsafe_allow_html=True)
            if len(tips) > 1:
                with st.expander("Additional coaching notes", expanded=False):
                    for t in tips[1:]:
                        st.markdown(f"<div style='font-size: 12.5px; color: #4B5563; margin-bottom: 6px;'>• {t}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Response Suggestions
        st.markdown("""
        <div class="saas-panel">
            <div class="panel-header">Response Suggestions</div>
        """, unsafe_allow_html=True)

        suggestions = coaching.get("suggested_responses", [])
        for idx, sug in enumerate(suggestions):
            label = sug.get("label", f"Suggestion {idx+1}")
            text_val = sug.get("text", "")
            
            st.markdown(f"""
            <div class="suggestion-card">
                <div class="suggestion-header">
                    <span class="suggestion-badge">{label}</span>
                </div>
                <div class="suggestion-text">{text_val}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Insert Suggestion #{idx+1}", key=f"ins_sug_{idx}", use_container_width=True):
                st.session_state.draft_reply = text_val
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # 4. Knowledge Articles
        st.markdown("""
        <div class="saas-panel">
            <div class="panel-header">Knowledge Articles</div>
        """, unsafe_allow_html=True)

        if knowledge:
            for k in knowledge:
                source_name = k.get("source", "Knowledge Article").replace(".pdf", "").replace(".txt", "").replace("_", " ").title()
                with st.expander(f"{source_name} (Page {k.get('page')})", expanded=False):
                    st.markdown(f"<div style='font-size: 12.5px; color: #374151; line-height: 1.5;'>{k.get('text')}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size: 12.5px; color: #6B7280;'>No relevant articles retrieved for this topic.</div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="saas-panel" style="text-align: center; padding: 32px 16px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="1.5" style="margin-bottom: 8px;">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <div style="font-size: 13.5px; font-weight: 600; color: #374151; margin-bottom: 4px;">No active session</div>
            <div style="font-size: 12.5px; color: #6B7280; max-width: 240px; margin: 0 auto 14px auto;">
                Start a training simulation or select a transcript to view copilot guidance.
            </div>
        </div>
        """, unsafe_allow_html=True)