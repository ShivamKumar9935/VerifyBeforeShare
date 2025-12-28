from flask import Flask, render_template, request
from rules import evaluate_content

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        content = request.form.get("content")

        if content and content.strip():
            result = evaluate_content(content)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
