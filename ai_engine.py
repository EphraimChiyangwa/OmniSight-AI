import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

MOCK_AI_MODE = False
DEFAULT_MODEL = None

if not api_key:
    MOCK_AI_MODE = True
    print("⚠️ No API key found. Running in MOCK AI MODE.")
else:
    try:
        genai.configure(api_key=api_key)
        models = list(genai.list_models())
        for m in models:
            if "generateContent" in getattr(m, "supported_generation_methods", []):
                DEFAULT_MODEL = m.name
                break
        if not DEFAULT_MODEL:
            MOCK_AI_MODE = True
    except Exception as e:
        MOCK_AI_MODE = True
        print(f"⚠️ Gemini unavailable: {e}")

if MOCK_AI_MODE:
    print("🟡 OmniSight AI running in MOCK DEMO MODE")
else:
    print(f"✅ OmniSight AI using model: {DEFAULT_MODEL}")

BASE_PERSONA = """
You are OmniSight AI. 
Tone: Executive, Direct, and Ultra-concise.
Constraint: Use plain English. No corporate jargon. Max 3-4 bullet points.
""".strip()

def _mock_executive_response():
    return """
### 🚨 EXECUTIVE ALERT
Revenue declined 8% in the last 24 hours, triggering an immediate risk to short-term margins.

### 🔎 KEY INSIGHT (Cross-Domain)
A competitor price reduction increased client churn in Region Y, which lowered partner referral quality and raised acquisition costs.

### ⛓️ CAUSAL CHAIN
**Competitor pricing pressure** → **Higher churn + weaker referrals** → **Revenue and margin decline**

### 🎯 RECOMMENDED ACTIONS (Next 48h)
1) Adjust partner incentives in Region Y — Partner Team — Stabilize referral quality  
2) Launch retention offers for high-risk clients — Client Success — Reduce churn  
3) Review regional pricing — Finance — Protect margins

### 📌 CONFIDENCE
Overall: Medium  
Reason: Competitive data is strong; client elasticity requires further validation
"""

def analyze_state(state_data):
    if MOCK_AI_MODE:
        return _mock_executive_response()

    system_prompt = f"""{BASE_PERSONA}
TASK:
- Identify the single most critical cross-domain issue.
- Link at least 3 domains.
- Be concise and actionable.
"""

    try:
        model = genai.GenerativeModel(
            model_name=DEFAULT_MODEL,
            system_instruction=system_prompt,
        )
        response = model.generate_content(
            f"DATA:\n{json.dumps(state_data, ensure_ascii=False)}"
        )
        return response.text
    except Exception as e:
        return _mock_executive_response()

def ask_ai_question(question, state_data):
    if MOCK_AI_MODE:
        return (
            "**Main Reason:** Competitive pricing combined with supplier quality issues.\n\n"
            "* **Supplier Issue:** P002 quality dropped by 12%.\n"
            "* **Market Pressure:** Competitor A cut prices by 15%.\n"
            "* **High Risk:** Major client C003 is likely to churn."
        )

    try:
        model = genai.GenerativeModel(
            model_name=DEFAULT_MODEL,
            system_instruction=BASE_PERSONA,
        )
        
        simplified_prompt = f"""
        Answer this question using the data provided: "{question}"
        
        Rules:
        1. Start with a single sentence "Root Cause".
        2. Provide max 3 "Key Evidences" as bullet points.
        3. Use simple words. Avoid technical metrics unless essential.
        
        DATA:
        {json.dumps(state_data, ensure_ascii=False)}
        """
        
        response = model.generate_content(simplified_prompt)
        return response.text
    except Exception:
        return "⚠️ AI service unavailable."
def predict_future_state(state_data, timeframe):
    return "Projected Revenue: -5% | Risk: Medium | Key Driver: Competitive pressure"

def simulate_scenario(scenario, state_data):
    return "Financial: Negative | Clients: Higher churn | Verdict: Investigate"

def analyze_specific_domain(domain_name, domain_data):
    return f"- Health: Stable\n- Risks: Competitive pressure\n- Anomalies: Churn spike"