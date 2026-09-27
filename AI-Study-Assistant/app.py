from flask import Flask, render_template, request, jsonify
import os
from google import genai

app = Flask(__name__)

# Gemini API client
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


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

    if client is None:
        return "AI Error: GEMINI_API_KEY is not configured."

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)