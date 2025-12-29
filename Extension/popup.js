document.getElementById("check").addEventListener("click", async () => {
    const content = document.getElementById("content").value;
    const resultDiv = document.getElementById("result");

    if (!content) {
        resultDiv.innerText = "Please enter text or a link.";
        return;
    }

    resultDiv.innerText = "Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content })
        });

        const data = await response.json();

        resultDiv.innerHTML = `
            <strong>${data.level}</strong><br>
            Score: ${data.score}/100
        `;
    } catch (error) {
        resultDiv.innerText = "Backend not running.";
    }
});
