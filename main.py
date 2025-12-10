import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.prompt`

    prompt = args.prompt
    load_dotenv()

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    # API
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")
    
    # Gemini
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )

    # Response
    if response.usage_metadata is None:
        raise RuntimeError("Failed API request.")
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")
        print(f"Response: {response.text}")
    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
