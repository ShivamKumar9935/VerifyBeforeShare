from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from rules import evaluate_content

# =========================
# Create Flask App (ONCE)
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# Website Route
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        content = request.form.get("content", "")

        if content.strip():
            result = evaluate_content(content)

    return render_template("index.html", result=result)

# =========================
# API Route (Browser Extension)
# =========================
@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json() or {}
    content = data.get("content", "")
    result = evaluate_content(content)
    return jsonify(result)

# =========================
# Report Issue Route
# =========================
@app.route("/report", methods=["POST"])
def report_issue():
    content = request.form.get("content")
    score = request.form.get("score")
    level = request.form.get("level")

    with open("reports.log", "a") as f:
        f.write("\nREPORTED ISSUE\n")
        f.write(f"Content: {content}\n")
        f.write(f"Score: {score}, Level: {level}\n")
        f.write("-" * 40 + "\n")

    return render_template(
        "index.html",
        result={
            "score": score,
            "level": level,
            "reasons": [
                "Thank you for reporting.",
                "This feedback will be reviewed to improve the system."
            ]
        }
    )

# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
