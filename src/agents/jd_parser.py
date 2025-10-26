"""
JD Parser Agent - Extracts structured data from job descriptions.

This LLM agent uses GPT-4o with structured output to parse unstructured
job postings into a standardized JDRecord format with company, role,
skills, requirements, and other key fields.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
from ..utils.parser_utils import load_prompt, load_schema
from ..utils.config_utils import get_config

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "../../config/prompts/jd_parser.txt")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../../config/schemas/jd_record_schema.json")

JD_PARSER_PROMPT = load_prompt(PROMPT_PATH)
JD_PARSER_SCHEMA = load_schema(SCHEMA_PATH)

# Load model config from config.json
config = get_config()
model_config = config.get("MODEL_CONFIG", {}).get(
    "jd_parser", {"model_name": "gpt-4o", "temperature": 0}
)

# Pass all config parameters to ChatOpenAI
llm = ChatOpenAI(**model_config)
structured_llm = llm.with_structured_output(JD_PARSER_SCHEMA)


def parse_job_description(job_description: str) -> Optional[Dict[str, Any]]:
    """
    Parse job description text using LLM with structured output.

    Args:
        job_description: Raw job description text

    Returns:
        Parsed JD dictionary or None if parsing fails

    Raises:
        Exception: Logs errors but returns None instead of raising
    """
    if not job_description or not job_description.strip():
        logging.warning("Empty job description provided to parser")
        return None

    try:
        system_prompt = JD_PARSER_PROMPT
        user_prompt = (
            "Parse the following job posting and extract structured information according to the guidelines in the system prompt:\n\n"
            f"{job_description}"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        result = structured_llm.invoke(messages)
        return result
    except Exception as e:
        logging.error(f"JD parsing failed: {type(e).__name__}: {e}")
        return None
