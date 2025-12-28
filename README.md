# VerifyBeforeShare
🛡️ VerifyBeforeShare

Think Before You Share

VerifyBeforeShare is a lightweight, rule-based web application designed to help users evaluate the credibility of online content before sharing it—especially during crisis situations where misinformation spreads rapidly.

Instead of deciding what is true or false, the system provides transparent credibility signals that encourage responsible and informed sharing.

🚀 Problem Statement

During emergencies, public events, or breaking news, misinformation often spreads faster than verified information.
Existing solutions frequently rely on opaque automated censorship, which can be biased and difficult to trust.

There is a need for a transparent, explainable, and non-censoring system that helps users pause and assess credibility before sharing content.

💡 Solution Overview

VerifyBeforeShare uses a rule-based credibility scoring system that analyzes common misinformation risk signals such as:

Unknown or unverified sources

Emotional or panic-inducing language

Sensational formatting

Missing references

Highly time-sensitive wording

Each piece of content receives:

A credibility score (0–100)

A credibility level (High / Medium / Low)

Clear explanations showing why points were deducted

No content is blocked or removed.

🧠 How Credibility Scoring Works

Start with a base score of 100

Deduct points when risk signals are detected

Assign credibility levels:

70–100 → High Credibility

40–69 → Medium Credibility

0–39 → Low Credibility

This approach prioritizes explainability and ethics over black-box automation.

🛠️ Technologies Used

Python (Flask) – Backend server and rule evaluation

HTML & CSS – Frontend user interface

Rule-Based Logic – Transparent credibility evaluation

🔐 Ethical Design Principles

No censorship or content blocking

No black-box AI decisions

No data storage or tracking

Focus on user awareness and critical thinking
