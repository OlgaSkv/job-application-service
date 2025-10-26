# --- Config loading utilities ---
import json
import logging


def load_prompt(path: str) -> str:
    """
    Load a prompt file from disk.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to load prompt: {e}")
        raise


def load_schema(path: str) -> dict:
    """
    Load a JSON schema file from disk.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load schema: {e}")
        raise


# General-purpose and job-related utility functions
import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


# --- Normalization ---
def sanitize_filename(text):
    """
    Sanitize text for use in filenames (max 50 chars, ASCII, no special chars)
    """
    if not text:
        return "Unknown"
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", str(text))
    sanitized = re.sub(r"\s+", "_", sanitized.strip())
    sanitized = sanitized.rstrip(". ")
    return sanitized[:50] if sanitized else "Unknown"


# --- Job description cleaning ---
def clean_job_description(text: str) -> str:
    """
    Lightly clean job description text: remove unprintable characters and normalize whitespace.

    Args:
        text: Raw job description text

    Returns:
        str: Cleaned text with normalized whitespace and printable characters only
    """
    if not text:
        return ""

    # Remove unprintable characters (keep newlines, tabs, spaces)
    printable = "".join(char for char in text if char.isprintable() or char in "\n\t ")

    # Normalize excessive whitespace
    # Convert multiple spaces to single space
    cleaned = re.sub(r" +", " ", printable)
    # Convert multiple tabs to single space
    cleaned = re.sub(r"\t+", " ", cleaned)
    # Convert multiple newlines to double newline (preserve paragraph breaks)
    cleaned = re.sub(r"\n\n+", "\n\n", cleaned)
    # Remove trailing whitespace from each line
    cleaned = "\n".join(line.rstrip() for line in cleaned.split("\n"))

    return cleaned.strip()


# --- Job URL utilities ---
def normalize_job_url(url: str) -> str:
    """
    Normalize job URLs by removing tracking parameters and standardizing format
    """
    if not url:
        return url
    parsed = urlparse(url.strip())
    allowed_params = {
        "greenhouse.io": ["gh_jid"],
        "linkedin.com": ["currentJobId"],
        "indeed.com": ["jk"],
        "careerbuilder.com": ["job_did"],
        "lever.co": [],
        "myworkdayjobs.com": [],
        "workdayjobs.com": [],
        "smartrecruiters.com": [],
        "ashbyhq.com": [],
    }
    domain = parsed.netloc.lower()
    keep_params = []
    for portal, params in allowed_params.items():
        if portal in domain:
            keep_params = params
            break
    path = re.sub(r"/+", "/", parsed.path or "/")
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    if keep_params and parsed.query:
        params = parse_qsl(parsed.query)
        filtered = [(k, v) for k, v in params if k in keep_params and v]
        query = urlencode(filtered)
    else:
        query = ""
    return urlunparse((parsed.scheme or "https", domain, path, "", query, ""))


def get_job_portal_name(url: str) -> str:
    """
    Extract job portal name from URL
    """
    if not url:
        return "Unknown"
    try:
        parsed = urlparse(url.strip())
        domain = parsed.netloc.lower()
        portal_mapping = {
            "linkedin.com": "LinkedIn",
            "indeed.com": "Indeed",
            "glassdoor.com": "Glassdoor",
            "monster.com": "Monster",
            "careerbuilder.com": "CareerBuilder",
            "ziprecruiter.com": "ZipRecruiter",
            "dice.com": "Dice",
            "simplyhired.com": "SimplyHired",
            "greenhouse.io": "Greenhouse",
            "boards.greenhouse.io": "Greenhouse",
            "myworkdayjobs.com": "Workday",
            "workdayjobs.com": "Workday",
            "myworkdaysite.com": "Workday",
            "smartrecruiters.com": "SmartRecruiters",
            "ashbyhq.com": "Ashby",
            "recruiting.ultipro.com": "UltiPro",
            "amazon.jobs": "Amazon Jobs",
            "wellfound.com": "Wellfound",
            "angel.co": "AngelList",
            "ycombinator.com": "Y Combinator",
            "stackoverflow.com": "Stack Overflow Jobs",
            "hired.com": "Hired",
            "vettery.com": "Vettery",
        }
        if domain in portal_mapping:
            return portal_mapping[domain]
        for portal_domain, portal_name in portal_mapping.items():
            if domain.endswith(portal_domain):
                return portal_name
        if "careers." in domain or "jobs." in domain:
            base_domain = domain.replace("careers.", "").replace("jobs.", "")
            company_name = base_domain.split(".")[0].title()
            return f"{company_name} Careers"
        return domain.split(".")[0].title()
    except Exception:
        return "Unknown"
