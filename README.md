# 🛡️ ProofPath — Think. Verify. Stay Safe.

**A confidence-aware digital safety assistant for students.**

ProofPath helps students make safer decisions when they encounter suspicious scholarship offers, internship requests, prize claims, payment demands, or messages asking for sensitive information.

🔗 **Live Demo:** https://proofpath-shreya.streamlit.app/  
💻 **GitHub Repository:** https://github.com/shreyabpatel632008-sudo/ProofPath

---

## 🚨 The Problem

Students frequently encounter online messages that may:

- Promise scholarships, internships, or rewards to create excitement.
- Demand unexpected registration or processing fees.
- Request OTPs, passwords, banking information, or identity documents.
- Use urgency or pressure to discourage independent verification.

Recognizing warning signs is important, but knowing what to do next can be equally challenging.

## 💡 Our Solution

ProofPath combines rule-based safety analysis with reusable verification guidance to help users decide on a cautious next step.

The application identifies common warning signs, provides practical safety recommendations, and uses **SourceCheck** to retrieve relevant guidance from an AWS S3-backed knowledge source.

### Key Features

- **Scholarship safety:** Guidance for checking scholarship offers and unexpected fees.
- **Internship safety:** Suggestions for independently verifying recruiters and employers.
- **Prize and reward safety:** Reminders to verify organizers and avoid suspicious payment requests.
- **OTP and account safety:** Guidance against sharing OTPs, passwords, and recovery codes.
- **SourceCheck:** Retrieves relevant verification guidance from an S3-hosted JSON knowledge base.
- **Privacy-conscious design:** Reminds users not to enter passwords, OTPs, banking details, or other sensitive personal information.

## ☁️ AWS Integration

ProofPath uses Amazon S3 to store and retrieve reusable verification guidance.

**How SourceCheck works:**

1. A user submits a message for analysis.
2. ProofPath identifies relevant warning signs and the type of request.
3. SourceCheck looks for matching guidance in the configured S3 knowledge base.
4. The application displays relevant guidance and recommends cautious next steps.

The S3 bucket is configured for private access. The application uses environment-based configuration and AWS credentials rather than embedding credentials in source code.

**Important:** A matching guidance record helps users find verification steps; it does not prove that a message, website, recruiter, or offer is genuine.

## 🧠 Decision-Making Approach

### Current deployed demo

The public Streamlit demo uses **rule-based safety analysis** and AWS S3-backed SourceCheck guidance. Live Strands Decider inference is not currently connected to the deployed demo.

### Strands Decider development pattern

ProofPath also explores a reusable decision pattern called **Confidence-Aware Safety Action Selection**.

- **Question type:** `choice`
- **Decision options:** `VERIFY_SOURCE`, `ANALYZE_REQUEST`, `DRAFT_RESPONSE`, `ASK_HUMAN`
- **Review threshold:** `0.50` (provisional prototype setting)

The intended development workflow uses Strands Decider to select an action, parses the returned decision and confidence, and presents relevant safety guidance.

The confidence score represents the model's confidence in its selected action. It is not the probability that a message is fraudulent, and the review threshold has not been validated as a safety guarantee.

**Amazon Bedrock integration is planned and is not claimed to be operational in this version.**

## 🛠️ Technology Stack

- **Python** — Application logic
- **Streamlit** — Interactive web interface
- **Amazon S3** — Private storage for verification guidance
- **Boto3** — AWS SDK for Python
- **Strands Decider 2B** — Experimental local decision-making development path
- **HTTP API** — Communication with the optional local Decider service

## 🚀 Run Locally

### Prerequisites

- Python 3.12
- Git
- AWS credentials with appropriate permissions if you want to use S3-backed SourceCheck
- Strands Decider CLI and its local model only if you want to experiment with the separate Decider development path

### 1. Clone the repository

```bash
git clone https://github.com/shreyabpatel632008-sudo/ProofPath.git
cd ProofPath
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure AWS access (optional)

For S3-backed SourceCheck, configure AWS credentials using a secure method supported by Boto3, such as an AWS CLI profile or environment variables.

Set the following application configuration values as appropriate for your environment:

- `PROOFPATH_GUIDANCE_BUCKET`
- `PROOFPATH_GUIDANCE_KEY`
- `AWS_DEFAULT_REGION`

Use the private bucket and the correct object key for your deployment. Grant only the permissions required to read the guidance object.

**Never commit AWS access keys, API tokens, `.env` files, or Streamlit secrets to GitHub.**

### 5. Start ProofPath

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal, usually:

`http://localhost:8501`

### Optional: Start the local Strands Decider development service

If you have installed and configured the Strands Decider CLI and downloaded the model:

```powershell
strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8000
```

This optional service is part of the experimental local development workflow; it is not required to describe or use the current deployed rule-based demo. Follow the project's actual API and gateway configuration if enabling the separate integration.

## 📁 Project Structure

```text
ProofPath/
├── app.py
├── decision.py
├── verification_tool.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

- `app.py` — Streamlit application and user interface
- `decision.py` — Decision parsing, analysis logic, and safety guidance
- `verification_tool.py` — SourceCheck guidance retrieval
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes local environments and sensitive configuration

## ⚠️ Limitations and Safety

ProofPath is an educational prototype, not a certified fraud detector, financial adviser, or official verification service.

- Rule-based analysis may miss threats or flag legitimate messages.
- Guidance matches do not establish authenticity.
- Model confidence, where applicable, is not a calibrated fraud probability.
- S3 guidance may be unavailable if AWS access or configuration fails.
- Live Strands Decider inference and Amazon Bedrock are not active in the current deployed demo.

Always verify important claims independently through official websites or trusted contact channels. Never share OTPs or passwords, and consult a trusted person or the relevant institution when uncertain.

Do not submit real passwords, OTPs, banking details, or sensitive identity information to the prototype.

## 🔮 Future Improvements

- Integrate and validate live Strands Decider inference in the deployed application.
- Explore Amazon Bedrock integration.
- Expand the verification guidance knowledge base.
- Add more testing for false positives, false negatives, and uncertain cases.
- Improve accessibility, usability, and security testing.

## 📜 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

**ProofPath — Think. Verify. Stay Safe.**

*Helping students pause, verify, and make safer digital decisions.*

