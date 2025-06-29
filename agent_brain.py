from llama_cpp import Llama
from db import save_complaint, check_complaint

llm = Llama(
    model_path="C:/Users/gourab/Desktop/gourab_jarvis/models/qwen2.5-coder-7b-instruct-q4_0.gguf",
    n_ctx=2048,
    n_threads=6,
    verbose=False
)

def local_chat(prompt):
    response = llm(
        f"<|system|>\nYou are a helpful electricity complaint assistant for Tripura.\n<|user|>\n{prompt}<|assistant|>",
        stop=["<|user|>"],
        temperature=0.7,
        top_p=0.95,
        max_tokens=512
    )
    return response["choices"][0]["text"].strip()

def get_response(user_input):
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
                return f"Complaint registered for power outage in {loc}. We’ll keep you updated."

    # Otherwise, ask the local model
    return local_chat(user_input)
