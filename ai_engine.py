import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
# Keep your key here (or use os.getenv("GOOGLE_API_KEY") for better security)
api_key = "AIzaSyAUvV5AvrRMggIaHqLVhZ7C7bisoijiRy4" 

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

# --- FUNCTION 1: The Analyst (Proactive) ---
def analyze_state(state_data):
    """
    Analyzes the full business state and returns a strategic executive summary.
    """
    system_prompt = """
    You are a senior strategic advisor.
    Synthesize the provided data (Finance, Operations, Partners) into a brief, high-impact memo.

    ### GUIDELINES:
    1. No fluff, no pleasantries, no robotic transitions.
    2. Focus strictly on cross-domain causality (e.g., how Partner issues are causing Financial variance).
    3. Use a direct, professional tone.

    ### FORMAT:
    
    EXECUTIVE BRIEFING: [High-Impact 5-Word Headline]

    CRITICAL INSIGHT:
    [1-2 sentences explaining the root cause connection. Example: Revenue is underperforming targets because Supplier X has failed to deliver, creating a bottleneck in Operations.]

    RECOMMENDATIONS:
    * Immediate: [Specific tactical step] (Est. Impact: [Value])
    * Strategic: [Long-term correction] (Est. Impact: [Value])
    """
    
    user_message = f"{system_prompt}\n\nCurrent Data: {json.dumps(state_data)}"

    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Error analyzing state: {e}"

# --- FUNCTION 2: The Chatbot (Reactive) ---
def ask_ai_question(question, state_data):
    """
    Answers a specific user question based on the current data state.
    """
    system_prompt = f"""
    You are a helpful Enterprise Assistant.
    Answer strictly based on this data: {json.dumps(state_data)}
    Be concise.
    """
    
    user_message = f"{system_prompt}\n\nUser Question: {question}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Error answering question: {e}"