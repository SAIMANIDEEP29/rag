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
# COMPREHENSIVE DESIGN TOKENS & HIGH-SPECIFICITY CSS
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #F7F8FA;
        --surface: #FFFFFF;
        --surface-muted: #F9FAFB;
        --border: #E5E7EB;
        --border-strong: #D1D5DB;
        --text-primary: #111827;
        --text-secondary: #374151;
        --text-muted: #6B7280;
        --text-placeholder: #9CA3AF;
        --primary: #2563EB;
        --primary-hover: #1D4ED8;
        --success: #16A34A;
        --warning: #D97706;
        --danger: #DC2626;
    }

    /* Base reset */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: var(--bg) !important;
        color: var(--text-primary) !important;
    }

    /* Force all Streamlit markdown containers to use dark text */
    [data-testid="stMarkdownContainer"], 
    [data-testid="stMarkdownContainer"] p, 
    [data-testid="stMarkdownContainer"] span, 
    [data-testid="stMarkdownContainer"] div, 
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] li {
        color: var(--text-primary) !important;
    }

    /* Make header transparent but keep collapsed sidebar button visible & accessible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        height: 0px !important;
    }

    /* Prominent Sidebar Expand Button (when collapsed) */
    div[data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 999999 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        color: #111827 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
        cursor: pointer !important;
    }
    div[data-testid="collapsedControl"]:hover {
        background-color: #F3F4F6 !important;
        border-color: #9CA3AF !important;
    }
    div[data-testid="collapsedControl"] svg {
        stroke: #111827 !important;
        fill: #111827 !important;
    }

    .block-container {
        padding: 1rem 2rem 2rem 2rem !important;
        max-width: 100% !important;
    }

    /* --------------------------------------------- */
    /* TOP NAVIGATION (54px)                         */
    /* --------------------------------------------- */
    .top-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 54px;
        background: var(--surface);
        border: 1px solid var(--border);
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
        color: var(--text-primary) !important;
    }
    .top-navbar-center {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: var(--text-muted) !important;
    }
    .top-navbar-center strong {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    .top-navbar-status {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 12px;
        font-weight: 600;
        color: var(--success) !important;
        background: #F0FDF4;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #DCFCE7;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--success);
    }

    /* --------------------------------------------- */
    /* SIDEBAR NAVIGATION                            */
    /* --------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
        padding: 1rem 0.75rem !important;
        z-index: 1000 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: var(--text-secondary) !important;
    }

    .nav-category {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted) !important;
        margin-top: 16px;
        margin-bottom: 8px;
        padding-left: 6px;
    }

    /* Radio Navigation in Sidebar */
    div[data-testid="stRadio"] {
        margin-bottom: 4px;
    }
    div[data-testid="stRadio"] > div {
        gap: 3px !important;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        padding: 7px 10px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        transition: all 150ms ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #F3F4F6 !important;
    }
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label div {
        font-size: 13.5px !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #EFF6FF !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) p,
    div[data-testid="stRadio"] label:has(input:checked) span {
        color: #1D4ED8 !important;
        font-weight: 600 !important;
    }

    /* --------------------------------------------- */
    /* SELECTBOX / DROPDOWN FIXES                    */
    /* --------------------------------------------- */
    div[data-testid="stSelectbox"] label p {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--text-muted) !important;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--surface) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
    }
    div[data-baseweb="select"] * {
        color: var(--text-primary) !important;
        font-size: 13.5px !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="popover"] ul {
        background-color: var(--surface) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-baseweb="popover"] li {
        color: var(--text-primary) !important;
        background-color: var(--surface) !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #F3F4F6 !important;
    }

    /* --------------------------------------------- */
    /* TEXTAREA & FORM FIXES                         */
    /* --------------------------------------------- */
    .stTextArea textarea {
        background-color: var(--surface) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        padding: 12px 14px !important;
    }
    .stTextArea textarea::placeholder {
        color: var(--text-placeholder) !important;
        opacity: 1 !important;
    }
    .stTextArea textarea::-webkit-input-placeholder {
        color: var(--text-placeholder) !important;
        opacity: 1 !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }

    /* --------------------------------------------- */
    /* BUTTONS FIXES                                 */
    /* --------------------------------------------- */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        background-color: #111827 !important;
        color: #FFFFFF !important;
        border: 1px solid #111827 !important;
        height: 40px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        transition: all 150ms ease !important;
    }
    div[data-testid="stFormSubmitButton"] button p,
    div[data-testid="stFormSubmitButton"] button span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #1F2937 !important;
        border-color: #1F2937 !important;
        color: #FFFFFF !important;
    }

    .stButton > button {
        background-color: var(--surface) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 6px 12px !important;
        transition: all 150ms ease !important;
    }
    .stButton > button p, .stButton > button span {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background-color: var(--surface-muted) !important;
        border-color: var(--text-muted) !important;
        color: var(--text-primary) !important;
    }
    .stButton > button:hover p {
        color: var(--text-primary) !important;
    }

    /* --------------------------------------------- */
    /* SAAS PANELS & CARDS                           */
    /* --------------------------------------------- */
    .saas-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .card-header-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Customer Header */
    .customer-header-box {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .customer-profile {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .customer-avatar-badge {
        width: 38px;
        height: 38px;
        border-radius: 6px;
        background: #F3F4F6;
        color: #374151;
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid var(--border);
    }
    .customer-name-heading {
        font-size: 14.5px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.2;
    }
    .customer-meta-sub {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 2px;
    }

    /* Status Pills */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 12px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 4px;
    }
    .badge-danger { background: #FEF2F2; color: var(--danger); border: 1px solid #FEE2E2; }
    .badge-warning { background: #FFFBEB; color: var(--warning); border: 1px solid #FEF3C7; }
    .badge-success { background: #F0FDF4; color: var(--success); border: 1px solid #DCFCE7; }
    .badge-neutral { background: #F3F4F6; color: var(--text-secondary); border: 1px solid var(--border); }

    /* Conversation Message Bubbles */
    .msg-bubble {
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 13.5px;
        line-height: 1.5;
        border: 1px solid var(--border);
        margin-bottom: 10px;
    }
    .msg-customer {
        background: var(--surface);
        border-left: 3px solid #6B7280;
    }
    .msg-agent {
        background: #F9FAFB;
        border-left: 3px solid var(--primary);
    }
    .msg-meta-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 11.5px;
        color: var(--text-muted);
    }
    .msg-author {
        font-weight: 600;
        color: var(--text-primary);
    }
    .msg-body-text {
        color: var(--text-secondary);
    }

    /* Signals Rows in Copilot */
    .signal-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #F3F4F6;
        font-size: 13px;
    }
    .signal-k {
        color: var(--text-muted);
        font-weight: 500;
    }
    .signal-v {
        font-weight: 600;
        color: var(--text-primary);
    }

    /* Coaching Action Panel */
    .action-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 3px solid var(--primary);
        border-radius: 6px;
        padding: 12px;
        margin-top: 4px;
    }
    .action-head {
        font-size: 13px;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .action-body {
        font-size: 12.5px;
        color: #334155;
        line-height: 1.45;
    }

    /* Response Suggestion Cards */
    .sug-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 10px 12px;
        margin-bottom: 10px;
    }
    .sug-pill {
        font-size: 11px;
        font-weight: 600;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 5px;
    }
    .sug-content {
        font-size: 12.5px;
        color: var(--text-secondary);
        line-height: 1.45;
        margin-bottom: 8px;
    }

    /* Mode Pill Buttons in Header */
    .nav-pill-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 12.5px;
        font-weight: 500;
        text-decoration: none;
        cursor: pointer;
        border: 1px solid var(--border-strong);
        background: #FFFFFF;
        color: var(--text-secondary);
        transition: all 150ms ease;
    }
    .nav-pill-btn:hover {
        background: #F3F4F6;
        color: var(--text-primary);
    }
    .nav-pill-btn.active {
        background: #EFF6FF;
        border-color: #BFDBFE;
        color: #1D4ED8;
        font-weight: 600;
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


# --------------------------------------------------
# SIDEBAR NAVIGATION (Focused & 100% Functional)
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding: 4px 6px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
            <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
        </svg>
        <span style="font-size: 15px; font-weight: 600; color: #111827;">Support Console</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-category">Workspace Mode</div>', unsafe_allow_html=True)
    
    mode_options = ["Live Simulator", "Manual Analysis", "Replay Library"]
    current_mode_idx = 0 if st.session_state.mode == "Simulator Mode" else (1 if st.session_state.mode == "Manual Mode" else 2)
    
    selected_nav = st.radio(
        "Workspace View",
        mode_options,
        index=current_mode_idx,
        label_visibility="collapsed"
    )

    target_mode = "Simulator Mode" if selected_nav == "Live Simulator" else ("Manual Mode" if selected_nav == "Manual Analysis" else "Replay Mode")
    if target_mode != st.session_state.mode:
        st.session_state.mode = target_mode
        st.session_state.messages = []
        st.session_state.coaching_data = None
        st.session_state.replay_index = 0
        st.rerun()

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

    # Mode Context & Controls
    if st.session_state.mode == "Simulator Mode":
        st.markdown('<div class="nav-category">Scenario Configuration</div>', unsafe_allow_html=True)
        scenario_titles = [s["title"] for s in scenarios]
        selected_title = st.selectbox("Scenario Selector", scenario_titles, label_visibility="collapsed")
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

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
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
        st.markdown('<div class="nav-category">Recorded Transcript</div>', unsafe_allow_html=True)
        transcript_titles = [t["title"] for t in replay_transcripts]
        selected_trans_title = st.selectbox("Transcript Selector", transcript_titles, label_visibility="collapsed")
        chosen_trans = next((t for t in replay_transcripts if t["title"] == selected_trans_title), replay_transcripts[0])
        
        if chosen_trans["id"] != st.session_state.selected_transcript.get("id"):
            st.session_state.selected_transcript = chosen_trans
            st.session_state.replay_index = 0
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Reset Timeline", use_container_width=True):
            st.session_state.replay_index = 0
            st.session_state.messages = []
            st.session_state.coaching_data = None
            st.rerun()

    elif st.session_state.mode == "Manual Mode":
        st.markdown('<div class="nav-category">Analyst Tools</div>', unsafe_allow_html=True)
        st.caption("Paste customer queries into the central workspace to receive real-time intent, escalation risk, and coaching guidance.")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Clear Analyst Session", use_container_width=True):
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
# TOP HEADER BAR
# --------------------------------------------------
case_label = "Training Session" if st.session_state.mode == "Simulator Mode" else ("Manual Analysis" if st.session_state.mode == "Manual Mode" else "Replay Session")
sub_label = st.session_state.current_scenario.get("title", "Active Session") if st.session_state.mode == "Simulator Mode" else (st.session_state.selected_transcript.get("title", "Transcript") if st.session_state.mode == "Replay Mode" else "Ad-hoc Query")

st.markdown(f"""
<div class="top-navbar">
    <div class="top-navbar-brand">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
            <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
        </svg>
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
# DESKTOP LAYOUT (Center Conversation & Right Copilot)
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

    badge_class = "badge-danger" if frust >= 7 else ("badge-warning" if frust >= 4 else "badge-success")

    st.markdown(f"""
    <div class="customer-header-box">
        <div class="customer-profile">
            <div class="customer-avatar-badge">{cust_name[:2].upper()}</div>
            <div>
                <h4 class="customer-name-heading">{cust_name}</h4>
                <div class="customer-meta-sub">{cust_plan} · Case #{abs(hash(cust_name)) % 9000 + 1000}</div>
            </div>
        </div>
        <div>
            <span class="status-badge {badge_class}">● {mood_str} ({frust}/10)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Conversation Message Stream
    st.markdown('<div class="card-header-label">Conversation</div>', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for idx, msg in enumerate(st.session_state.messages):
            is_cust = (msg["role"] == "customer")
            sender = cust_name if is_cust else "You (Support Representative)"
            role_label = "Customer · 2:14 PM" if is_cust else "Agent · 2:15 PM"
            bubble_class = "msg-customer" if is_cust else "msg-agent"
            
            st.markdown(f"""
            <div class="msg-bubble {bubble_class}">
                <div class="msg-meta-row">
                    <span class="msg-author">{sender}</span>
                    <span>{role_label}</span>
                </div>
                <div class="msg-body-text">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 24px; text-align: center; color: #6B7280; font-size: 13.5px; background: #FFFFFF; border: 1px dashed #E5E7EB; border-radius: 6px; margin-bottom: 12px;">
            No messages in this session yet.
        </div>
        """, unsafe_allow_html=True)

    # 3. Response Composer / Controls
    if st.session_state.mode == "Simulator Mode":
        st.markdown('<div class="card-header-label" style="margin-top: 14px;">Your Response</div>', unsafe_allow_html=True)
        with st.form(key="composer_form", clear_on_submit=True):
            agent_input = st.text_area(
                "Response Composer",
                value=st.session_state.draft_reply,
                height=95,
                placeholder="Type your response to the customer...",
                label_visibility="collapsed"
            )
            submit_agent = st.form_submit_button("Send Response", use_container_width=True)

        if submit_agent and agent_input.strip():
            st.session_state.messages.append({"role": "agent", "content": agent_input.strip()})
            st.session_state.draft_reply = ""

            sim_result = CoachingOrchestrator.simulate_next_customer_turn(
                scenario=st.session_state.current_scenario,
                conversation_history=st.session_state.messages,
                current_frustration=st.session_state.customer_frustration,
                current_mood=st.session_state.customer_mood
            )

            st.session_state.customer_frustration = sim_result["new_frustration"]
            st.session_state.customer_mood = sim_result["new_mood"]
            st.session_state.messages.append({"role": "customer", "content": sim_result["message"]})

            st.session_state.coaching_data = CoachingOrchestrator.process_customer_turn(
                sim_result["message"],
                st.session_state.messages
            )
            st.rerun()

    elif st.session_state.mode == "Manual Mode":
        st.markdown('<div class="card-header-label" style="margin-top: 14px;">Customer Message</div>', unsafe_allow_html=True)
        with st.form(key="manual_form", clear_on_submit=True):
            manual_input = st.text_area(
                "Customer Input",
                height=95,
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
        
        st.markdown('<div class="card-header-label" style="margin-top: 14px;">Timeline Navigation</div>', unsafe_allow_html=True)
        r_col1, r_col2, r_col3 = st.columns([3, 4, 3])
        with r_col1:
            prev_step = st.button("Previous Turn", use_container_width=True, disabled=(curr_idx <= 0))
        with r_col2:
            st.markdown(f"<div style='text-align: center; font-size: 13px; font-weight: 600; color: #374151; padding-top: 6px;'>Step {curr_idx} of {len(turns)}</div>", unsafe_allow_html=True)
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
    st.markdown('<div class="card-header-label">Agent Copilot</div>', unsafe_allow_html=True)

    if st.session_state.coaching_data:
        coach = st.session_state.coaching_data
        sentiment = coach.get("sentiment", {})
        escalation = coach.get("escalation", {})
        coaching = coach.get("coaching", {})
        knowledge = coach.get("knowledge", [])

        # 1. Customer Signals Card
        st.markdown("""
        <div class="saas-card">
            <div class="card-header-label">Customer Signals</div>
        """, unsafe_allow_html=True)

        sent_mood = sentiment.get("emotional_state", "Neutral")
        frust_level = sentiment.get("frustration_level", 5)
        intent_str = sentiment.get("intent", "General Inquiry").replace("_", " ").title()
        
        esc_score = escalation.get("escalation_risk", 25)
        esc_level = escalation.get("risk_level", "LOW").capitalize()

        esc_color = "#DC2626" if esc_score >= 70 else ("#D97706" if esc_score >= 40 else "#16A34A")

        st.markdown(f"""
            <div class="signal-item">
                <span class="signal-k">Sentiment</span>
                <span class="signal-v">{sent_mood} ({frust_level}/10)</span>
            </div>
            <div class="signal-item">
                <span class="signal-k">Intent</span>
                <span class="signal-v">{intent_str}</span>
            </div>
            <div class="signal-item" style="border-bottom: none;">
                <span class="signal-k">Escalation Risk</span>
                <span class="signal-v" style="color: {esc_color};">{esc_level} ({esc_score}%)</span>
            </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, esc_score / 100.0))
        st.markdown("</div>", unsafe_allow_html=True)

        # 2. Next Best Action Card
        st.markdown("""
        <div class="saas-card">
            <div class="card-header-label">Next Best Action</div>
        """, unsafe_allow_html=True)

        tips = coaching.get("coaching_tips", [])
        top_tip = tips[0] if tips else "Maintain professional and clear communication."
        
        st.markdown(f"""
        <div class="action-container">
            <div class="action-head">Recommended Guidance</div>
            <div class="action-body">{top_tip}</div>
        </div>
        """, unsafe_allow_html=True)

        if len(tips) > 1:
            with st.expander("Additional coaching notes", expanded=False):
                for t in tips[1:]:
                    st.markdown(f"<div style='font-size: 12px; color: #4B5563; margin-bottom: 4px;'>• {t}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Response Suggestions Card
        st.markdown("""
        <div class="saas-card">
            <div class="card-header-label">Response Suggestions</div>
        """, unsafe_allow_html=True)

        suggestions = coaching.get("suggested_responses", [])
        for idx, sug in enumerate(suggestions):
            label = sug.get("label", f"Suggestion {idx+1}")
            text_val = sug.get("text", "")
            
            st.markdown(f"""
            <div class="sug-card">
                <div class="sug-pill">{label}</div>
                <div class="sug-content">{text_val}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Insert Suggestion #{idx+1}", key=f"btn_sug_{idx}", use_container_width=True):
                st.session_state.draft_reply = text_val
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # 4. Knowledge Articles Card
        st.markdown("""
        <div class="saas-card">
            <div class="card-header-label">Knowledge Articles</div>
        """, unsafe_allow_html=True)

        if knowledge:
            for k in knowledge:
                source_name = k.get("source", "Knowledge Article").replace(".pdf", "").replace(".txt", "").replace("_", " ").title()
                with st.expander(f"{source_name} (Page {k.get('page')})", expanded=False):
                    st.markdown(f"<div style='font-size: 12.5px; color: #374151; line-height: 1.5;'>{k.get('text')}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size: 12.5px; color: #6B7280; padding: 4px 0;'>No relevant articles retrieved for this query.</div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="saas-card" style="text-align: center; padding: 28px 16px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="1.5" style="margin-bottom: 8px;">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <div style="font-size: 13.5px; font-weight: 600; color: #374151; margin-bottom: 4px;">No active session</div>
            <div style="font-size: 12px; color: #6B7280; max-width: 220px; margin: 0 auto;">
                Start a training simulation or select a transcript to view copilot guidance.
            </div>
        </div>
        """, unsafe_allow_html=True)