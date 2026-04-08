import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    load_dotenv()

    model = "gemini-2.5-flash"
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found")

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if not response.usage_metadata:
            raise RuntimeError("No usage metadata found")

        if args.verbose:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        if response.function_calls:
            function_responses = []

            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)

                if not function_call_result.parts:
                    raise RuntimeError("Function call result has no parts")

                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise RuntimeError("Function call result is missing function_response")

                if function_response.response is None:
                    raise RuntimeError("Function response is missing response data")

                function_responses.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_response.response}")

            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(f"Final response:\n{response.text}")
            return

    print("Error: Maximum iterations reached before the agent produced a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
