"""
Optimized AI Engine for OmniSight-AI
Focus: Minimal latency, high-density insights, zero redundancy.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    # Fallback/Warning if key is missing
    print("⚠️ WARNING: GOOGLE_API_KEY not found in .env file")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- SHARED PERSONA ---
BASE_PERSONA = """
You are OmniSight AI, a ruthlessly efficient enterprise intelligence agent.
Style: Executive brief. No fluff. No pleasantries. High information density.
Data Context: 6 Domains (Finance, Ops, Partners, Clients, Competitive, Compliance).
"""

def analyze_state(state_data):
    """Generates the main executive briefing."""
    if not api_key: return "⚠️ API Key Missing"
    
    system_prompt = f"""{BASE_PERSONA}
    
    TASK: Analyze the provided enterprise state and identify the SINGLE most critical cross-domain risk.
    
    OUTPUT FORMAT (Markdown):
    ### 🔴 CRITICAL INSIGHT
    [1 sentence: The core problem and its specific financial impact]
    
    ### ⛓️ CAUSAL CHAIN
    **[Root Cause]** → **[Intermediate Effect]** → **[Final Business Impact]**
    
    ### 🛠️ RECOMMENDED ACTION (48h)
    * **Action**: [Specific Step]
    * **Cost**: $[Amount]
    * **ROI**: [X.x]x
    """
    
    # Send minimal data to save tokens
    data_snapshot = {
        "finance_recent": state_data.get('finance', [])[:5],
        "ops_summary": state_data.get('operations', []),
        "partners_at_risk": [p for p in state_data.get('partners', []) if p.get('relationship_health', 1) < 0.8],
        "competitive": state_data.get('competitive', [])
    }
    
    user_message = f"{system_prompt}\n\nDATA: {json.dumps(data_snapshot)}"

    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ AI Analysis Unavailable: {str(e)}"

def ask_ai_question(question, state_data):
    """Context-aware Q&A."""
    if not api_key: return "⚠️ API Key Missing"

    system_prompt = f"""{BASE_PERSONA}
    TASK: Answer the user's question using the provided data.
    CONSTRAINT: Max 2 sentences. Use specific numbers.
    """
    user_message = f"{system_prompt}\n\nDATA: {json.dumps(state_data)[:5000]}\nQUESTION: {question}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return "⚠️ System offline."

def predict_future_state(state_data, timeframe):
    """Predictive modeling."""
    if not api_key: return "⚠️ API Key Missing"

    system_prompt = f"""{BASE_PERSONA}
    TASK: Forecast the state in {timeframe} based on current trends.
    OUTPUT: 
    * **Projected Revenue**: $[Amount] (Change %)
    * **Risk Probability**: [Low/Med/High]
    * **Key Driver**: [1 short sentence]
    """
    user_message = f"{system_prompt}\n\nDATA: {json.dumps(state_data)[:4000]}"
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ Prediction Failed: {e}"

def simulate_scenario(scenario, state_data):
    """What-if simulation."""
    if not api_key: return "⚠️ API Key Missing"

    system_prompt = f"""{BASE_PERSONA}
    TASK: Simulate impact of: "{scenario}".
    OUTPUT FORMAT:
    * **Financial**: [Impact]
    * **Operational**: [Impact]
    * **Market Position**: [Impact]
    * **Verdict**: [Pursue/Avoid]
    """
    user_message = f"{system_prompt}\n\nDATA: {json.dumps(state_data)[:4000]}"
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ Simulation Failed: {e}"

def analyze_specific_domain(domain_name, domain_data):
    """Domain Deep Dive."""
    if not api_key: return "⚠️ API Key Missing"

    system_prompt = f"""{BASE_PERSONA}
    TASK: Analyze {domain_name} domain.
    OUTPUT: 3 bullet points on Health, Risks, and Anomalies.
    """
    user_message = f"{system_prompt}\n\nDATA: {json.dumps(domain_data)}"
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ Domain Analysis Failed: {e}"