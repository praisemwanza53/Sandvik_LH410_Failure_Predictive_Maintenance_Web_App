import os
import groq
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = groq.Groq(api_key=groq_api_key)

PROMPT_TEMPLATE = """
You are a technical assistant. Based on this failure prediction:

Component: {component}
Alarm Type: {alarm}
Failure Probability: {probability}
Estimated Time to Failure: {hours_to_failure} hrs
SPN/FMI: {spn}/{fmi}
Count: {count}

Give a clear explanation and actionable recommendation for a field engineer.
"""

async def get_llm_explanation(prediction: dict, alarm: dict):
    prompt = PROMPT_TEMPLATE.format(
        component=prediction["component"],
        alarm=alarm["alarm_type"],
        probability=prediction["probability"],
        hours_to_failure=prediction["hours_to_failure"],
        spn=alarm["spn"],
        fmi=alarm["fmi"],
        count=alarm["count"]
    )
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a predictive maintenance assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        # Simple split: explanation vs recommendation
        explanation, *recommendation = content.split("Recommendation:")
        return {
            "explanation": explanation.strip(),
            "recommendation": (recommendation[0].strip() if recommendation else ""),
            "generated_at": datetime.utcnow()
        }
    except Exception as e:
        return {
            "explanation": f"LLM API call failed: {e}",
            "recommendation": "",
            "generated_at": datetime.utcnow()
        }