import os
import argparse
from generate_content import generate_content
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
    
    # Call Gemini
    client = genai.Client(api_key=api_key)
    generate_content(client, messages, args.verbose)

if __name__ == "__main__":
    main()
