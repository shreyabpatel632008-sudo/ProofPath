import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict


# ============================================================
# ProofPath Configuration
# ============================================================

python
def get_setting(name, default=""):
    value = os.environ.get(name)

    if value:
        return value.strip()

    try:
        import streamlit as st
        value = st.secrets.get(name, default)
        return str(value).strip() if value else default
    except Exception:
        return default


API_URL = get_setting(
    "PROOFPATH_API_URL",
    "http://127.0.0.1:8000/v1/systemone",
)

API_TOKEN = get_setting("PROOFPATH_TOKEN", "")

REQUEST_TIMEOUT = 180
MAX_MESSAGE_LENGTH = 10_000
HUMAN_REVIEW_THRESHOLD = 0.50


# ============================================================
# Available Actions
# ============================================================

OPTIONS = {
    "VERIFY_SOURCE": (
        "Recommend checking the message against an official source."
    ),
    "ANALYZE_REQUEST": (
        "Examine the message for suspicious requests or warning signs."
    ),
    "DRAFT_RESPONSE": (
        "Help draft a cautious reply without sharing sensitive information."
    ),
    "ASK_HUMAN": (
        "Recommend getting help from a trusted person."
    ),
}


# ============================================================
# Safety Guidance
# ============================================================

GUIDANCE = {
    "VERIFY_SOURCE": [
        "Open the organization's official website independently.",
        "Contact the institution using verified contact details.",
        "Do not pay fees until the offer is independently verified.",
    ],
    "ANALYZE_REQUEST": [
        "Look for urgency, requests for money, unknown links, or sensitive information.",
        "Check the sender's address and the organization's official contact details.",
        "Never share OTPs, passwords, or identity documents through an unverified link.",
    ],
    "DRAFT_RESPONSE": [
        "Keep your reply brief and cautious.",
        "Do not include passwords, OTPs, payment details, or unnecessary personal information.",
        "Verify the sender before continuing the conversation.",
    ],
    "ASK_HUMAN": [
        "Pause before taking action.",
        "Ask a trusted person or the relevant institution to review the message.",
        "Avoid clicking unknown links or sending money while uncertain.",
    ],
}


# ============================================================
# Decision Data Model
# ============================================================

@dataclass
class ProofPathDecision:
    selected_action: str
    confidence: float
    probabilities: Dict[str, float]
    needs_review: bool


# ============================================================
# API Request
# ============================================================

def get_decision(message: str) -> ProofPathDecision:
    """Request a decision from the configured Strands Decider API."""

    message = message.strip()

    if not message:
        raise ValueError("The message cannot be empty.")

    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(
            f"Message is too long. Maximum length is "
            f"{MAX_MESSAGE_LENGTH} characters."
        )

    payload = {
        "state": message,
        "questions": {
            "choice_0": {
                "type": "choice",
                "instructions": (
                    "Choose the most appropriate next action for a digital "
                    "safety assistant. Prefer source verification or human "
                    "review when uncertain. Do not assume a message is safe "
                    "merely because it sounds convincing. Select exactly "
                    "one of the provided action options."
                ),
                "criteria": OPTIONS,
            }
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            response_body = response.read().decode("utf-8")

    except urllib.error.HTTPError as error:
        if error.code == 401:
            raise RuntimeError(
                "Authentication failed. Check the configured API token."
            ) from None

        if error.code == 404:
            raise RuntimeError(
                "The Decider API endpoint was not found. Check PROOFPATH_API_URL."
            ) from None

        raise RuntimeError(
            f"The Decider API returned HTTP {error.code}."
        ) from None

    except urllib.error.URLError as error:
        reason = str(error.reason)
        raise RuntimeError(
            "Could not connect to the Decider API. Check that the server "
            f"or protected gateway is running. Details: {reason}"
        ) from None

    except TimeoutError:
        raise RuntimeError(
            "The Decider API request timed out. Try again."
        ) from None

    try:
        data = json.loads(response_body)
        answer = data["answers"]["choice_0"]

        action = answer["choice"]
        confidence = float(answer["confidence"])
        raw_probabilities = answer["probabilities"]

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        raise RuntimeError(
            "The Decider API returned an unexpected response format."
        ) from None

    if action not in OPTIONS:
        raise RuntimeError(
            f"The Decider returned an unsupported action: {action!r}"
        )

    if not 0.0 <= confidence <= 1.0:
        raise RuntimeError(
            "The Decider returned an invalid confidence value."
        )

    if not isinstance(raw_probabilities, dict):
        raise RuntimeError(
            "The Decider returned invalid option probabilities."
        )

    probabilities = {}

    for key, value in raw_probabilities.items():
        try:
            probability = float(value)
        except (TypeError, ValueError):
            raise RuntimeError(
                "The Decider returned an invalid probability."
            ) from None

        if not 0.0 <= probability <= 1.0:
            raise RuntimeError(
                "The Decider returned a probability outside the valid range."
            )

        probabilities[str(key)] = probability

    return ProofPathDecision(
        selected_action=action,
        confidence=confidence,
        probabilities=probabilities,
        needs_review=confidence < HUMAN_REVIEW_THRESHOLD,
    )


# ============================================================
# Display Results
# ============================================================

def show_guidance(decision: ProofPathDecision) -> None:
    """Print the selected action, probabilities, and safety guidance."""

    print("\n=== ProofPath: Live Decider Result ===")
    print(f"Selected action: {decision.selected_action}")
    print(f"Meaning: {OPTIONS[decision.selected_action]}")
    print(f"Decider confidence: {decision.confidence:.4f}")
    print(f"Human review flag: {decision.needs_review}")

    print("\nOption probabilities:")

    for action, probability in sorted(
        decision.probabilities.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"  {action}: {probability:.4f}")

    print("\n=== Recommended Safety Steps ===")

    for number, step in enumerate(
        GUIDANCE[decision.selected_action],
        start=1,
    ):
        print(f"{number}. {step}")

    if decision.needs_review:
        print("\nCAUTION: The recommendation is uncertain.")
        print(
            "Seek human review before taking consequential action."
        )

    print(
        "\nSafety note: These recommendations are guidance, not proof "
        "that a message is genuine or fraudulent."
    )


# ============================================================
# Command-Line Entry Point
# ============================================================

def main() -> int:
    print("ProofPath — Digital Safety Decision Assistant")
    print(f"Configured API endpoint: {API_URL}")

    message = input(
        "\nEnter a message or situation to evaluate:\n> "
    ).strip()

    if not message:
        print("Please enter a message and try again.")
        return 1

    try:
        decision = get_decision(message)
        show_guidance(decision)
        return 0

    except (RuntimeError, ValueError) as error:
        print("\nProofPath could not get a decision.")
        print(f"Reason: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())