import argparse
import os

from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()

    model = "gemini-2.5-flash"

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)
    generated_content = client.models.generate_content(model=model, contents=args.user_prompt)
    if not generated_content.usage_metadata:
        raise RuntimeError("No usage metadata found")

    prompt_tokens = generated_content.usage_metadata.prompt_token_count
    response_tokens = generated_content.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    print(f"Response:\n{generated_content.text}")


if __name__ == "__main__":
    main()
