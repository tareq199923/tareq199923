# Hi, I'm Tareq 👋

**Full-stack developer · AI tooling builder · Researcher**
I build AI-powered products and ship them in public. Based in Bangladesh.

[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=flat-square&logo=vercel&logoColor=white)](https://tareq-tareq199923s-projects.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/md-jahidulislam199923/)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:jahidulislam199923@gmail.com)

> 🔎 **Open to work:** AI engineer · full-stack · AI tooling roles

---

## 🚀 Start Here

- 🔌 [**Invincible**](https://invincible-ai.me/): AI continuity gateway that survives rate limits, plus an MCP agent that runs on your own PC
- 📚 [**Book Dialogues**](https://book-dialogues.vercel.app): two books enter, one idea wins. Live AI debates between any two books

---

## 🛠️ What I'm Shipping

### [Invincible](https://invincible-ai.me/) — AI Continuity Gateway & Local MCP Agent

Free-tier LLM rate limits kept killing my coding agents mid-task. Invincible sits between your agent and your AI providers, **fails over to the next provider on a 429**, and lets cloud AI tools like Claude **act on your own PC** through MCP. Remote-first and multi-user, each account fully isolated.

**What's live:** OpenAI-compatible, Anthropic Messages and OpenAI Responses endpoints (Claude Code and Codex plug in with one config change), bring-your-own-key routing with automatic failover and cooldowns, MCP tool server (`read_file`, `execute_bash`, `write_file`) that runs on your paired machine with approval tokens, OAuth 2.1 + PKCE, shared memory and task continuity across models, web dashboard, per-user data isolation. Published on PyPI (0.6.x beta).

```bash
pip install -U invincible-ai
invincible connect      # browser opens → sign in → Approve

# Use it from Claude Code
export ANTHROPIC_BASE_URL=https://invincible-ai.me
export ANTHROPIC_AUTH_TOKEN=inv_...    # dashboard → Account → API keys
claude
```

Add `https://invincible-ai.me/mcp` as an MCP connector in Claude to let it work on your machine.

[![PyPI](https://img.shields.io/pypi/v/invincible-ai?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/invincible-ai/)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-121212?style=flat-square)
[![Repo](https://img.shields.io/badge/GitHub-invincible-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/tareq199923/invincible)

### [Book Dialogues](https://book-dialogues.vercel.app) — Two Books Enter. One Idea Wins.

Pick any two books and watch them argue. Book Dialogues pulls a "mind" out of each book (temperament, obsessions, argument style, voice) and stages a **live, persona-driven debate** with Google Gemini.

**What's live:** persona derivation from any book, live SSE streaming debates (intro, debate, reflection), editable debate topics, persona cache for instant revisits, magic-link login via Supabase Auth, bring-your-own Gemini key (stored only in your browser), export to Markdown or JSON, history viewer, persona gallery. Deployed on Vercel.

```bash
git clone https://github.com/tareq199923/book-dialogues
cd book-dialogues && npm install
cp .env.example .env.local     # add your Supabase keys
npm run dev
```

![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)
[![Repo](https://img.shields.io/badge/GitHub-book--dialogues-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/tareq199923/book-dialogues)

---

## 🔬 Research

| Paper | Venue | Status |
|---|---|---|
| Hybrid TF-IDF and Explainable Supervised Learning Approach for Detecting Fake Reviews | 5th IEEE SPICSCON 2026 | Accepted |

---

## 🧰 Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)

---

## 📊 GitHub Activity

![Contribution heatmap](./assets/heatmap.svg)

![GitHub stats](./assets/stats.svg)

![Top languages](./assets/langs.svg)

<sub>Refreshed daily by a GitHub Action. Languages exclude HTML, CSS, notebooks and TeX.</sub>

---

## 🎯 What I'm Doing

- **Building AI tooling:** gateways, agents, and tools that make LLMs practical
- **Shipping products:** small, real apps with live links
- **Researching:** explainable ML for text classification

## 💼 Background

- B.Sc. in Computer Science & Engineering, AIUB (2026)
- Web Developer at Join Venture AI (Jan to Jun 2026)
- Independent founder

---

## 🤝 Connect

[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=flat-square&logo=vercel&logoColor=white)](https://tareq-tareq199923s-projects.vercel.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/md-jahidulislam199923/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/tareq199923)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:jahidulislam199923@gmail.com)

---

> *Ship it, then make it better.*
