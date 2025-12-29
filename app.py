from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rules import evaluate_content
from dotenv import load_dotenv

load_dotenv()
# =========================
app = Flask(__name__)
CORS(app)

# ===== ====================
# Websit    e Route
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        content = request.form.get("content")
        use_ai = request.form.get("use_ai") == "true"

        if content and content.strip():
            result = evaluate_content(content, use_ai=use_ai)

    return render_template("index.html", result=result)


# =========================
# API Route (for extension)
# =========================
@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json()
    content = data.get("content", "")
    use_ai = data.get("use_ai", True)
    result = evaluate_content(content, use_ai=use_ai)
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
        f.write("-" * 40 + "\n")

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
