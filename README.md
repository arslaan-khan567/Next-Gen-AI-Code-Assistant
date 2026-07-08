# Next-Gen-AI-Code-Assistant

This repository contains a full-stack Flask web application that automatically solves programming problems. Users can either type a problem statement or upload an image containing a problem. The app extracts the text, uses an AI agent to generate the corresponding Python code, executes it safely within a secure sandbox environment, and returns both the code and the runtime output to the user.

🚀 Features
-Dual Input Modes: Accepts text queries or images containing problem descriptions.
-Optical Character Recognition (OCR): Uses Tesseract OCR to extract text dynamically from uploaded images.
-AI Code Generation: Leverages the Agno framework integrated with Groq (using LLMs like openai/gpt-oss-120b) to generate pure, executable Python code blocks.
-Secure Code Execution: Utilizes E2B Sandbox to run the generated code safely in an isolated cloud environment, preventing malicious execution on the host machine.
-Clean Web Interface: A minimalist UI powered by Flask templates (index.html).

🛠️ Tech Stack
Backend: Flask (Python)
AI Agent Framework: Agno Agent API
LLM Provider: Groq Cloud
OCR Engine: Tesseract OCR (via pytesseract & Pillow)
Secure Sandbox: E2B Code Interpreter (e2b_code_interpreter)
Environment Management: python-dotenv

📂 Project Structure
├── app.py             # Main Flask application logic, OCR processing, and AI execution
├── templates/
│   └── index.html     # Frontend HTML file for user input and results display
├── .env               # Environment variables (API keys, paths)
└── README.md          # Project documentation
