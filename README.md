# Autonomous Office AI Agent Workflow Engine (Local Sandbox)

An enterprise-grade, multi-tool autonomous AI Agent backend orchestrated using **n8n** and exposed via an interactive **Streamlit** user interface. The agent intelligently parses natural language strings into validated CRUD commands for office tool suites.

## 🛠️ Tech Stack & Integration Ecosystem
- **Orchestration Hub:** n8n (Advanced LLM Agent Node running Mistral Cloud)
- **Front-End Interface:** Streamlit (Python / Chat Element Session States)
- **Connected API Tooling Suite:** Google Calendar, Google Sheets, Google Tasks, Gmail, Google Docs, SerpApi

## 🧠 Core Engineering Challenges Solved
1. **Dynamic Parameter Normalization:** Engineered custom JavaScript formatting expressions inside the n8n node infrastructure (`$fromAI`) to clean input streams, apply whitespace optimization via `.trim()`, and map parameters precisely to strict Google API schemas.
2. **Context Window Optimization:** Resolved a critical 2.4-million token overflow condition (`Status 400 Context Length Error`) caused by massive unconstrained raw data reads from large Google Sheets datasets. Implemented structural query constraints, query filtering, and dataset pagination limits.
3. **Temporal Awareness Injection:** Stabilized downstream timezone and relative date calculation hallucinations (e.g., matching "yesterday" or "last Friday") by dynamically passing server-side datetime stamps (`{{ $now }}`) in standard `Asia/Kolkata` (IST) notation straight into the core prompt layout.
4. **Input Serialization Guardrails:** Configured raw data payload processing on the webhook ingestion layer to ensure that natural paragraph breaks and indentation styles passed from the web front end remain fully preserved across target platforms.

## 🔒 Security & Data Isolation Architecture
Because this system interfaces directly with private productivity infrastructure, the workflow executes natively as a secure developer backend sandbox. This isolates sensitive OAuth tokens and API access keys entirely within the server-side firewall, preventing credential exposure to the frontend client layer.
