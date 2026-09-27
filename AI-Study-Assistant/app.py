from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

MODEL = "llama3.2:3b"


def study_assistant(topic, mode):
    topic = topic.strip()

    if not topic:
        return "Please enter a topic or question."

    prompts = {
        "explain": f"""
Explain {topic} in very easy language for a B.Tech 1st year student.

Give:
1. Simple definition
2. Main concept
3. Important points
4. One easy example
5. Short conclusion

Use simple English.
""",

        "summary": f"""
Give a simple summary of {topic} for a B.Tech 1st year student.
Give 5 to 7 important bullet points.
""",

        "quiz": f"""
Create 5 MCQ questions about {topic}.
Give options A, B, C and D.
At the end, provide the correct answers.
""",

        "plan": f"""
Create a simple 5-day study plan for {topic}.
Include learning, practice and revision.
"""
    }

    prompt = prompts.get(mode)

    if not prompt:
        return "Please select a valid option."

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    topic = data.get("topic", "")
    mode = data.get("mode", "explain")

    answer = study_assistant(topic, mode)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)