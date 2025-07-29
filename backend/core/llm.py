import os
import groq
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client with API key
if groq_api_key:
    try:
        client = groq.Groq(api_key=groq_api_key)
        logging.info("Successfully initialized Groq client.")
    except Exception as e:
        logging.error(f"Failed to initialize Groq client: {e}")
        client = None  # Disable client if initialization fails
else:
    logging.warning("GROQ_API_KEY not found in environment.")
    client = None  # Disable client if API key is missing

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
    if not client:
        logging.warning("Groq client is not initialized. Returning empty explanation and recommendation.")
        return {
            "explanation": "Groq client is not initialized. Please check the API key.",
            "recommendation": "",
            "generated_at": datetime.utcnow()
        }

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
        logging.info(f"Sending prompt to Groq API: {prompt}")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a predictive maintenance assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        logging.info(f"Received response from Groq API: {content}")
        # Simple split: explanation vs recommendation
        explanation, *recommendation = content.split("Recommendation:")
        return {
            "explanation": explanation.strip(),
            "recommendation": (recommendation[0].strip() if recommendation else ""),
            "generated_at": datetime.utcnow()
        }
    except Exception as e:
        logging.exception(f"Groq API call failed: {e}")
        return {
            "explanation": f"LLM API call failed: {e}",
            "recommendation": "",
            "generated_at": datetime.utcnow()
        }
