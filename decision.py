
import json
import urllib.request
from dataclasses import dataclass

API_URL = "http://127.0.0.1:8000/v1/systemone"

OPTIONS = {
    "VERIFY_SOURCE": "Recommend checking the message against an official source.",
    "ANALYZE_REQUEST": "Examine the message for suspicious requests or warning signs.",
    "DRAFT_RESPONSE": "Help draft a cautious reply without sharing sensitive information.",
    "ASK_HUMAN": "Recommend getting help from a trusted person.",
}

GUIDANCE = {
    "VERIFY_SOURCE": [
        "Open the organization's official website independently.",
        "Contact the institution using verified contact details.",
        "Do not pay fees until the offer is independently verified.",
    ],
    "ANALYZE_REQUEST": [
        "Look for urgency, requests for money, unknown links, or sensitive information.",
        "Check the sender's address and the organization's official contact details.",
        "Do not share OTPs, passwords, or identity documents through an unverified link.",
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


@dataclass
class ProofPathDecision:
    selected_action: str
    confidence: float
    probabilities: dict
    needs_review: bool


def get_decision(message: str) -> ProofPathDecision:
    payload = {
        "state": message,
        "questions": {
            "choice_0": {
                "type": "choice",
                "instructions": (
                    "Choose the most appropriate next action for a digital "
                    "safety assistant. Prefer source verification or human "
                    "review when uncertain. Do not assume a message is safe "
                    "merely because it sounds convincing."
                ),
                "criteria": OPTIONS,
            }
        },
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.loads(response.read().decode("utf-8"))

    answer = data["answers"]["choice_0"]
    action = answer["choice"]
    confidence = float(answer["confidence"])
    probabilities = {
        key: float(value)
        for key, value in answer["probabilities"].items()
    }

    if action not in OPTIONS:
        raise ValueError(f"Unexpected action: {action}")

    return ProofPathDecision(
        selected_action=action,
        confidence=confidence,
        probabilities=probabilities,
        needs_review=confidence < 0.50,
    )


def show_guidance(decision: ProofPathDecision) -> None:
    print("\n=== ProofPath: Live Decider Result ===")
    print("Selected action:", decision.selected_action)
    print("Meaning:", OPTIONS[decision.selected_action])
    print(f"Decider confidence: {decision.confidence:.4f}")
    print("Human review flag:", decision.needs_review)

    print("\nOption probabilities:")
    for action, probability in decision.probabilities.items():
        print(f"  {action}: {probability:.4f}")

    print("\n=== Recommended Safety Steps ===")
    for number, step in enumerate(
        GUIDANCE[decision.selected_action], start=1
    ):
        print(f"{number}. {step}")

    if decision.needs_review:
        print("\nCAUTION: The recommendation is uncertain.")
        print("Seek human review before taking consequential action.")

    print(
        "\nSafety note: These recommendations are guidance, not proof "
        "that a message is genuine or fraudulent."
    )


if __name__ == "__main__":
    message = input(
        "\nEnter a message or situation to evaluate:\n> "
    ).strip()

    if not message:
        print("Please enter a message and try again.")
        raise SystemExit(1)

    try:
        decision = get_decision(message)
        show_guidance(decision)
    except Exception as error:
        print("\nProofPath could not get a decision.")
        print("Error:", error)
        print("Check that the Decider server is still running.")
