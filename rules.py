from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rules import evaluate_content


app = Flask(__name__)
CORS(app)



# ✅ Create Flask app FIRST
app = Flask(__name__)

# =========================
# Website Route
# =========================
def ai_credibility_check(text):
    if not OPENAI_ENABLED:
        return "AI Disabled", 50, "AI verification not available"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify the news credibility."},
                {"role": "user", "content": text}
            ]
        )
        reply = response.choices[0].message.content
        return "AI Verified", 70, reply

    except Exception as e:
        return "AI Error", 50, str(e)



@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        content = request.form.get("content")

        if content and content.strip():
            result = evaluate_content(content)

    return render_template("index.html", result=result)


# =========================
# API Route (for extension)
# =========================
@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json()
    content = data.get("content", "")
    result = evaluate_content(content)
    return jsonify(result)

@app.route("/report", methods=["POST"])
def report_issue():
    content = request.form.get("content")
    score = request.form.get("score")
    level = request.form.get("level")

    with open("reports.log", "a") as f:
        f.write(f"\nREPORTED ISSUE\n")
        f.write(f"Content: {content}\n")
        f.write(f"Score: {score}, Level: {level}\n")
        f.write("-" * 40)

    return render_template(
        "index.html",
        result={
            "score": score,
            "level": level,
            "reasons": ["Thank you for reporting. This feedback helps improve the system."]
        }
    )



# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)

