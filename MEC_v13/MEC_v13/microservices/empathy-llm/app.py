from flask import Flask, request, jsonify
from empathy_llm.model.prompt_templates import build_prompt
from empathy_llm.model.loader import generate_response

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("user_input")
    esil = data.get("esil", {})
    persona = data.get("persona", {})

    prompt = build_prompt(user_input, esil, persona)
    output = generate_response(prompt)

    return jsonify({
        "response": output.strip(),
        "prompt": prompt.strip()
    })

if __name__ == "__main__":
    app.run(port=8008, host="0.0.0.0", debug=True)
