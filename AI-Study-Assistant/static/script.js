async function askAssistant(mode) {

    const topic = document.getElementById("topic").value;
    const answer = document.getElementById("answer");

    if (topic.trim() === "") {
        answer.innerText = "Please enter a topic first.";
        return;
    }

    answer.innerText = "Thinking...";

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                topic: topic,
                mode: mode
            })

        });

        const data = await response.json();

        answer.innerText = data.answer;

    } catch (error) {

        answer.innerText =
            "Something went wrong. Please try again.";

    }
}