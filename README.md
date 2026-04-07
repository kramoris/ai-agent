# AI Agent

Simple AI Agent using gemini-2.5-flash made during Boot.dev with some improvements.

## ⚠️ Warning

This project allows executing Python code and accessing the local filesystem.

Running it with untrusted input can lead to arbitrary code execution and data exposure.

It can modify or delete files on your system.

## Requirements
- Python 3.13 or newer
- python-dotenv 1.1.0
- google-genai 1.12.1

## Install
If Python 3.13 or newer is installed:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-genai==1.12.1
pip install python-dotenv==1.1.0
```

If not:

install uv and run:
```bash
uv venv --python 3.13
source .venv/bin/activate
uv add google-genai==1.12.1
uv add python-dotenv==1.1.0
```

After completing set up, you need to create .env file in root of the project and add API key in the following format:
```bash
GEMINI_API_KEY='your_api_key_here'
```

## Run
```bash
python3 main.py "User prompt"
```