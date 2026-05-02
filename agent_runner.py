"""
agents/agent_runner.py
=======================
Handles calling the Groq API for individual agents
and orchestrating the full multi-agent simulation loop.
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from agent_definitions import AGENTS, build_system_prompt

# ── Groq model to use ─────────────────────────────────────────────────────────
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Fast & capable on Groq

# Load environment variables from local .env (if present).
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def get_groq_client() -> Groq:
    """
    Returns an authenticated Groq client.
    Checks st.session_state first (entered via sidebar), then env var.
    """
    api_key = st.session_state.get("groq_api_key") or os.environ.get("GROQ_API_KEY", "")
    api_key = api_key.strip().strip('"').strip("'")
    if not api_key:
        st.error("❌ No Groq API key found. Please enter it in the sidebar or set GROQ_API_KEY env variable.")
        st.stop()
    return Groq(api_key=api_key)


def build_messages_for_agent(
    agent: dict,
    idea: str,
    history: list,
    turn_num: int,
    direct_question: str = "",
) -> list:
    """
    Constructs the OpenAI-style messages list for a given agent.
    Includes the full conversation history as context.
    """
    system_prompt = build_system_prompt(agent, 3 if turn_num >= 10 else (2 if turn_num >= 5 else 1))

    # Build a readable transcript of prior conversation
    transcript_parts = []
    for msg in history:
        speaker_type = msg.get("speaker_type", "agent")
        if speaker_type == "user":
            transcript_parts.append(
                f"[Turn {msg.get('turn', '?')}] Chairperson: {msg['content']}"
            )
        else:
            transcript_parts.append(
                f"[Turn {msg.get('turn', '?')}] {msg.get('emoji', '')} {msg['agent']} ({msg['role']}): {msg['content']}"
            )
    transcript = "\n\n".join(transcript_parts) if transcript_parts else "No prior discussion."

    recent_context_instruction = ""
    if direct_question.strip():
        recent_context_instruction = (
            "You were directly asked this question by the Chairperson. "
            f"Answer it clearly before expanding your broader view: \"{direct_question.strip()}\""
        )
    elif history:
        last_msg = history[-1]
        # Ignore system messages like "Session started"
        if last_msg.get("role") != "Session":
            last_speaker = last_msg.get("agent", "Another agent")
            last_content = last_msg.get("content", "")
            if last_msg.get("speaker_type") == "user":
                recent_context_instruction = (
                    "IMPORTANT: The Chairperson just spoke. In your first sentence, explicitly "
                    f"acknowledge and react to this input: \"{last_content}\"."
                )
            else:
                recent_context_instruction = (
                    f"IMPORTANT: {last_speaker} just made a point. In your first sentence, "
                    f"explicitly acknowledge, agree, or push back on their statement: \"{last_content}\"."
                )

    user_content = f"""STARTUP IDEA: {idea}

PRIOR BOARDROOM DISCUSSION:
{transcript}

---
You are now speaking on Turn {turn_num}. Give your perspective as {agent['name']} ({agent['role']}).
React to what has been said. Be specific, opinionated, and direct.
{recent_context_instruction}"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]


def call_agent(
    agent: dict,
    idea: str,
    history: list,
    turn_num: int,
    direct_question: str = "",
) -> str:
    """
    Calls the Groq API for a single agent and returns their response text.
    """
    client = get_groq_client()
    messages = build_messages_for_agent(agent, idea, history, turn_num, direct_question)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.85,       # High enough for personality variation
            max_tokens=300,
            top_p=0.95,
        )
        content = response.choices[0].message.content or ""
        return content.strip()
    except Exception as e:
        return f"[Error generating response: {str(e)}]"


def run_simulation(idea: str) -> list:
    """
    Full simulation: 3 rounds × 5 agents = 15 messages.
    Returns the complete conversation list.
    NOTE: In the Streamlit app, this is called incrementally via session_state
    to enable streaming UX. This function is kept for non-streaming use.
    """
    conversation = []

    for round_num in range(1, 4):  # Legacy non-interactive mode
        for agent in AGENTS:
            response = call_agent(
                agent=agent,
                idea=idea,
                history=conversation,
                turn_num=len(conversation) + 1,
            )
            conversation.append({
                "agent": agent["name"],
                "role": agent["role"],
                "content": response,
                "round": round_num,
                "turn": len(conversation) + 1,
                "speaker_type": "agent",
                "color": agent["color"],
                "emoji": agent["emoji"],
            })

    return conversation
