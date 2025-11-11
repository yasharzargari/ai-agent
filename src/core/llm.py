import json
from litellm import completion
from .language import Prompt


def generate_response(prompt: Prompt, model: str = "openai/gpt-4o") -> str:
    """Generate response from LLM using function calling"""
    messages = prompt.messages
    tools = prompt.tools

    if not tools:
        response = completion(
            model=model,
            messages=messages,
            max_tokens=1024
        )
        return response.choices[0].message.content
    else:
        # The inclusion of the tools parameter, tells the model what functions it can call. 
        # This is what activates the function calling mechanism.
        response = completion(
            model=model,
            messages=messages,
            tools=tools,
            max_tokens=1024
        )

        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            return json.dumps(result)
        else:
            return response.choices[0].message.content
