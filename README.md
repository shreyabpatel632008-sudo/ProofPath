# ProofPath — Think. Verify. Stay Safe.

ProofPath is a student-focused digital safety assistant that helps users choose a cautious next step when they receive suspicious messages, scholarship offers, internship requests, prize claims, or requests for sensitive information.

## The Problem

Students may encounter messages that create urgency, request processing fees, ask for identity documents, or attempt to obtain OTPs and other sensitive information. Deciding what to do next can be difficult.

## Our Approach

ProofPath uses the local Strands Decider 2B model to select one of four actions:

- `VERIFY_SOURCE` — Check the offer through an independently verified official source.
- `ANALYZE_REQUEST` — Examine the message for suspicious requests and warning signs.
- `DRAFT_RESPONSE` — Prepare a cautious reply without exposing sensitive information.
- `ASK_HUMAN` — Seek help from a trusted person when appropriate.

The application displays the selected action, model confidence, option probabilities, and practical safety guidance.

## Reusable Strands Decider Decision Pattern

**Pattern name:** Confidence-Aware Safety Action Selection

**Question type:** `choice`

**Decision options:** `VERIFY_SOURCE`, `ANALYZE_REQUEST`, `DRAFT_RESPONSE`, `ASK_HUMAN`

**How it is wired into the agent path:** The message is passed as the decision state to the Strands Decider System One API. Its selected option and confidence are parsed by `decision.py`. The application then displays the corresponding safety guidance. A provisional confidence threshold flags decisions below `0.50` for additional review.

**When to use:** When an assistant must choose among a small, typed set of next actions and communicate uncertainty instead of presenting its recommendation as a guarantee.

The confidence score is the model's decision confidence, not the probability that a message is fraudulent. The review threshold is a prototype setting and has not been validated as a safety guarantee.

## Technology Stack

- Python
- Streamlit
- Strands Decider 2B
- HTTP API communication with the local Decider server

**Amazon Bedrock:** Integration is pending and is not claimed to be operational in this version.

## Run Locally

### Requirements

- Python 3.12
- A working installation of the Strands Decider CLI
- The Strands Decider 2B model downloaded locally

### 1. Install the Python dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install streamlit
```

Install and configure Strands Decider using its official documentation and ensure the model is available locally.

### 2. Start the Decider server

In one PowerShell window, run:

```powershell
strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8000
```

Keep this window open while using the application.

### 3. Start ProofPath

In a second PowerShell window, navigate to the project folder, activate the environment, and run:

```powershell
streamlit run app.py
```

Open the local URL displayed by Streamlit, normally `http://localhost:8501`.

## Project Files

- `app.py` — Streamlit user interface
- `decision.py` — Strands Decider API integration, decision parsing, and safety guidance
- `.gitignore` — Excludes local environments, caches, and sensitive configuration

## Limitations and Safety

ProofPath is an educational prototype, not a fraud detector, financial adviser, or official verification service. Its recommendations and confidence scores can be wrong. Independently verify important claims, avoid sharing OTPs or passwords, and consult a trusted person or the relevant institution when uncertain.

Do not enter real passwords, OTPs, banking information, or other sensitive personal data into the prototype.

## License

This project is licensed under the MIT License. See `LICENSE`.
