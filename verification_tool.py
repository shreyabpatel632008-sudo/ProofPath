
import json
import os
import re
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def lookup_verification_guidance(query: str) -> dict[str, Any]:
    """Retrieve curated verification guidance from S3."""

    bucket = os.getenv("PROOFPATH_GUIDANCE_BUCKET")
    key = os.getenv(
        "PROOFPATH_GUIDANCE_KEY",
        "verification-guidance.json",
    )

    if not bucket:
        return {
            "status": "not_configured",
            "message": (
                "Storage is not configured. Verify the claim "
                "through an independent official source."
            ),
            "matches": [],
        }

    if not isinstance(query, str) or not query.strip():
        return {
            "status": "no_match",
            "message": (
                "Please provide a topic or keywords to search. "
                "Verify independently before taking action."
            ),
            "matches": [],
        }

    try:
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=bucket, Key=key)

        with response["Body"] as body:
            records = json.loads(body.read().decode("utf-8"))

        if not isinstance(records, list):
            return {
                "status": "invalid_data",
                "message": "Guidance data must be a JSON list.",
                "matches": [],
            }

        # Normalize the query into whole words.
        stop_words = {
            "a", "an", "the", "and", "or", "for", "to",
            "of", "in", "on", "with", "is", "my", "me",
            "about", "please", "check", "verify",
        }

        terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        terms -= stop_words

        if not terms:
            return {
                "status": "no_match",
                "message": (
                    "Please provide more specific keywords. "
                    "Verify independently before taking action."
                ),
                "matches": [],
            }

        matches = []

        for record in records:
            if not isinstance(record, dict):
                continue

            # Match against names and keywords, not the guidance
            # text or URL, to reduce unrelated results.
            searchable = " ".join(
                str(record.get(field, ""))
                for field in ("name", "keywords")
            ).lower()

            searchable_terms = set(
                re.findall(r"[a-z0-9]+", searchable)
            )

            overlap = terms & searchable_terms

            if overlap:
                # Rank records by the number of matching query words.
                matches.append((len(overlap), record))

        # Most relevant matches first.
        matches.sort(key=lambda item: item[0], reverse=True)
        matched_records = [record for _, record in matches[:5]]

        if not matched_records:
            return {
                "status": "no_match",
                "message": (
                    "No matching record was found. This does not "
                    "mean the message is safe. Verify independently."
                ),
                "matches": [],
            }

        return {
            "status": "match_found",
            "message": (
                "These records may help with verification but do "
                "not prove that a message is genuine."
            ),
            "matches": matched_records,
        }


    except (
        BotoCoreError,
        ClientError,
        ValueError,
        KeyError,
        UnicodeDecodeError,
    ) as exc:
        if isinstance(exc, ClientError):
            error_code = exc.response.get("Error", {}).get("Code", "Unknown")
            print(f"Guidance lookup failed: ClientError ({error_code})")
        else:
            print(f"Guidance lookup failed: {type(exc).__name__}")

        return {
            "status": "lookup_unavailable",
            "message": (
                "Guidance is unavailable. Verify through an "
                "official source before taking action."
            ),
            "matches": [],
        }

