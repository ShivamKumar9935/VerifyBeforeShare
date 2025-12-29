import re
import os
import json
from groq import Groq

# Initialize Groq client (FREE API)
client = Groq(api_key=os.environ.get("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"))

# Known reliable sources
RELIABLE_SOURCES = [
    "gov.in", "who.int", "bbc.com", "reuters.com",
    "ndtv.com", "timesofindia.com", "thehindu.com",
    "timesofindia.indiatimes.com", "apnews.com", "cnn.com",
    "aljazeera.com", "theguardian.com", "nytimes.com"
]

# Known Unreliable
UNRELIABLE_SOURCES = [
    "fake-news.com", "clickbait.com", "unreliablesite.org", 
    "babylonbee.com", "theonion.com"
]

# Emotional / panic keywords
EMOTIONAL_KEYWORDS = [
    "urgent", "breaking", "shocking", "alert",
    "panic", "danger", "warning", "forward",
    "share immediately", "do not ignore", "must read",
    "you won't believe", "doctors hate this"
]

# Time-sensitive keywords
TIME_KEYWORDS = [
    "just now", "right now", "today only",
    "happening now", "at this moment", "limited time"
]


def evaluate_content_with_ai(text: str) -> dict:
    """
    Use Groq AI (FREE) to analyze content for misinformation
    Using Llama 3.1 70B model - fast and accurate
    """
    try:
        prompt = f"""You are an expert fact-checker and misinformation analyst. Analyze the following content for credibility and potential misinformation.

Content to analyze:
{text}

Provide a detailed analysis with:
1. A credibility score from 0-100 (where 100 is highly credible)
2. Specific red flags or positive indicators you identified
3. Whether sources are cited and if they appear reliable
4. Analysis of emotional manipulation tactics
5. Fact-checking recommendations

IMPORTANT: Respond ONLY with valid JSON, no markdown formatting or extra text.

{{
    "score": <number 0-100>,
    "level": "<High Credibility|Medium Credibility|Low Credibility>",
    "reasons": ["reason1", "reason2", "reason3"],
    "analysis": "brief overall assessment in one sentence"
}}

Be thorough but concise. Focus on actionable insights."""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-70b-versatile",  # Fast and FREE
            temperature=0.3,  # Lower temperature for more consistent analysis
            max_tokens=800
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Clean up response - remove markdown if present
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        # Find JSON in response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            
            # Ensure score is within bounds
            result['score'] = max(0, min(100, int(result['score'])))
            
            # Validate and set default level if needed
            if result['level'] not in ["High Credibility", "Medium Credibility", "Low Credibility"]:
                score = result['score']
                if score >= 70:
                    result['level'] = "High Credibility"
                elif score >= 40:
                    result['level'] = "Medium Credibility"
                else:
                    result['level'] = "Low Credibility"
            
            # Ensure reasons is a list
            if not isinstance(result.get('reasons'), list):
                result['reasons'] = ["AI analysis completed"]
            
            return result
        else:
            # If JSON parsing fails, try to extract meaningful info
            return {
                "score": 50,
                "level": "Medium Credibility",
                "reasons": ["AI analysis completed but response format was unexpected"],
                "analysis": response_text[:200] if response_text else "Analysis inconclusive"
            }
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response was: {response_text[:200]}")
        return evaluate_content_rules_based(text)
    except Exception as e:
        print(f"AI analysis error: {e}")
        # Fallback to rule-based system
        return evaluate_content_rules_based(text)


def evaluate_content_rules_based(text: str) -> dict:
    """
    Original rule-based evaluation (fallback method)
    """
    score = 100
    reasons = []
    text_lower = text.lower()

    # 1️⃣ Source Reliability Check
    has_reliable_source = any(source in text_lower for source in RELIABLE_SOURCES)
    if not has_reliable_source:
        score -= 25
        reasons.append("⚠️ Source is unverified or unknown")
    else:
        reasons.append("✅ Recognized reliable source detected")

    # 2️⃣ Emotional Language Check
    emotional_words_found = [word for word in EMOTIONAL_KEYWORDS if word in text_lower]
    if emotional_words_found:
        score -= 20
        reasons.append(f"⚠️ Emotional language detected: {', '.join(emotional_words_found[:3])}")

    # 3️⃣ Source Unreliability Check
    unreliable_found = [source for source in UNRELIABLE_SOURCES if source in text_lower]
    if unreliable_found:
        score -= 50
        reasons.append(f"❌ Unreliable source detected: {unreliable_found[0]}")

    # 4️⃣ Sensational Formatting Check
    if re.search(r"[A-Z]{4,}", text):
        score -= 10
        reasons.append("⚠️ Excessive CAPS detected (sensational formatting)")
    
    if "!!!" in text or text.count("!") > 3:
        score -= 10
        reasons.append("⚠️ Excessive punctuation detected")

    # 5️⃣ Context & Reference Check
    has_links = "http" in text_lower or "www" in text_lower
    if not has_links and len(text) > 100:
        score -= 15
        reasons.append("⚠️ No references or supporting links provided")
    elif has_links:
        reasons.append("✅ Contains reference links")

    # 6️⃣ Time Sensitivity Check
    time_words_found = [word for word in TIME_KEYWORDS if word in text_lower]
    if time_words_found:
        score -= 15
        reasons.append(f"⚠️ Time-sensitive urgency detected: {time_words_found[0]}")

    # 7️⃣ Length check (very short messages are often suspicious)
    if len(text.strip()) < 20:
        score -= 15
        reasons.append("⚠️ Very short message (lacks context)")

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
        reasons.append("✅ No major credibility risk signals detected")

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }


def evaluate_content(text: str, use_ai: bool = True) -> dict:
    """
    Main evaluation function that can use AI or rule-based approach
    """
    if use_ai and os.environ.get("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"):
        try:
            return evaluate_content_with_ai(text)
        except:
            print("AI failed, using rule-based fallback")
            return evaluate_content_rules_based(text)
    else:
        return evaluate_content_rules_based(text)
