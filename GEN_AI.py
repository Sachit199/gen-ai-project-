from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def ask_llama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "No response")
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