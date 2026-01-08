# Bhasha.ai — AI Tone Corrector

[![Project Status: Prototype](https://img.shields.io/badge/status-prototype-yellow?style=for-the-badge)]()
[![Tech: Python + Flask](https://img.shields.io/badge/backend-python%20%2B%20flask-blue?style=for-the-badge)]()
[![Frontend: HTML/CSS](https://img.shields.io/badge/frontend-html%20%2B%20css-lightgrey?style=for-the-badge)]()

One-line: Bhasha.ai is an AI-powered tone detection and correction platform that analyzes emotional tone and rewrites messages to be professional, friendly, and context-appropriate — for email, realtime chat, and meeting replies.

Demo: (Add demo video link here)  
Screenshots: (Add product photos here)

---

## Table of contents
- [Why Bhasha.ai?](#why-bhashaai)
- [Features](#features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [API: Endpoints & Examples](#api-endpoints--examples)
- [Installation & Local Setup](#installation--local-setup)
- [Deployment & Hosting](#deployment--hosting)
- [Integration Designs](#integration-designs)
- [Pricing & Business Model](#pricing--business-model)
- [Security & Privacy](#security--privacy)
- [Contributing & Code Quality](#contributing--code-quality)
- [Roadmap](#roadmap)
- [Contact & Attribution](#contact--attribution)

---

## Why Bhasha.ai?
- Helps professionals convert rough or emotionally-charged text into polite, professional, and friendly communication.
- Useful for email composition, real-time messaging, meeting reply suggestions, and as an API to integrate tone-aware rewriting in other apps (Slack, Teams, Chrome extension).
- Focus on brevity, clarity, and measurable improvement in message tone.

---

## Features
- Tone detection / emotional analysis (e.g., angry, sad, neutral, joyful)
- Tone-aware rewrite suggestions: professional, friendly, calm, persuasive, concise
- Email writer endpoint to convert raw text into a business email
- Realtime chat / messaging-ready responses and meeting reply suggestions
- Multi-language input handling (detects language, translates to English, processes, returns improved text)
- Usage tracking and simple plan enforcement (FREE/PRO usage limits)
- History log of processed items per user
- Ready-to-extend API for integrations and frontend demo

---

## Architecture & Tech Stack
- Frontend: Plain HTML, CSS for prototype (can be migrated to React/Next.js)
- Backend: Python + Flask (REST API)
- Models: Hugging Face pipelines (text-classification for emotions, text2text-generation for rewriting)
- Database: SQLite for prototype (switch to Postgres for production)
- Optional: translator via googletrans for language detection/translation
- Development: VS Code recommended
- Packaging: Use poetry or provide requirements.txt

Provided prototype code uses:
- endpoints: /login, /email, /tone, /meeting, /history/<user_id>
- SQLite schema with tables: users, plans, history

---

## API — Endpoints & Examples

Note: All endpoints expect JSON and return JSON.

1) POST /login
- Purpose: create or log in a user (simple prototype auth)
- Request:
  {
    "email": "user@example.com",
    "password": "mypassword"
  }
- Response:
  {
    "user_id": 1
  }

2) POST /email
- Purpose: Convert text into a professional email
- Request:
  {
    "user_id": 1,
    "text": "Hey, we messed up the delivery and need to apologize..."
  }
- Response:
  {
    "result": "Dear X,\n\nI am writing to apologize..."
  }

3) POST /tone
- Purpose: Detect emotional tone and return a friendly professional rewrite
- Request:
  {
    "user_id": 1,
    "text": "I am really upset about the delay!"
  }
- Response:
  {
    "emotion": "anger",
    "improved_text": "I'm sorry to hear about the delay. Could you please provide more details so we can resolve this quickly?"
  }

4) POST /meeting
- Purpose: Send transcribed meeting text and get suggested replies
- Request:
  {
    "user_id": 1,
    "text": "The client is frustrated with the timeline..."
  }
- Response:
  {
    "detected_emotion": "anger",
    "suggested_reply": "I understand your concerns. Here's a plan to improve the timeline..."
  }

5) GET /history/<user_id>
- Purpose: Get user processing history
- Response:
  [
    {
      "type": "TONE",
      "emotion": "anger",
      "suggestion": "...",
      "time": "2025-12-31 12:00:00"
    },
    ...
  ]

Curl example:
curl -X POST http://localhost:5000/tone -H "Content-Type: application/json" -d '{"user_id":1,"text":"I am disappointed"}'

Important extension notes:
- For realtime chat, replace REST with WebSocket (Socket.IO) or add an event-driven layer.
- For production auth, swap the simple user table for token-based auth (JWT/OAuth) and hashed passwords (bcrypt).

---

## Installation & Local Setup

Option A — Using pip + requirements.txt (quick):
1. Clone repo:
   git clone https://github.com/<your-username>/bhasha.ai.git
2. Navigate:
   cd bhasha.ai
3. Create venv:
   python -m venv .venv
   source .venv/bin/activate  # mac/linux
   .venv\Scripts\activate     # windows
4. Install:
   pip install -r requirements.txt
   (requirements should include flask, flask-cors, transformers, langdetect, googletrans==4.0.0-rc1, torch or accelerate as needed)
5. Run:
   python app.py
6. Visit http://localhost:5000

Option B — Using Poetry (recommended for Python projects):
1. Install poetry: https://python-poetry.org/docs/
2. poetry install
3. poetry run python app.py

Environment variables (add to .env):
- FLASK_ENV=development
- SECRET_KEY=your_secret_key
- HF_AUTH_TOKEN=your_huggingface_token (if using private models or to avoid rate limits)
- DATABASE_URL (for production Postgres)

Files to include in repo:
- requirements.txt or pyproject.toml + poetry.lock
- .env.example
- README.md (this file)
- LICENSE
- Dockerfile
- .github/workflows/ci.yml (optional CI)

---

## Deployment & Hosting
Prototype hosting recommendations:
- Backend: Railway, Render, Fly.io, or AWS Elastic Beanstalk / ECS / GCP Cloud Run
- Frontend (static HTML/CSS): Vercel, Netlify, GitHub Pages
- For demos, containerize with Docker and push to registry. Example Dockerfile provided in repo.
- Use GitHub Actions for CI: run lint, tests, build container image, and deploy.

Scaling/production changes:
- Replace SQLite with Postgres
- Use a model-serving layer (Triton, Hugging Face Inference Endpoints, Replicate, or a fine-tuned model served on GPU)
- Add rate-limiting, request queueing, batching of model requests
- Use Redis for caching & background jobs (RQ/Celery)

---

## Integration Designs

Slack
- Slash command /bhasha or message action
- Workflow: user selects text -> request to Bhasha API -> return suggestion -> post as ephemeral message or replace text
- OAuth app + granular scopes (chat:write, commands)

Microsoft Teams
- Bot-based integration using Bot Framework
- Adaptive cards for suggestions and one-click post

Chrome Extension
- Content script detects textareas -> context menu "Rewrite with Bhasha" -> popup to show suggestions -> replace selected text
- Auth via OAuth + token stored in extension (secure storage recommended)

Realtime Chat App
- Use WebSocket endpoint for low-latency rewrites
- Frontend shows tone label in-line and "Use suggestion" button

---

## Pricing & Business Model (Suggested)
Goal: Convert free users into paid users while providing API access for teams.

Tier ideas:
- Free: $0 — 5 rewrites/day, basic email and tone features, community support
- Pro: $9/mo — 100 rewrites/day, priority model throughput, email templates, Web UI features
- Team: $49/mo — shared team seats (5 users), team analytics, shared history, SSO
- Enterprise: Custom — SLA, on-premise options, dedicated model hosting, higher throughput

Alternative API model:
- Monthly subscription + pay-as-you-go credits for heavy API usage (e.g., $0.002 per rewrite after quota)
- Volume discounts for high-usage customers

Monetization channels:
- Direct subscriptions (Stripe)
- API marketplace (RapidAPI, Hugging Face Marketplace)
- White-label / licensing to enterprise
- Chrome extension with freemium features

Metrics to track:
- Conversion rate (Free -> Pro)
- Active users / DAU
- Average rewrites per user per month
- Revenue per user

---

## Security & Privacy
- Store passwords hashed (bcrypt) — do not store plaintext passwords (prototype currently stores plaintext; change this before production)
- Offer data retention controls (delete user history)
- Use HTTPS, secure cookies, and secure storage for tokens
- For GDPR: provide data export and delete endpoints
- Clarify model data usage in privacy policy (do not send PII to third-party inference services without consent)

---

## Contributing & Code Quality
- Use black / isort / flake8 for Python formatting & linting
- Write unit tests for endpoints (pytest + test client)
- Add type hints (mypy) where possible
- Keep commit history clean and include PR templates
- Provide CONTRIBUTING.md with branching, testing, and PR review guidelines

Code review checklist (for companies):
- Proper dependency file (requirements.txt or poetry)
- No secrets in source
- Passwords hashed, secure auth used
- Tests included and passing
- Clear README with setup + docs

---

## Roadmap & Ideas
- Improve emotion taxonomy and support fine-grained tone suggestions
- Add user-editable tone presets (e.g., "concise", "empathetic", "assertive")
- Add analytics dashboard for teams (tone trends, response time)
- Deploy dedicated inference endpoints (GPU-backed)
- Mobile app + SDKs for iOS/Android
- Browser plugin and native integrations (Gmail, Outlook)

---

## Demo Video & Screenshots
Add a short 60–90s demo video showing:
1. Entering raw text (email / chat)
2. Tone detection and label
3. Suggested improved text and "Apply" action
4. Slack/Chrome extension flow (if implemented)

Place the demo link and one or two screenshots in the repo root:
- demo/video.mp4 (or YouTube link)
- assets/screenshot-1.png
- assets/screenshot-2.png

---

## Example: Minimal Dockerfile
(Place Dockerfile in repo root)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=2", "--timeout=120"]
```

---

## Contact & Attribution
Project: Bhasha.ai — AI Tone Corrector  
Prototype author: (Add your name)  
Repo: https://github.com/<your-username>/bhasha.ai

---
