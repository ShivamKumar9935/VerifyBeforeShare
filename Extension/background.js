chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "verifyText",
        title: "VerifyBeforeShare – Check Reliability",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener((info) => {
    if (info.menuItemId === "verifyText") {
        fetch("https://verifybeforeshare.onrender.com/api/check", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ content: selectedText })
})

        .then(res => res.json())
        .then(data => {
            chrome.notifications.create({
                type: "basic",
                iconUrl: "icon.png",   // optional
                title: data.level,
                message: `Score: ${data.score}/100`
            });
        })
        .catch(() => {
            chrome.notifications.create({
                type: "basic",
                iconUrl: "icon.png",
                title: "VerifyBeforeShare",
                message: "Backend not running"
            });
        });
    }
});
