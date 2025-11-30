from flask import Flask, request, jsonify, render_template_string
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeDraft AI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
        textarea { width: 100%; height: 100px; }
        pre { background: #222; color: #0f0; padding: 15px; border-radius: 10px; }
        button { padding: 10px 20px; background: #007BFF; color: white; border: none; border-radius: 6px; }
    </style>
</head>
<body>
    <h1>⚡ CodeDraft AI</h1>
    <p>Ask the AI to build code for you:</p>
    <textarea id="prompt" placeholder="e.g., Create a to-do list app using HTML, CSS, JS..."></textarea><br><br>
    <button onclick="generate()">Generate Code</button>
    <h2>Output:</h2>
    <pre id="output"></pre>

    <script>
        async function generate() {
            const prompt = document.getElementById('prompt').value;
            document.getElementById('output').innerText = "Generating...";
            const res = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt })
            });
            const data = await res.json();
            document.getElementById('output').innerText = data.response || "Error generating code.";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()

    if not prompt:
        return jsonify({'response': 'Please enter a valid prompt.'})

    try:
        result = subprocess.run(
            ["ollama", "run", "codellama:7b", prompt],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        return jsonify({'response': output})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
