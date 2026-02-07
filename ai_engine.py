"""
Enhanced AI Engine for OmniSight-AI
Multi-agent system with cross-domain reasoning
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyAUvV5AvrRMggIaHqLVhZ7C7bisoijiRy4")

genai.configure(api_key=api_key)

# FIXED: Changed 'gemini-1.5-flash-latest' to 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-1.5-flash')


def analyze_state(state_data):
    """
    Enhanced cross-domain analysis with causal reasoning
    """
    system_prompt = """
    You are OmniSight AI - an elite enterprise intelligence analyst with the ability to see across all business domains simultaneously.

    Your mission: Perform CROSS-DOMAIN CAUSAL ANALYSIS to identify hidden connections that individual department heads would miss.

    ### ANALYSIS FRAMEWORK:

    1. **IDENTIFY THE CORE ISSUE**: What's the most critical problem affecting the business right now?

    2. **CROSS-DOMAIN CORRELATION**: How do issues in one domain (e.g., Partners) cause problems in another (e.g., Finance)?
       - Don't just say "revenue is down" - explain WHY through the causal chain
       - Example: "Competitor pricing → Partner quality decline → Client acquisition cost increase → Revenue impact"

    3. **QUANTIFY THE IMPACT**: Use actual numbers from the data
       - "CAC increased from $245 to $312 (+27%)"
       - "Partner quality in APAC declined 12%"
       - "Revenue down 15% week-over-week"

    4. **ROOT CAUSE ANALYSIS**: What's the ultimate cause?
       - Competitive pressure (40%)
       - Partner economics (35%)
       - Operational issues (25%)

    5. **ACTIONABLE RECOMMENDATIONS**: Be specific with ROI estimates
       - NOT: "Improve partner relationships"
       - YES: "Increase APAC partner commission by $50/client (Investment: $50K, Expected ROI: 3.2x, Timeline: 2 weeks)"

    ### OUTPUT FORMAT (Use Markdown):

    ## 🎯 EXECUTIVE INTELLIGENCE BRIEFING

    ### 🔴 CRITICAL INSIGHT
    [One powerful sentence about the core problem and its cross-domain impact]

    ### 📊 CAUSAL CHAIN ANALYSIS
    **Root Cause → Intermediate Effects → Final Impact**
    
    [Explain the domino effect across domains with specific data]

    ### 💰 BUSINESS IMPACT
    - **Revenue Impact**: $X,XXX (-X%)
    - **Risk Level**: High/Medium/Low
    - **Affected Domains**: X of 6
    - **Trend Direction**: ⬇️ Worsening / ➡️ Stable / ⬆️ Improving

    ### 💡 PRIORITIZED RECOMMENDATIONS

    **1. IMMEDIATE ACTION (48-hour window)**
    - **What**: [Specific action]
    - **Investment**: $XX,XXX
    - **Expected Impact**: [Metric improvement]
    - **ROI**: X.Xx
    - **Confidence**: XX%

    **2. SHORT-TERM (2-4 weeks)**
    - [Similar format]

    **3. STRATEGIC (Long-term)**
    - [Similar format]

    ### ⚠️ EARLY WARNING SIGNALS
    [What to watch for that indicates things are getting worse or better]

    ---

    **KEY PRINCIPLE**: Everything is connected. Show those connections with data.
    """
    
    user_message = f"""{system_prompt}

### CURRENT ENTERPRISE STATE:

**Financial Data**: {json.dumps(state_data.get('finance', [])[:10], indent=2)}  # Recent transactions

**Operations Data**: {json.dumps(state_data.get('operations', []), indent=2)}

**Partner Data**: {json.dumps(state_data.get('partners', []), indent=2)}

**Client Data**: {json.dumps(state_data.get('clients', []), indent=2)}

**Competitive Intelligence**: {json.dumps(state_data.get('competitive', []), indent=2)}

**Compliance Status**: {json.dumps(state_data.get('compliance', []), indent=2)}

