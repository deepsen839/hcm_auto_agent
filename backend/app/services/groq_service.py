from groq import Groq
import re
import os
import json

from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_summary(
    notes: str,
    existing_data=None
):

    if existing_data is None:

        existing_data = {}

    prompt = f"""
You are an AI pharmaceutical CRM assistant.

Your task is to extract and update structured CRM interaction data.

Previous CRM Interaction:

{json.dumps(existing_data, indent=2)}

User Update:

{notes}

TASK:
Update ONLY the fields mentioned by the user.

Preserve existing values if they are not changed.

Return ONLY valid JSON.

Format:

{{
 
  "hcp_name": "",
  "product": "",
  "sentiment": "",
  "summary": "",
  "follow_up_action": "",
  "date": "",
  "time": ""

}}

Interpretation Rules:

- If the message mentions "Dr" or a doctor/person name:
  update hcp_name

- If the message mentions medicine/drug/product names:
  update product

- Short edits like:
  "it is blood pressure"
  "product is X"
  "medicine was Y"
  should update ONLY the product field

- Do NOT treat product names as doctor names

- Preserve previous values unless explicitly changed

- Do NOT hallucinate new doctors or products

- sentiment must be:
  positive / neutral / negative

- Return JSON only
- No markdown
- No explanation

Examples:

Previous:
{{
  "hcp_name": "Dr. Sharma",
  "product": "GlucoX"
}}

User:
"it is blood pressure"

Output:
{{
  "hcp_name": "Dr. Sharma",
  "product": "Blood Pressure"
}}

---

Previous:
{{
  "hcp_name": "Dr. Sharma",
  "product": "GlucoX"
}}

User:
"Actually it was Dr John"

Output:
{{
  "hcp_name": "Dr. John",
  "product": "GlucoX"
}}

---

User:
"the date is last saturday"

Output:
{{
  "date": "last saturday"
}}

---

User:
"the time is 12:38 PM"

Output:
{{
  "time": "12:38 PM"
}}

---

User:
"the meeting was last monday at 3:45 PM"

Output:
{{
  "date": "last monday",
  "time": "3:45 PM"
}}

---

User:
"Doctor claimed the medicine is a guaranteed cure"

Output:
{{
  "sentiment": "negative"
}}

"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content":
                "You are an AI CRM assistant."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0,

        response_format={
            "type": "json_object"
        }

    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    print("\nLLM RESPONSE:\n")
    print(content)

    return json.loads(content)