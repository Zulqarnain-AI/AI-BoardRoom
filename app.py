"""
🧠 AI Boardroom
===============
Premium Interactive Boardroom for Startup Pitching
User acts as Chairperson controlling 5 AI executive agents.

Layout:
  [Board Members] | [Live Session] | [Chairperson Controls]
  [Bottom: Insights & Pitch Tabs]
"""
import sys
import os

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st  # type: ignore
import re
import time
import random
from agent_definitions import AGENTS
from agent_runner import call_agent
from pitch_generator import generate_pitch, generate_business_plan
from ui_helpers import (
    inject_custom_css,
    render_chat_bubble,
    render_agent_card,
    render_insights_section,
    render_pitch_section,
    play_agent_audio,
    stream_chat_bubble_with_audio,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🧠 AI Boardroom",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_custom_css()

# ── Session state init ────────────────────────────────────────────────────────
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "pitch" not in st.session_state:
    st.session_state.pitch = None
if "current_idea" not in st.session_state:
    st.session_state.current_idea = ""
if "debate_finished" not in st.session_state:
    st.session_state.debate_finished = False
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "business_plan" not in st.session_state:
    st.session_state.business_plan = ""
if "audio_enabled" not in st.session_state:
    st.session_state.audio_enabled = False
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None
if "last_response" not in st.session_state:
    st.session_state.last_response = ""
if "last_role" not in st.session_state:
    st.session_state.last_role = ""
if "scores" not in st.session_state:
    st.session_state.scores = {
        "market": 5,
        "tech": 5,
        "finance": 5,
        "growth": 5,
        "investor": 5
    }


def _next_turn() -> int:
    return len(st.session_state.conversation_history) + 1


def _find_agent_by_mention(text: str):
    match = re.search(r"@\s*(ceo|cto|cfo|cmo|investor)\b", text or "", flags=re.IGNORECASE)
    if not match:
        return None
    mention_role = match.group(1).upper()
    for a in AGENTS:
        if a["role"].upper() == mention_role:
            return a
    return None


def _get_agent_status(agent_role: str) -> str:
    """Determine if agent is currently speaking, has spoken, or idle."""
    if st.session_state.conversation_history:
        # Check if agent spoke in last message
        last_msg = st.session_state.conversation_history[-1]
        if last_msg.get("speaker_type") == "agent" and last_msg.get("role") == agent_role:
            return "speaking"
        # Check if agent has spoken before
        for msg in st.session_state.conversation_history:
            if msg.get("speaker_type") == "agent" and msg.get("role") == agent_role:
                return "spoken"
    return "idle"


# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header header-brand">
        🧠 AI BOARDROOM
    </div>
    """,
    unsafe_allow_html=True,
)


# ── MAIN LAYOUT: 3-COLUMN STRUCTURE ────────────────────────────────────────────
if st.session_state.current_idea:
    # Main boardroom layout
    col_left, col_center, col_right = st.columns([1, 2, 1], gap="large")

    # ────────────────────────────────────────────────────────────────────────────
    # LEFT COLUMN: BOARD MEMBERS
    # ────────────────────────────────────────────────────────────────────────────
    with col_left:
        st.markdown('<div class="panel-title">👥 BOARD MEMBERS</div>', unsafe_allow_html=True)

        for agent in AGENTS:
            status = _get_agent_status(agent["role"])
            render_agent_card(agent, status)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gamification Scores
        st.markdown('<div class="section-label">📊 Board Confidence</div>', unsafe_allow_html=True)
        st.progress(st.session_state.scores["market"] / 10.0, text="👔 Market (CEO)")
        st.progress(st.session_state.scores["tech"] / 10.0, text="⚙️ Tech (CTO)")
        st.progress(st.session_state.scores["finance"] / 10.0, text="💰 Finance (CFO)")
        st.progress(st.session_state.scores["growth"] / 10.0, text="📣 Growth (CMO)")
        st.progress(st.session_state.scores["investor"] / 10.0, text="🏦 Investor (VC)")


    # ────────────────────────────────────────────────────────────────────────────
    # CENTER COLUMN: LIVE SESSION / CHAT
    # ────────────────────────────────────────────────────────────────────────────
    with col_center:
        st.markdown(
            '<div class="panel-title">💬 LIVE BOARDROOM SESSION</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.conversation_history:
            st.markdown(
                '<div class="empty-session">No conversation yet. Start by asking a question or summoning an agent.</div>',
                unsafe_allow_html=True,
            )
        else:
            # ── DISPLAY LAST MESSAGE PROMINENTLY ──────────────────────────────
            last_msg = st.session_state.conversation_history[-1]
            st.markdown(
                '<div class="current-message-label">📍 CURRENT RESPONSE</div>',
                unsafe_allow_html=True,
            ) 
            
            if last_msg.get("speaker_type") == "user":
                render_chat_bubble(
                    speaker=last_msg.get("agent", "Chairperson"),
                    role="Chairperson",
                    content=last_msg.get("content", ""),
                    is_user=True,
                )
            else:
                if st.session_state.pending_audio and last_msg.get("role") == st.session_state.pending_audio["role"] and last_msg.get("content") == st.session_state.pending_audio["text"]:
                    audio_data = st.session_state.pending_audio
                    st.session_state.pending_audio = None
                    stream_chat_bubble_with_audio(
                        speaker=last_msg.get("agent", "Agent"),
                        role=last_msg.get("role", "Unknown"),
                        content=last_msg.get("content", ""),
                        agent_color=last_msg.get("color", "#6366f1"),
                        emoji=last_msg.get("emoji", ""),
                    )
                else:
                    render_chat_bubble(
                        speaker=last_msg.get("agent", "Agent"),
                        role=last_msg.get("role", "Unknown"),
                        content=last_msg.get("content", ""),
                        is_user=False,
                        agent_color=last_msg.get("color", "#6366f1"),
                        emoji=last_msg.get("emoji", ""),
                    )
            
            
            # ── TOGGLE HISTORY BUTTON ──────────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            col_hist_btn, col_hist_count = st.columns([1, 1])
            with col_hist_btn:
                if st.button(
                    f"{'📖 Hide' if st.session_state.show_history else '📖 Show'} Conversation History",
                    use_container_width=True,
                    key="toggle_history_btn",
                ):
                    st.session_state.show_history = not st.session_state.show_history
                    st.rerun()
            
            with col_hist_count:
                history_count = len(st.session_state.conversation_history) - 1
                st.markdown(
                    f'<div style="text-align: right; color: var(--text-muted); font-size: 0.85rem; padding-top: 0.6rem;">{history_count} previous message{"s" if history_count != 1 else ""}</div>',
                    unsafe_allow_html=True,
                )
            
            # ── SHOW FULL HISTORY IF EXPANDED ──────────────────────────────────
            if st.session_state.show_history:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    '<div class="history-divider"></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="history-label">📜 Full Conversation</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="chat-stream">', unsafe_allow_html=True)
                
                for msg in st.session_state.conversation_history:
                    if msg.get("speaker_type") == "user":
                        render_chat_bubble(
                            speaker=msg.get("agent", "Chairperson"),
                            role="Chairperson",
                            content=msg.get("content", ""),
                            is_user=True,
                        )
                    else:
                        render_chat_bubble(
                            speaker=msg.get("agent", "Agent"),
                            role=msg.get("role", "Unknown"),
                            content=msg.get("content", ""),
                            is_user=False,
                            agent_color=msg.get("color", "#6366f1"),
                            emoji=msg.get("emoji", ""),
                        )
                
                st.markdown('</div>', unsafe_allow_html=True)

        # Final outcome
        if st.session_state.debate_finished:
            inv_score = st.session_state.scores.get("investor", 5)
            if inv_score >= 7:
                outcome = "✅ FUNDED! The board believes in your vision."
                color = "#10b981"
            elif inv_score >= 4:
                outcome = "⚠️ NEEDS IMPROVEMENT. The board is skeptical."
                color = "#f59e0b"
            else:
                outcome = "❌ REJECTED. The board passed on this idea."
                color = "#ef4444"
                
            st.markdown(f'''
            <div style="background-color: {color}15; border: 1px solid {color}50; padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 1.5rem;">
                <h3 style="color: {color}; margin: 0; font-family: 'Syne', sans-serif;">{outcome}</h3>
                <p style="color: var(--text-muted); margin-top: 0.5rem; margin-bottom: 0;">Final Investor Score: <strong>{inv_score}/10</strong></p>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Audio is now handled inline by stream_chat_bubble_with_audio

    # ────────────────────────────────────────────────────────────────────────────
    # RIGHT COLUMN: CHAIRPERSON CONTROLS
    # ────────────────────────────────────────────────────────────────────────────
    with col_right:
        st.markdown(
            '<div class="panel-title">⚙️ YOUR CONTROLS</div>',
            unsafe_allow_html=True,
        )

        # Audio Mode & Replay
        st.session_state.audio_enabled = st.toggle("🎙️ Audio Mode", value=st.session_state.audio_enabled)
        if st.button("🎙️ Replay Last Response", disabled=not st.session_state.last_response):
            st.session_state.pending_audio = {
                "text": st.session_state.last_response,
                "role": st.session_state.last_role
            }
            st.rerun()


        # Session info
        
        # Quick action buttons
        st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2, gap="small")
        with col_btn1:
            if st.button("▶️ Start Session", use_container_width=True, key="start_btn"):
                # If session not started yet, initialize session state and add a visible session-start message
                if not st.session_state.get("session_started", False):
                    st.session_state.session_started = True
                    # Append a visible system/user message so the center panel shows the session started
                    st.session_state.conversation_history.append({
                        "speaker_type": "user",
                        "agent": "System",
                        "role": "Session",
                        "content": "📢 Boardroom session started by Chairperson.",
                        "turn": _next_turn(),
                    })
                    # Ensure the current response is shown
                    st.session_state.show_history = False
                    try:
                        st.toast("📢 Boardroom session started!", icon="✨")
                    except Exception:
                        st.success("📢 Boardroom session started!")
                    st.rerun()
                else:
                    # Provide feedback if already started
                    st.info("Boardroom session is already running.")

        with col_btn2:
            if st.button("🔄 Reset", use_container_width=True, key="reset_btn"):
                st.session_state.conversation_history = []
                st.session_state.pitch = None
                st.session_state.business_plan = ""
                st.session_state.debate_finished = False
                st.session_state.session_started = False
                st.toast("🔄 Debate reset", icon="🔄")
                st.rerun()

        # Agent summoning
        st.markdown(
            '<div class="section-label">Summon an Agent</div>',
            unsafe_allow_html=True,
        )
        selected_role = st.selectbox(
            "Choose agent",
            options=[a["role"] for a in AGENTS],
            format_func=lambda role: next(
                a["emoji"] + " " + a["name"] for a in AGENTS if a["role"] == role
            ),
            key="agent_select",
        )

        direct_q = st.text_input(
            "Direct question (optional)",
            placeholder="Ask something specific...",
            key="direct_q_input",
        )

        if st.button("🎙️ SUMMON AGENT", use_container_width=True, type="primary", key="summon_btn"):
            target_agent = next(a for a in AGENTS if a["role"] == selected_role)
            mentioned = _find_agent_by_mention(direct_q.strip())
            if mentioned:
                target_agent = mentioned

            with st.spinner(f"💭 {target_agent['name']} is thinking…"):
                time.sleep(random.uniform(0.5, 1.5))
                response = call_agent(
                    agent=target_agent,
                    idea=st.session_state.current_idea,
                    history=st.session_state.conversation_history,
                    turn_num=_next_turn(),
                    direct_question=direct_q.strip(),
                )

            st.session_state.conversation_history.append({
                "speaker_type": "agent",
                "agent": target_agent["name"],
                "role": target_agent["role"],
                "content": response,
                "turn": _next_turn(),
                "color": target_agent["color"],
                "emoji": target_agent["emoji"],
            })
            
            # Gamification update
            mapping = {"CEO": "market", "CTO": "tech", "CFO": "finance", "CMO": "growth", "Investor": "investor"}
            score_key = mapping.get(target_agent["role"])
            if score_key:
                st.session_state.scores[score_key] = min(10, st.session_state.scores[score_key] + 1)
                
            st.session_state.last_response = response
            st.session_state.last_role = target_agent["role"]
            
            if st.session_state.audio_enabled:
                st.session_state.pending_audio = {"text": response, "role": target_agent["role"]}
                
            st.toast(f"🎙️ {target_agent['name']} has spoken!", icon="✨")
            st.rerun()


        # Chairperson speak
        st.markdown(
            '<div class="section-label">Your Comment</div>',
            unsafe_allow_html=True,
        )

        chairperson_msg = st.text_area(
            "Your message to the board",
            placeholder="Share guidance, challenge ideas...",
            height=100,
            label_visibility="collapsed",
            key="chair_msg",
        )

        if st.button("💬 SPEAK", use_container_width=True, key="speak_btn"):
            if chairperson_msg.strip():
                st.session_state.conversation_history.append({
                    "speaker_type": "user",
                    "agent": "You (Chairperson)",
                    "role": "Chairperson",
                    "content": chairperson_msg.strip(),
                    "turn": _next_turn(),
                })
                st.toast("✅ Your comment added to the board!", icon="💬")
                st.rerun()
            else:
                st.warning("Please type a message first.")


        # Debate controls
        st.markdown(
            '<div class="section-label">Debate Control</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.debate_finished:
            if st.button("✅ FINISH DEBATE", use_container_width=True, key="finish_btn"):
                st.session_state.debate_finished = True
                st.toast("🏁 Debate closed! Ready to generate pitch.", icon="✨")
                st.rerun()
        else:
            if st.button("↩️ REOPEN DEBATE", use_container_width=True, key="reopen_btn"):
                st.session_state.debate_finished = False
                st.toast("🔄 Debate reopened", icon="🔄")
                st.rerun()

        if st.session_state.debate_finished:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎯 GENERATE PITCH", use_container_width=True, type="primary", key="pitch_btn"):
                with st.spinner("✍️ Crafting your investor pitch…"):
                    pitch_data = generate_pitch(
                        idea=st.session_state.current_idea,
                        conversation=st.session_state.conversation_history,
                    )
                st.session_state.pitch = pitch_data
                st.session_state.business_plan = ""
                st.toast("🎯 Pitch generated!", icon="✨")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ────────────────────────────────────────────────────────────────────────────
    # HERO STATE: NO IDEA YET
    # ────────────────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-icon">🎯</div>
            <h1 class="hero-title">Welcome to the AI Boardroom</h1>
            <p class="hero-subtitle">
                Pitch your startup idea to a panel of expert AI executives.
            </p>
            <p class="hero-description">
                 .
            </p>
            <div class="agent-badges">
                <span class="badge ceo">👔 CEO (Strategy)</span>
                <span class="badge cto">⚙️ CTO (Tech)</span>
                <span class="badge cfo">💰 CFO (Finance)</span>
                <span class="badge cmo">📣 CMO (Marketing)</span>
                <span class="badge investor">🏦 Investor (VC)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">Step 1: Pitch Your Idea</div>',
        unsafe_allow_html=True,
    )

    col_input, col_btn = st.columns([5, 1], gap="medium")
    with col_input:
        idea_input = st.text_area(
            "startup_idea",
            placeholder='Describe your startup idea… e.g., "An AI-powered legal assistant for small businesses"',
            height=100,
            label_visibility="collapsed",
            key="idea_input_main",
        )

    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        start_btn = st.button(
            "⚡ START\nBOARDROOM",
            use_container_width=True,
            type="primary",
            key="start_boardroom_btn",
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if start_btn:
        if idea_input.strip():
            st.session_state.conversation_history = []
            st.session_state.pitch = None
            st.session_state.business_plan = ""
            st.session_state.debate_finished = False
            st.session_state.current_idea = idea_input.strip()
            st.session_state.session_started = True
            st.session_state.session_round = 1
            st.toast("🎉 Boardroom initialized! Welcome, Chairperson.", icon="✨")
            st.rerun()
        else:
            st.error("Please enter a startup idea first.")

# ── BOTTOM SECTION: INSIGHTS & PITCH ───────────────────────────────────────────
if st.session_state.current_idea and st.session_state.conversation_history:
    st.divider()

    tab_insights, tab_pitch = st.tabs(["📊 INSIGHTS", "🎯 PITCH DECK"])

    with tab_insights:
        render_insights_section(st.session_state.conversation_history)

    with tab_pitch:
        if st.session_state.pitch:
            render_pitch_section(st.session_state.pitch)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Business Plan")
            st.caption("Generate a board-ready business plan and download it as a Markdown document.")

            col_plan_generate, col_plan_download = st.columns([1, 1], gap="small")

            with col_plan_generate:
                if st.button("🧾 Generate Business Plan", use_container_width=True, key="generate_plan_btn"):
                    with st.spinner("Building a professional business plan…"):
                        plan_md = generate_business_plan(
                            idea=st.session_state.current_idea,
                            pitch=st.session_state.pitch,
                            conversation=st.session_state.conversation_history,
                        )
                    st.session_state.business_plan = plan_md
                    st.toast("🧾 Business plan generated", icon="✅")
                    st.rerun()

            with col_plan_download:
                if st.session_state.business_plan:
                    st.download_button(
                        label="⬇️ Download Business Plan",
                        data=st.session_state.business_plan,
                        file_name="business_plan.md",
                        mime="text/markdown",
                        use_container_width=True,
                        key="download_plan_btn",
                    )
                else:
                    st.button(
                        "⬇️ Download Business Plan",
                        use_container_width=True,
                        disabled=True,
                        key="download_plan_btn_disabled",
                    )

            if st.session_state.business_plan:
                with st.expander("Preview Business Plan", expanded=False):
                    st.markdown(st.session_state.business_plan)
        else:
            st.info(
                "💡 Finish the debate and click 'GENERATE PITCH' in the controls panel to create your pitch deck."
            )

# ── SIDEBAR: Configuration ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_…",
        help="Get your free key at console.groq.com",
    )
    if api_key:
        st.session_state["groq_api_key"] = api_key
        st.success("✅ API key saved")

    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown(
        """
**AI Boardroom** is an interactive multi-agent simulation where you control the conversation.

**Your Role:** Chairperson  
Steer the debate, ask targeted questions, and synthesize insights.

**The Panel:**
- 👔 **CEO** — Market vision & strategy
- ⚙️ **CTO** — Technical feasibility  
- 💰 **CFO** — Unit economics & risk
- 📣 **CMO** — Growth & positioning
- 🏦 **Investor** — Final verdict

**Workflow:**
1. Pitch your idea
2. Summon agents or speak as chairperson
3. Close debate when satisfied
4. Generate investor pitch

Built with Streamlit + Groq API.
    """
    )

    if st.session_state.current_idea:
        st.markdown("---")
        if st.button("🔄 Start Over", use_container_width=True):
            for key in ["conversation_history", "pitch", "business_plan", "debate_finished", "current_idea"]:
                if key == "conversation_history":
                    st.session_state[key] = []
                elif key in ("pitch",):
                    st.session_state[key] = None
                elif key == "business_plan":
                    st.session_state[key] = ""
                elif key == "debate_finished":
                    st.session_state[key] = False
                else:
                    st.session_state[key] = ""
            st.rerun()