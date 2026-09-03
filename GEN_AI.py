from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)


def ask_llama(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = "Generate clean working code:\n" + data.get("prompt", "")
    result = ask_llama(prompt)
    return jsonify({"result": result})


@app.route("/explain", methods=["POST"])
def explain():
    data = request.json
    prompt = "Explain this code simply:\n" + data.get("code", "")
    result = ask_llama(prompt)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)