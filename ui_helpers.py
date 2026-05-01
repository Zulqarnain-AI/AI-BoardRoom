"""
utils/ui_helpers.py
====================
Premium Boardroom UI Components & Styling
- Dark theme CSS (premium boardroom aesthetic)
- Agent cards with status indicators
- Styled chat bubbles for live session
- Insights & pitch rendering
- Professional animations & transitions
"""

import streamlit as st
from agent_definitions import AGENTS


def inject_custom_css():
    """Injects all custom CSS for premium dark boardroom theme."""
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary:      #05050a;
        --bg-secondary:    #0a0a10;
        --bg-card:         #0f0f1a;
        --bg-hover:        rgba(255,255,255,0.03);
        --border:          rgba(255,255,255,0.06);
        --border-accent:   rgba(255,255,255,0.10);
        --border-bright:   rgba(255,255,255,0.16);
        --text-primary:    #f5f5fa;
        --text-secondary:  #9090a8;
        --text-muted:      #5a5a70;
        --ceo:     #6366f1;
        --cto:     #10b981;
        --cfo:     #f59e0b;
        --cmo:     #ec4899;
        --investor:#a78bfa;
        --gold:    #fbbf24;
        --radius-sm:  8px;
        --radius:     12px;
        --radius-lg:  16px;
        --radius-xl:  20px;
    }

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    .main { background: var(--bg-primary) !important; }
    .block-container {
        padding: 1rem 1.5rem !important;
        max-width: 100% !important;
    }

    /* ── Page Header ── */
    .page-header {
        position: sticky;
        top: 0;
        z-index: 50;
        background: linear-gradient(180deg, rgba(5,5,10,0.95), rgba(5,5,10,0.7));
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
        padding: 1.5rem 0 0 0 ;
        margin-bottom:0.5rem;
        text-align:center;
    }
    .header-brand {
        font-family: 'Syne', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #fff, #a78bfa, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
    }
    .header-subtitle {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        color: var(--text-muted);
        text-transform: uppercase;
    }

    /* ── Hero Container ── */
    .hero-container {
        text-align: center;
        padding: 1rem 2rem;
    }
    .hero-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #fff, #c4b5fd, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    .hero-description {
        font-size: 1rem;
        color: var(--text-muted);
        max-width: 600px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }
    .agent-badges {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }

    /* ── Idea Input Container ── */
    .idea-input-container {
        background: var(--bg-card);
        border: 1px solid var(--border-accent);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin-bottom: 2rem;
    }

    /* ── 3-Column Layout Panels ── */
    .board-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-accent);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        height: fit-content;
        position: sticky;
        top: 140px;
    }
    .session-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-accent);
        border-radius: var(--radius-lg);
        padding: 0rem;
        min-height: 0px;
    }
    .controls-panel {
        background: var(--bg-card);
        border: 1px solid var(--border-accent);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        height: fit-content;
        position: sticky;
        top: 140px;
    }
    .panel-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: var(--text-primary);
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }

    /* ── Agent Cards ── */
    .agent-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.005));
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        cursor: default;
    }
    .agent-card:hover {
        border-color: var(--border-accent);
        background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    }
    .agent-card.speaking {
        border-color: currentColor;
        background: linear-gradient(135deg, var(--agent-color-light), rgba(255,255,255,0.02));
        box-shadow: 0 0 16px rgba(0,0,0,0.4);
    }
    .agent-card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.5rem;
    }
    .agent-card-emoji {
        font-size: 1.4rem;
    }
    .agent-card-info {
        flex: 1;
    }
    .agent-card-name {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        color: var(--text-primary);
    }
    .agent-card-role {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .agent-card-status {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 100px;
        font-family: 'DM Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        white-space: nowrap;
    }
    .agent-card-status.idle {
        background: rgba(255,255,255,0.05);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }
    .agent-card-status.spoken {
        background: rgba(99,102,241,0.15);
        color: var(--ceo);
        border: 1px solid rgba(99,102,241,0.3);
    }
    .agent-card-status.speaking {
        background: rgba(16,185,129,0.2);
        color: #10b981;
        border: 1px solid rgba(16,185,129,0.4);
        animation: pulse-status 1.5s ease-in-out infinite;
    }
    @keyframes pulse-status {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* ── Live Session ── */
    .empty-session {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 650px;
        color: var(--text-muted);
        font-style: italic;
        text-align: center;
        padding: 2rem;
        border: 2px dashed var(--border-accent);
        border-radius: var(--radius-lg);
    }

    /* ── Current Message Section ── */
    .current-message-section {
        background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.05));
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .current-message-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--ceo);
        margin-bottom: 0.75rem;
        display: block;
    }

    /* ── History Divider ── */
    .history-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
        margin: 1.5rem 0;
    }
    .history-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 1rem;
        display: block;
    }

    /* ── Chat Stream ── */
    .chat-stream {
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    /* ── Chat Bubble (Agent) ── */
    .chat-bubble-agent {
        display: flex;
        gap: 0.75rem;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
        animation: slideInUp 0.3s ease forwards;
        opacity: 0;
    }
    .chat-bubble-agent:last-child { border-bottom: none; }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .chat-bubble-agent:hover { background: var(--bg-hover); border-radius: var(--radius); padding-left: 0.5rem; padding-right: 0.5rem; }

    .bubble-avatar {
        width: 40px;
        height: 40px;
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
        border: 1px solid var(--border-accent);
    }
    .bubble-content {
        flex: 1;
        min-width: 0;
    }
    .bubble-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.4rem;
        flex-wrap: wrap;
    }
    .bubble-speaker {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .bubble-role-badge {
        font-family: 'DM Mono', monospace;
        font-size: 0.6rem;
        padding: 2px 6px;
        border-radius: 100px;
        background: var(--bg-hover);
        border: 1px solid var(--border);
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .bubble-text {
        font-size: 0.92rem;
        line-height: 1.7;
        color: var(--text-primary);
        word-wrap: break-word;
        overflow-wrap: break-word;
    }

    /* ── Chat Bubble (User/Chairperson) ── */
    .chat-bubble-user {
        display: flex;
        gap: 0.75rem;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
        animation: slideInUp 0.3s ease forwards;
        opacity: 0;
    }
    .chat-bubble-user:last-child { border-bottom: none; }
    .chat-bubble-user:hover { background: var(--bg-hover); border-radius: var(--radius); padding-left: 0.5rem; padding-right: 0.5rem; }

    /* ── Control Stats ── */
    .control-stat {
        font-size: 0.85rem;
        color: var(--text-secondary);
        padding: 0.5rem 0;
        display: flex;
        justify-content: space-between;
    }
    .control-stat strong {
        color: var(--text-primary);
        font-weight: 600;
    }

    /* ── Section Label ── */
    .section-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        display: block;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: var(--radius) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: #fff !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
    }
    .stButton > button[kind="secondary"] {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-accent) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: var(--bg-hover) !important;
        border-color: var(--border-bright) !important;
    }

    /* ── Text Areas & Inputs ── */
    textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-accent) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        resize: none !important;
        transition: border-color 0.2s !important;
    }
    textarea:focus {
        border-color: var(--ceo) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    }
    input[type="text"],
    input[type="password"],
    input[type="number"],
    input[type="email"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-accent) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        transition: border-color 0.2s !important;
    }
    input:focus {
        border-color: var(--ceo) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    }

    /* ── Select Box ── */
    [data-baseweb="select"] > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-accent) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border: none !important;
        gap: 0.5rem !important;
        padding: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.2s !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1)) !important;
        color: var(--text-primary) !important;
        border-color: var(--ceo) !important;
    }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

    /* ── Divider ── */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Pitch Section ── */
    .pitch-hero {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: linear-gradient(135deg, rgba(251,191,36,0.08), rgba(245,158,11,0.04));
        border: 1px solid rgba(251,191,36,0.15);
        border-radius: var(--radius-xl);
        margin-bottom: 2rem;
    }
    .pitch-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 0.75rem;
    }
    .pitch-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    .pitch-tagline {
        font-size: 1rem;
        color: var(--text-secondary);
        font-style: italic;
    }

    /* ── Pitch Card Grid ── */
    .pitch-card {
        background: var(--bg-card);
        border: 1px solid var(--border-accent);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        transition: all 0.2s ease;
    }
    .pitch-card:hover {
        border-color: var(--border-bright);
        transform: translateY(-1px);
    }
    .pitch-card-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        display: block;
    }
    .pitch-card-content {
        font-size: 0.92rem;
        line-height: 1.7;
        color: var(--text-primary);
    }

    /* ── Insights Container ── */
    .insight-item {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .insight-item strong {
        color: var(--gold);
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 100px;
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        border: 1px solid var(--border-accent);
        background: var(--bg-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        white-space: nowrap;
        margin: 0.25rem;
    }
    .badge.ceo      { border-color: rgba(99,102,241,0.4); color: var(--ceo); }
    .badge.cto      { border-color: rgba(16,185,129,0.4); color: var(--cto); }
    .badge.cfo      { border-color: rgba(245,158,11,0.4); color: var(--cfo); }
    .badge.cmo      { border-color: rgba(236,72,153,0.4); color: var(--cmo); }
    .badge.investor { border-color: rgba(167,139,250,0.4); color: var(--investor); }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebarContent"] {
        padding: 1.5rem 1rem !important;
    }

    /* ── Alerts ── */
    .stAlert {
        background: var(--bg-card) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border-accent) !important;
        font-size: 0.85rem !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: var(--ceo) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: var(--border-accent);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-bright);
    }

    /* ── Mobile Responsive ── */
    @media (max-width: 768px) {
        .block-container { padding: 0.75rem !important; }
        .page-header { padding: 1rem 0; margin-bottom: 1rem; }
        .board-panel, .controls-panel { position: static; top: auto; }
        .session-panel { min-height: auto; }
        .pitch-title { font-size: 1.6rem; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_chat_bubble(speaker: str, role: str, content: str, is_user: bool = False,
                       agent_color: str = "#6366f1", emoji: str = "🤖"):
    """Renders a styled chat bubble for either agent or chairperson."""
    safe_content = (content or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    if is_user:
        st.markdown(f"""
        <div class="chat-bubble-user">
            <div class="bubble-avatar" style="background:rgba(251,191,36,0.1);border-color:#fbbf2444;">
                🧑‍⚖️
            </div>
            <div class="bubble-content">
                <div class="bubble-header">
                    <span class="bubble-speaker" style="color:#fbbf24">{speaker}</span>
                    <span class="bubble-role-badge">Chairperson</span>
                </div>
                <div class="bubble-text">{safe_content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-bubble-agent">
            <div class="bubble-avatar" style="background:rgba({int(agent_color[1:3], 16)},{int(agent_color[3:5], 16)},{int(agent_color[5:7], 16)},0.12);border-color:{agent_color}44;">
                {emoji}
            </div>
            <div class="bubble-content">
                <div class="bubble-header">
                    <span class="bubble-speaker" style="color:{agent_color}">{speaker}</span>
                    <span class="bubble-role-badge">{role}</span>
                </div>
                <div class="bubble-text">{safe_content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_agent_card(agent: dict, status: str):
    """Renders an agent card in the left board members panel."""
    emoji = agent.get("emoji", "🤖")
    name = agent.get("name", "Agent")
    role = agent.get("role", "Unknown")
    color = agent.get("color", "#6366f1")

    status_text = "IDLE"
    status_class = "idle"
    if status == "speaking":
        status_text = "SPEAKING"
        status_class = "speaking"
    elif status == "spoken":
        status_text = "SPOKEN"
        status_class = "spoken"

    st.markdown(f"""
    <div class="agent-card {status_class}" style="--agent-color-light:rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.15)">
        <div class="agent-card-header">
            <div class="agent-card-emoji">{emoji}</div>
            <div class="agent-card-info">
                <div class="agent-card-name">{name}</div>
                <div class="agent-card-role">{role}</div>
            </div>
        </div>
        <div>
            <span class="agent-card-status {status_class}">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_insights_section(conversation_history: list):
    """Renders key insights extracted from the conversation."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="margin-top: 0; font-family: 'Syne', sans-serif;">Key Insights from the Boardroom</h3>
    </div>
    """, unsafe_allow_html=True)

    if not conversation_history:
        st.info("Start the debate to extract insights.")
        return

    # Count agent contributions
    agent_stats = {}
    for msg in conversation_history:
        if msg.get("speaker_type") == "agent":
            role = msg.get("role", "Unknown")
            agent_stats[role] = agent_stats.get(role, 0) + 1

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem;">
            👥 Agent Contributions
        </div>
        """, unsafe_allow_html=True)
        for role, count in sorted(agent_stats.items(), key=lambda x: x[1], reverse=True):
            agent = next((a for a in AGENTS if a["role"] == role), None)
            if agent:
                emoji = agent.get("emoji", "🤖")
                color = agent.get("color", "#6366f1")
                st.markdown(f"""
                <div class="insight-item">
                    <strong style="color:{color}">{emoji} {agent.get('name', role)}</strong><br/>
                    <span style="color: var(--text-muted);">{count} contribution{'s' if count != 1 else ''}</span>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem;">
            📊 Debate Statistics
        </div>
        """, unsafe_allow_html=True)

        total_turns = len(conversation_history)
        agent_turns = sum(1 for m in conversation_history if m.get("speaker_type") == "agent")
        user_turns = total_turns - agent_turns

        st.markdown(f"""
        <div class="insight-item">
            <strong>Total Turns:</strong> {total_turns}
        </div>
        <div class="insight-item">
            <strong style="color: var(--ceo);">Agent Responses:</strong> {agent_turns}
        </div>
        <div class="insight-item">
            <strong style="color: var(--gold);">Chairperson Inputs:</strong> {user_turns}
        </div>
        """, unsafe_allow_html=True)


def render_pitch_section(pitch: dict):
    """Renders the structured pitch deck."""
    if not pitch:
        st.info("Generate a pitch to see the deck here.")
        return

    company = pitch.get("startup_name", "Your Startup")
    tagline = pitch.get("startup_tagline", "")
    problem = pitch.get("problem", "")
    solution = pitch.get("solution", "")
    target = pitch.get("target_market", "")
    model = pitch.get("business_model", "")
    score = pitch.get("investor_score", "?/10")
    vision = pitch.get("vision", "")
    risks = pitch.get("key_risks", "")

    st.markdown(f"""
    <div class="pitch-hero">
        <div class="pitch-label">🏆 Investor Pitch Deck</div>
        <div class="pitch-title">{company}</div>
        <div class="pitch-tagline">"{tagline}"</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
        <div class="pitch-card">
            <span class="pitch-card-label">🔥 The Problem</span>
            <div class="pitch-card-content">{problem}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="pitch-card" style="margin-top: 1rem;">
            <span class="pitch-card-label">💡 The Solution</span>
            <div class="pitch-card-content">{solution}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="pitch-card">
            <span class="pitch-card-label">🎯 Target Market</span>
            <div class="pitch-card-content">{target}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="pitch-card" style="margin-top: 1rem;">
            <span class="pitch-card-label">💵 Business Model</span>
            <div class="pitch-card-content">{model}</div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2, gap="large")

    with col3:
        st.markdown(f"""
        <div class="pitch-card">
            <span class="pitch-card-label">🚀 Vision</span>
            <div class="pitch-card-content">{vision}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="pitch-card">
            <span class="pitch-card-label">⚠️ Key Risks</span>
            <div class="pitch-card-content">{risks}</div>
        </div>
        """, unsafe_allow_html=True)

    # Investor score at the bottom
    st.markdown(f"""
    <div style="text-align: center; margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, rgba(167,139,250,0.1), rgba(99,102,241,0.08)); border: 1px solid rgba(167,139,250,0.2); border-radius: var(--radius-lg);">
        <div style="font-family: 'DM Mono', monospace; font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Final Investor Score</div>
        <div style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: var(--investor);">🏦 {score}</div>
    </div>
    """, unsafe_allow_html=True)