Now perform your cross-domain analysis and identify the critical issues connecting these domains.
"""

    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ **Analysis Error**: {e}\n\nPlease check API key and try again."


def ask_ai_question(question, state_data):
    """
    Enhanced Q&A with context-aware responses
    """
    system_prompt = f"""
    You are OmniSight AI Assistant - an intelligent enterprise analyst.
    
    You have access to complete enterprise data across 6 domains:
    - Financial (transactions, revenue, costs)
    - Operations (production, capacity, performance)
    - Partners (suppliers, distributors, quality)
    - Clients (acquisition, retention, risk)
    - Competitive (market intelligence, threats)
    - Compliance (risk, regulations, audits)

    **Your Task**: Answer the user's question with:
    1. Direct answer with specific data
    2. Cross-domain context if relevant
    3. Actionable insights
    4. Confidence level

    **Guidelines**:
    - Be concise but comprehensive
    - Use actual numbers from the data
    - If you see a pattern, mention it
    - If there's a risk, flag it
    - Always provide confidence score

    **Current Data**: {json.dumps(state_data, indent=2)}
    """
    
    user_message = f"{system_prompt}\n\n**User Question**: {question}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Error answering question: {e}"


def analyze_specific_domain(domain_name, domain_data):
    """
    NEW: Deep dive into a specific domain
    """
    system_prompt = f"""
    You are a specialist analyst for the {domain_name} domain.
    
    Analyze this data and provide:
    1. Key trends (up/down/stable)
    2. Anomalies or red flags
    3. Top 3 insights
    4. Recommended actions
    
    Be specific with numbers and percentages.
    """
    
    user_message = f"{system_prompt}\n\n**{domain_name} Data**: {json.dumps(domain_data, indent=2)}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Error analyzing {domain_name}: {e}"


def predict_future_state(state_data, timeframe="30 days"):
    """
    NEW: Predictive analytics
    """
    system_prompt = f"""
    You are OmniSight Predictive Engine.
    
    Based on current trends in the data, forecast what will happen in the next {timeframe}.
    
    **Prediction Framework**:
    1. **Current Trajectory**: Where are we headed if nothing changes?
    2. **Confidence Interval**: Best case / Most likely / Worst case
    3. **Key Assumptions**: What we're assuming holds true
    4. **Trigger Points**: What events would change the forecast
    5. **Recommended Interventions**: Actions to improve the outcome
    
    Use specific numbers and probabilities.
    Format as a brief executive forecast.
    """
    
    user_message = f"{system_prompt}\n\n**Current State**: {json.dumps(state_data, indent=2)}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Prediction error: {e}"


def simulate_scenario(scenario_description, state_data):
    """
    NEW: What-if scenario modeling
    """
    system_prompt = f"""
    You are OmniSight Scenario Modeler.
    
    The user wants to simulate: "{scenario_description}"
    
    **Your Task**:
    1. Model how this scenario would affect each domain
    2. Quantify the impact (use percentages and estimates)
    3. Identify ripple effects across domains
    4. Assess overall risk vs. opportunity
    5. Provide recommendation: Pursue / Avoid / Mitigate
    
    **Impact Assessment Format**:
    - Financial Impact: [estimated change]
    - Operational Impact: [estimated change]
    - Partner Impact: [estimated change]
    - Client Impact: [estimated change]
    - Competitive Position: [estimated change]
    - Compliance Risk: [assessment]
    
    Overall Recommendation: [Action with reasoning]
    """
    
    user_message = f"{system_prompt}\n\n**Current Baseline**: {json.dumps(state_data, indent=2)}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Scenario simulation error: {e}"


def generate_executive_briefing(state_data):
    """
    NEW: Automated morning briefing
    """
    system_prompt = """
    You are OmniSight Morning Briefing Generator.
    
    Create a concise executive briefing in this format:
    
    ## 🌅 DAILY INTELLIGENCE BRIEFING
    
    ### 🔴 REQUIRES IMMEDIATE ATTENTION (Top 3)
    1. [Issue] - [Impact] - [Recommended action]
    2. [Issue] - [Impact] - [Recommended action]
    3. [Issue] - [Impact] - [Recommended action]
    
    ### 🟡 EMERGING RISKS (Monitoring)
    - [Risk 1]: [Why it matters]
    - [Risk 2]: [Why it matters]
    
    ### 🟢 OPPORTUNITIES IDENTIFIED
    - [Opportunity]: [Potential value]
    
    ### 📊 KEY METRICS SNAPSHOT
    - Revenue: [Trend]
    - Operations: [Status]
    - Partners: [Health]
    - Clients: [Status]
    
    **Bottom Line**: [One sentence summary of business health]
    
    Keep it scannable - busy executives should read this in 60 seconds.
    """
    
    user_message = f"{system_prompt}\n\n**Current Data**: {json.dumps(state_data, indent=2)}"
    
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        return f"Briefing generation error: {e}"


# Backward compatibility - keep original function
def analyze_state_simple(state_data):
    """Original simple version"""
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