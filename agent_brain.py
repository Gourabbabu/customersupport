import os
from openai import OpenAI
from dotenv import load_dotenv
from db import save_complaint, check_complaint

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def get_response(user_input, site_url=None, site_title=None):
    # Filter irrelevant queries
    irrelevant_keywords = ["weather", "movie", "sports", "news"]
    if any(word in user_input.lower() for word in irrelevant_keywords):
        return "I'm here to help you with electricity-related problems. This topic is irrelevant."

    # Check existing complaint
    for loc in ["indranagar", "krishna nagar", "banamalipur"]:
        if loc in user_input.lower() and ("status" in user_input.lower() or "when" in user_input.lower()):
            complaints = check_complaint(loc)
            if complaints:
                return f"A team is already working in {loc}. Estimated time to restore power: 2 hours."
            else:
                return "No complaints registered yet for your area. Would you like to report one?"

    # Save new complaint if keywords match
    if "no electricity" in user_input.lower() or "power cut" in user_input.lower():
        for loc in ["indranagar", "krishna nagar", "banamalipur"]:
            if loc in user_input.lower():
                save_complaint(loc, "Power Outage")
                return f"Complaint registered for power outage in {loc}. We'll keep you updated."

    # Otherwise, use OpenRouter API
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": site_url or "http://localhost", # Optional
            "X-Title": site_title or "CustomerSupportAI", # Optional
        },
        extra_body={},
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return completion.choices[0].message.content.strip()
