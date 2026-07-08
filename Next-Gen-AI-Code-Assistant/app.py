import os
from PIL import Image
import pytesseract
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from flask import Flask, request, render_template

load_dotenv()

tesseract_path = os.getenv("TESSERACT_CMD")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")
app = Flask(__name__)

my_ai = Agent(
    model = Groq(id ="openai/gpt-oss-120b", 
              api_key= GROQ_API_KEY ), 
              markdown = True 
)

def generate_code(problem : str):
    prompt = f"""You are a Python developer. Solve the problem below.
                Return ONLY a python code block. No explanation before or after
                Problem: {problem}"""
    response = my_ai.run(prompt)
    full_response = response.content
    if "```python" not in full_response:
        return None
    clean_response = full_response.split("```python")[1].split("```")[0]
    return clean_response

def execution_code(code):
    try:
        with Sandbox(timeout=30) as sandbox:
            execution = sandbox.run_code(code)
            if execution.error:
                return f"Error: {execution.error.name}: {execution.error.value}"
            return "\n".join(execution.logs.stdout) if execution.logs.stdout else "No Output"
    except Exception as e:
        return f"Sandbox failed: {e}"

def extract_text_from_image(image_file) -> str:
    img = Image.open(image_file.stream)
    text = pytesseract.image_to_string(img).strip()
    return text
        
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method != "POST":
        return render_template("index.html")

    image = request.files.get("image")
    if image and image.filename:
        query = extract_text_from_image(image)
    else:
        query = request.form.get("query")

    if not query:
        return render_template("index.html", result="error: no problem given")

    code = generate_code(query)
    if not code:
        return render_template("index.html", result="error: model didn't return code")

    output = execution_code(code)
    return render_template("index.html", solution=code, result=output)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")