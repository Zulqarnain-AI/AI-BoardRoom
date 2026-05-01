---
title: Multi-Agent Startup Simulator
emoji: 🚀
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: "1.35.0"
app_file: app.py
pinned: false
license: mit
short_description: AI boardroom of 5 agents debate your startup idea and generate a pitch
---

# 🚀 Multi-Agent Startup Simulator + Pitch Generator

Simulate a real startup boardroom: 5 distinct AI agents debate your idea across 3 rounds, then synthesize a polished investor pitch.

## Agents

| Agent | Role | Personality |
|-------|------|-------------|
| 👔 Sarah Chen | CEO | Visionary, optimistic, big-picture |
| ⚙️ Marcus Webb | CTO | Technical, realistic, feasibility-focused |
| 💰 Diana Okafor | CFO | Skeptical, risk-focused, cost-aware |
| 📣 Jake Rivera | CMO | Marketing-obsessed, user-centric |
| 🏦 Victoria Stone | Investor | Final evaluator — gives a score out of 10 |

## Features

- 3 debate rounds x 5 agents = 15 unique AI responses
- Each agent sees the full conversation history
- Conflict is encouraged — agents push back on each other
- Generates a structured 9-section investor pitch
- Dark luxury boardroom UI with smooth animations

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/startup-simulator
cd startup-simulator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Groq API key

Option A — environment variable:
```bash
export GROQ_API_KEY=gsk_your_key_here
```

Option B — enter it in the sidebar when the app is running.

Get a free Groq key at: https://console.groq.com

### 4. Run locally

```bash
streamlit run app.py
```

The app opens at http://localhost:8501

---

## Deploy to Hugging Face Spaces

### Method 1: Web UI upload

1. Go to https://huggingface.co/new-space
2. Set SDK to Streamlit
3. Upload all files preserving the directory structure
4. Go to Settings → Repository secrets → add GROQ_API_KEY

### Method 2: Git push

```bash
pip install huggingface_hub
huggingface-cli login
huggingface-cli repo create startup-simulator --type space --space-sdk streamlit

git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/startup-simulator
git push hf main
```

After pushing, add secret GROQ_API_KEY in Space Settings.

---

## Project Structure

```
startup-simulator/
├── app.py                       # Main Streamlit entry point
├── requirements.txt             # Dependencies
├── README.md                    # This file (HF Spaces config header)
├── agents/
│   ├── __init__.py
│   ├── agent_definitions.py     # Agent personalities and system prompts
│   ├── agent_runner.py          # Groq API calls and simulation loop
│   └── pitch_generator.py      # Structured pitch generation
└── utils/
    ├── __init__.py
    └── ui_helpers.py            # CSS, HTML rendering, UI components
```

---

## Environment Variables

| Variable     | Required | Description                          |
|-------------|----------|--------------------------------------|
| GROQ_API_KEY | Yes      | Your key from console.groq.com       |

---

## Example Startup Ideas

- "An AI legal assistant that helps small businesses draft contracts for $49/month"
- "A subscription box for Gen Z curated by TikTok creators"
- "B2B SaaS that detects employee burnout from Zoom calls using computer vision"
- "Peer-to-peer platform for renting unused garage space as storage units"

---

## License

MIT
