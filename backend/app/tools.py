# app/tools.py

import re
import dateparser

from dateparser.search import (
    search_dates
)
from datetime import datetime

from app.services.groq_service import (
    generate_summary
)




# =========================
# DATE NORMALIZER
# =========================
def normalize_date(
    date_str,
    reference_datetime=None
):

    if not date_str:

        return None

    # =========================
    # BROWSER DATETIME
    # =========================

    if reference_datetime:

        reference_datetime = (

            datetime.fromisoformat(

                reference_datetime.replace(
                    "Z",
                    "+00:00"
                )

            )

        )

    else:

        reference_datetime = datetime.now()

    # =========================
    # PAST vs FUTURE
    # =========================

    future_keywords = [

        "after",
        "next",
        "tomorrow",
        "upcoming"

    ]

    prefer_direction = "past"

    if any(

        word in date_str.lower()

        for word in future_keywords

    ):

        prefer_direction = "future"

    # =========================
    # SEARCH DATE
    # =========================

    results = search_dates(

        date_str,

        languages=['en'],

        settings={

            "PREFER_DATES_FROM":
                prefer_direction,

            "RELATIVE_BASE":
                reference_datetime

        }

    )

    print(
        "REFERENCE DATETIME:",
        reference_datetime
    )

    print("RAW DATE:", date_str)

    print("SEARCH RESULTS:", results)

    if results:

        parsed_date = results[0][1]

        return parsed_date.strftime(
            "%Y-%m-%d"
        )

    return None

# =========================
# TIME NORMALIZER
# =========================

def normalize_time(time_str):

    if not time_str:

        return None

    parsed = dateparser.parse(
        time_str
    )

    if parsed:

        return parsed.strftime(
            "%H:%M"
        )

    return None


# =========================
# SAFE MERGE
# =========================

def safe_merge(
    new_value,
    old_value
):

    if (
        new_value is None or
        new_value == "" or
        str(new_value).lower() == "unknown"
    ):

        return old_value

    return new_value


# =========================
# TOOL 1
# LOG / EDIT INTERACTION
# =========================

def log_interaction_tool(
    user_input: str,
    existing_data=None,
    current_datetime=None
):

    if existing_data is None:

        existing_data = {}

    # =========================
    # REGEX DATE/TIME EXTRACTION
    # =========================

    date_match = re.search(

        r'(date\s*(is|was)?\s*)(.*)',

        user_input,

        re.IGNORECASE
    )

    time_match = re.search(

        r'(\d{1,2}:\d{2}\s?(AM|PM)?)',

        user_input,

        re.IGNORECASE
    )

    # =========================
    # LLM EXTRACTION
    # =========================

    extracted = generate_summary(

        user_input,

        existing_data
    )

    # =========================
    # FORCE DATE/TIME FROM REGEX
    # =========================

    if date_match:

        extracted["date"] = (
            date_match.group(3).strip()
        )

    if time_match:

        extracted["time"] = (
            time_match.group(1)
        )

    # =========================
    # NORMALIZATION
    # =========================

    normalized_date = normalize_date(

    extracted.get("date"),

    current_datetime

)

    normalized_time = normalize_time(

        extracted.get("time")
    )

    # =========================
    # HCP PROTECTION
    # =========================

    new_hcp = extracted.get(
        "hcp_name"
    )

    if (

        "dr" not in user_input.lower()

        and

        "doctor" not in user_input.lower()

    ):

        new_hcp = existing_data.get(
            "hcp_name"
        )

    # =========================
    # FINAL INTERACTION
    # =========================
    new_sentiment = extracted.get(
    "sentiment"
)

    new_sentiment = extracted.get(
    "sentiment"
)

    sentiment_keywords = [

        "interested",
        "happy",
        "positive",
        "negative",
        "concern",
        "issue",
        "angry",
        "excellent"

    ]

    if not any(

        word in user_input.lower()

        for word in sentiment_keywords

    ):

        new_sentiment = existing_data.get(
            "sentiment",
            "neutral"
        )





    interaction = {

        "hcp_name":

            safe_merge(

                new_hcp,

                existing_data.get(
                    "hcp_name"
                )

            ),

        "product":

            safe_merge(

                extracted.get(
                    "product"
                ),

                existing_data.get(
                    "product"
                )

            ),

        "sentiment":

            safe_merge(

                new_sentiment,
                existing_data.get(
                    "sentiment",
                    "neutral"
                )

            ),

        "summary":

            safe_merge(

                extracted.get(
                    "summary"
                ),

                existing_data.get(
                    "summary"
                )

            ),

        "follow_up_action":

            safe_merge(

                extracted.get(
                    "follow_up_action"
                ),

                existing_data.get(
                    "follow_up_action"
                )

            ),

        "date":

            safe_merge(

                normalized_date,

                existing_data.get(
                    "date"
                )

            ),

        "time":

            safe_merge(

                normalized_time,

                existing_data.get(
                    "time"
                )

            ),

        "follow_up_required":
            True
    }

    # =========================
    # REMOVE NONE VALUES
    # =========================

    interaction = {

        k: v

        for k, v in interaction.items()

        if v is not None

    }

    print("\nFINAL INTERACTION:\n")

    print(interaction)

    return interaction


# =========================
# TOOL 3
# COMPLIANCE VALIDATION
# =========================

def compliance_validation_tool(
    interaction
):

    summary = interaction.get(
        "summary",
        ""
    ).lower()

    risky_terms = [

        "cure",

        "guaranteed",

        "100% effective"

    ]

    violations = []

    for term in risky_terms:

        if term in summary:

            violations.append(term)

    if violations:

        return {

            "status": "warning",

            "violations": violations

        }

    return {

        "status": "approved",

        "violations": []

    }


# =========================
# TOOL 4
# FOLLOWUP SCHEDULER
# =========================

def followup_scheduler_tool(
    interaction
):

    if interaction.get(
        "follow_up_required"
    ):

        followup_task = interaction.get(
            "follow_up_action"
        )

        if not followup_task:

            followup_task = (
                "Schedule follow-up meeting"
            )

        return [

            {

                "task":
                    followup_task,

                "priority":
                    "high"

            }

        ]

    return []


# =========================
# TOOL 5
# HCP RECOMMENDATION TOOL
# =========================

def hcp_recommendation_tool(
    interaction
):

    recommendations = []

    sentiment = interaction.get(
        "sentiment"
    )

    if sentiment == "positive":

        recommendations.append(

            "Schedule another meeting within 2 weeks"

        )

        recommendations.append(

            "Share latest efficacy studies"

        )

    elif sentiment == "neutral":

        recommendations.append(

            "Send educational materials"

        )

    else:

        recommendations.append(

            "Escalate to senior sales manager"

        )

    return recommendations


def final_finaloutput_tool(interaction):
    result = {
        "final_output": {
            "interaction": interaction["interaction_data"],
            "compliance": interaction["compliance_result"],
            "recommendations": interaction["recommendations"],
            "followups": interaction["followup_tasks"]
        }
    }

    return result