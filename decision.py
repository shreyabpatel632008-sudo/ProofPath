
import re

OPTIONS = [
    "VERIFY_SOURCE",
    "DO_NOT_PROCEED",
    "SEEK_HELP",
    "PROCEED_WITH_CAUTION",
]

GUIDANCE = {
    "VERIFY_SOURCE": [
        "Verify the sender through an independently found official website or contact.",
        "Do not trust links or phone numbers supplied in the suspicious message.",
        "Do not share identity documents, passwords, OTPs, or bank details until verified.",
    ],
    "DO_NOT_PROCEED": [
        "Do not pay or share sensitive information.",
        "Do not click suspicious links or download unexpected attachments.",
        "Save the message as evidence and report it to the appropriate platform or authority.",
    ],
    "SEEK_HELP": [
        "Pause before taking action.",
        "Ask a trusted person or the relevant official support team for help.",
        "Do not share sensitive information until the situation is clarified.",
    ],
    "PROCEED_WITH_CAUTION": [
        "Check the sender and details independently.",
        "Read the terms before agreeing or sharing information.",
        "Stop if you notice pressure, unusual requests, or inconsistent details.",
    ],
}


def get_setting(name, default=""):
    """Read an optional setting from the environment or Streamlit secrets."""
    import os

    value = os.environ.get(name)
    if value:
        return value.strip()

    try:
        import streamlit as st
        value = st.secrets.get(name, default)
        return str(value).strip() if value else default
    except Exception:
        return default


def analyze_situation(message):
    """Analyze common safety warning signs using local rules."""
    text = (message or "").strip().lower()

    if not text:
        raise ValueError("Please describe the situation before analyzing it.")


    payment_terms = [
        "pay", "payment", "processing fee", "registration fee",
        "application fee", "transfer money", "send money",
        "gift card", "cryptocurrency", "crypto", "release fee",
    ]

    identity_terms = [
        "identity documents", "identity proof", "id documents",
        "passport", "aadhaar", "aadhar", "unknown link",
        "upload my documents", "send my documents",
        "personal documents", "sensitive information",
    ]

    pressure_terms = [
        "immediately", "immediate", "urgent", "right now",
        "act now", "within minutes", "final warning",
        "award can be released", "offer expires",
        "account will be blocked", "will be blocked",
    ]

    credential_terms = [
        "otp", "one-time password", "password",
        "bank details", "card number", "pin number",
        "share your credentials",
    ]

    prize_terms = [
        "you won a prize", "claim your prize",
        "lottery winner", "free reward", "you have won",
    ]

    payment_risk = any(term in text for term in payment_terms)
    identity_risk = any(term in text for term in identity_terms)
    pressure_risk = any(term in text for term in pressure_terms)
    credential_risk = any(term in text for term in credential_terms)
    prize_risk = any(term in text for term in prize_terms)

    # Record individual warning signs for the explanation.
    reasons = []
    if payment_risk:
        reasons.append("The message mentions a payment or fee.")
    if identity_risk:
        reasons.append("The message mentions identity documents or an unfamiliar link.")
    if pressure_risk:
        reasons.append("The message uses urgency or threatens a consequence.")
    if credential_risk:
        reasons.append("The message mentions passwords, OTPs, or financial credentials.")
    if prize_risk:
        reasons.append("The message makes a prize or reward claim.")

    if credential_risk:
        action = "DO_NOT_PROCEED"
        confidence = 0.90

    elif payment_risk and pressure_risk:
        action = "DO_NOT_PROCEED"
        confidence = 0.88

    elif prize_risk and (payment_risk or pressure_risk):
        action = "DO_NOT_PROCEED"
        confidence = 0.86

    elif identity_risk:
        action = "VERIFY_SOURCE"
        confidence = 0.82

    elif payment_risk:
        action = "VERIFY_SOURCE"
        confidence = 0.78

    elif pressure_risk or prize_risk:
        action = "SEEK_HELP"
        confidence = 0.72

    else:
        action = "PROCEED_WITH_CAUTION"
        confidence = 0.60
        reasons.append(
            "No listed warning pattern was detected; this does not prove the situation is safe."
        )

    meanings = {
        "VERIFY_SOURCE": (
            "Verify the sender, offer, or request using an independently "
            "located official source before proceeding."
        ),
        "DO_NOT_PROCEED": (
            "Pause. Do not send money or disclose sensitive information "
            "until the risk is resolved."
        ),
        "SEEK_HELP": (
            "Pause and seek independent guidance before taking action."
        ),
        "PROCEED_WITH_CAUTION": (
            "Review the details carefully and verify important claims "
            "before proceeding."
        ),
    }

    return {
        "selected_action": action,
        "action": action,
        "meaning": meanings[action],
        "confidence": confidence,
        "probabilities": {
            action: confidence,
        },
        "human_review": True,
        "guidance": GUIDANCE[action],
        "reasons": reasons,
        "analysis_mode": "Rule-based safety checks (not live AI)",
    }


def get_decision(message):
    """Return a decision for the ProofPath interface."""
    return analyze_situation(message)


def show_guidance(result):
    """Return the recommended next steps."""
    return result.get("guidance", [])


def main():
    print("ProofPath - Safety Situation Analyzer")
    print("This version uses local rules, not live AI.")

    message = input("\nDescribe the situation: ").strip()

    try:
        result = get_decision(message)

        print("\n=== ProofPath Result ===")
        print("Recommended action:", result["selected_action"])
        print("Meaning:", result["meaning"])
        print("Confidence:", result["confidence"])
        print("Human review recommended:", result["human_review"])
        print("Analysis mode:", result["analysis_mode"])

        print("\nWarning signs:")
        for reason in result["reasons"]:
            print("-", reason)

        print("\nRecommended next steps:")
        for step in result["guidance"]:
            print("-", step)

        print(
            "\nNote: This is a basic rule-based assessment, "
            "not a guarantee that a message is safe or fraudulent."
        )

    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()

