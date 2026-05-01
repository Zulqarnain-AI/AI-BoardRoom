"""
agents/pitch_generator.py
==========================
After the simulation completes, this module calls the Groq API
with the full conversation to synthesize a structured investor pitch.
"""

import json
import re
import streamlit as st
from groq import Groq
from agent_runner import get_groq_client, MODEL


PITCH_SYSTEM_PROMPT = """You are an expert startup pitch writer and venture capital advisor.
Your job is to synthesize a boardroom discussion into a polished, structured investor pitch.

You MUST respond with ONLY a valid JSON object — no markdown fences, no preamble, no extra text.

The JSON must have exactly these keys:
{
  "startup_name": "A creative, memorable startup name",
  "tagline": "One punchy sentence tagline under 12 words",
  "problem": "2-3 sentences describing the core problem being solved",
  "solution": "2-3 sentences describing the product/service solution",
  "target_market": "2 sentences on TAM and primary customer segment",
  "business_model": "2 sentences on how money is made (pricing, model type)",
    "vision": "2-3 sentences describing long-term strategic vision and future state",
  "key_features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
  "competitive_advantage": "2-3 sentences on moat and differentiation",
  "elevator_pitch": "A compelling 4-5 sentence pitch you'd give to a partner at Sequoia in an elevator",
  "investor_score": "X/10",
    "critical_risk": "The single most critical risk identified in the discussion",
    "key_risks": "2-3 sentences with the top execution and market risks"
}
"""


BUSINESS_PLAN_SYSTEM_PROMPT = """You are an expert management consultant and startup operator.
Create a professional, board-ready business plan in clean markdown.

Return ONLY markdown. No code fences.
Use these sections in this exact order:
1. Executive Summary
2. Company Overview
3. Problem Statement
4. Solution & Product
5. Market Analysis
6. Business Model
7. Go-To-Market Strategy
8. Operations Plan
9. Financial Snapshot
10. Risk Management
11. Milestones (12 Months)
12. Funding Ask & Use of Funds

Requirements:
- Keep it specific, practical, and investor-grade.
- Use short paragraphs and concise bullet points where useful.
- Include realistic assumptions and measurable goals.
"""


def generate_pitch(idea: str, conversation: list) -> dict:
    """
    Calls the Groq API to generate a structured investor pitch
    based on the startup idea and full agent conversation.
    Returns a parsed dict.
    """
    client = get_groq_client()
    raw = ""

    # Build conversation summary for context
    transcript_parts = []
    for msg in conversation:
        speaker_type = msg.get("speaker_type", "agent")
        if speaker_type == "user":
            transcript_parts.append(
                f"Chairperson (Turn {msg.get('turn', '?')}): {msg['content']}"
            )
        else:
            transcript_parts.append(
                f"{msg['agent']} ({msg['role']}, Turn {msg.get('turn', '?')}): {msg['content']}"
            )
    transcript = "\n\n".join(transcript_parts)

    user_content = f"""ORIGINAL STARTUP IDEA:
{idea}

FULL BOARDROOM DISCUSSION:
{transcript}

---
Based on the above, generate a complete structured investor pitch JSON as instructed."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PITCH_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.6,
            max_tokens=1200,
        )

        raw = (response.choices[0].message.content or "").strip()

        # Strip markdown fences if model added them anyway
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        pitch = json.loads(raw)
        return pitch

    except json.JSONDecodeError as e:
        # Fallback: return raw text wrapped in a dict so UI can still display something
        return {
            "startup_name": "Unnamed Startup",
            "tagline": "Pitch generation encountered a formatting error.",
            "problem": raw if raw else "Unknown error",
            "solution": "",
            "target_market": "",
            "business_model": "",
            "key_features": [],
            "competitive_advantage": "",
            "elevator_pitch": "",
            "investor_score": "N/A",
            "critical_risk": str(e),
        }
    except Exception as e:
        st.error(f"Pitch generation error: {e}")
        return {}


def generate_business_plan(idea: str, pitch: dict, conversation: list) -> str:
    """Generate a professional markdown business plan from idea, pitch, and board discussion."""
    client = get_groq_client()
    raw = ""

    transcript_parts = []
    for msg in conversation:
        speaker_type = msg.get("speaker_type", "agent")
        if speaker_type == "user":
            transcript_parts.append(
                f"Chairperson (Turn {msg.get('turn', '?')}): {msg.get('content', '')}"
            )
        else:
            transcript_parts.append(
                f"{msg.get('agent', 'Agent')} ({msg.get('role', 'Unknown')}, Turn {msg.get('turn', '?')}): {msg.get('content', '')}"
            )
    transcript = "\n\n".join(transcript_parts) if transcript_parts else "No discussion transcript provided."

    pitch_json = json.dumps(pitch or {}, indent=2)
    user_content = f"""STARTUP IDEA:
{idea}

PITCH JSON:
{pitch_json}

BOARDROOM DISCUSSION:
{transcript}

Create a complete business plan as instructed."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": BUSINESS_PLAN_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.5,
            max_tokens=2200,
        )

        raw = (response.choices[0].message.content or "").strip()
        raw = re.sub(r"^```(?:markdown|md)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        return raw

    except Exception as e:
        st.error(f"Business plan generation error: {e}")
        # Fallback simple markdown so users can still download something useful
        startup_name = (pitch or {}).get("startup_name", "Startup")
        tagline = (pitch or {}).get("tagline", "")
        return (
            f"# {startup_name} Business Plan\n\n"
            f"## Executive Summary\n{tagline}\n\n"
            f"## Company Overview\n{idea}\n\n"
            "## Problem Statement\nTBD\n\n"
            "## Solution & Product\nTBD\n\n"
            "## Market Analysis\nTBD\n\n"
            "## Business Model\nTBD\n\n"
            "## Go-To-Market Strategy\nTBD\n\n"
            "## Operations Plan\nTBD\n\n"
            "## Financial Snapshot\nTBD\n\n"
            "## Risk Management\nTBD\n\n"
            "## Milestones (12 Months)\nTBD\n\n"
            "## Funding Ask & Use of Funds\nTBD\n"
        )
