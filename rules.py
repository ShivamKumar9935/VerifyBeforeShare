import re

# Known reliable sources (you can expand this list)
RELIABLE_SOURCES = [
    "gov.in", "who.int", "bbc.com", "reuters.com",
    "ndtv.com", "timesofindia.com", "thehindu.com","timesofindia.indiatimes.com"


]

# Emotional / panic keywords
EMOTIONAL_KEYWORDS = [
    "urgent", "breaking", "shocking", "alert",
    "panic", "danger", "warning", "forward",
    "share immediately", "do not ignore"
]

# Time-sensitive keywords
TIME_KEYWORDS = [
    "just now", "right now", "today only",
    "happening now", "at this moment"
]


def evaluate_content(text: str) -> dict:
    score = 100
    reasons = []
    text_lower = text.lower()

    # 1️⃣ Source Reliability Check
    if not any(source in text_lower for source in RELIABLE_SOURCES):
        score -= 25
        reasons.append("Source is unverified or unknown")

    # 2️⃣ Emotional Language Check
    if any(word in text_lower for word in EMOTIONAL_KEYWORDS):
        score -= 20
        reasons.append("Emotional or panic-inducing language detected")

    # 3️⃣ Sensational Formatting Check
    if re.search(r"[A-Z]{4,}", text) or "!!!" in text:
        score -= 10
        reasons.append("Sensational formatting (CAPS or excessive punctuation)")

    # 4️⃣ Context & Reference Check
    if "http" not in text_lower and "www" not in text_lower:
        score -= 15
        reasons.append("Lack of references or supporting links")

    # 5️⃣ Time Sensitivity Check
    if any(word in text_lower for word in TIME_KEYWORDS):
        score -= 15
        reasons.append("Highly time-sensitive wording detected")

    # Keep score in valid range
    score = max(score, 0)

    # Decide credibility level
    if score >= 70:
        level = "High Credibility"
    elif score >= 40:
        level = "Medium Credibility"
    else:
        level = "Low Credibility"

    # If nothing triggered, add positive message
    if not reasons:
        reasons.append("No major credibility risk signals detected")

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }
