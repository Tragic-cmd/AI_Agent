from config import MAX_ITERS
from prompts import system_prompt
from call_function import available_functions, call_function

from google.genai import types

def generate_content(client, messages, verbose):
    for i in range(MAX_ITERS):
        try:
            # 1. call client.models.generate_content(...)
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt,
                ),
            )
            # 2. handle response
            for candidate in response.candidates:
                messages.append(candidate.content)
            if response.usage_metadata is None:
                raise RuntimeError("Failed API request.")
            prompt_token_count = response.usage_metadata.prompt_token_count
            candidates_token_count = response.usage_metadata.candidates_token_count
            if verbose:
                print(f"Prompt tokens: {prompt_token_count}")
                print(f"Response tokens: {candidates_token_count}")
                print(f"Response: {response.text}")
            
            if not response.function_calls and response.text:
                print("Final response:")
                print(response.text)
                return
            # 3. decide whether to break or continue
            tool_parts = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=verbose)
                part = function_call_result.parts[0]
                if part.function_response is None or part.function_response.response is None:
                    raise RuntimeError("Function call did not return a valid response")
                tool_parts.append(part)
                if verbose:
                    print(f"-> {part.function_response.response}")
            # now turn tool_parts into a message and add to conversation
            tool_message = types.Content(role="user", parts=tool_parts)
            messages.append(tool_message)

        except Exception as e:
            if verbose:
                print(f"Error during generation: {e}")
            break