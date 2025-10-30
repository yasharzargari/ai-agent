import json
from litellm import completion
from core.prompt import Prompt


def generate_response(prompt: Prompt) -> str:
    """Call LLM to get response using litellm."""
    messages = prompt.messages
    tools = prompt.tools

    if not tools:
        response = completion(
            model="openai/gpt-4o",
            messages=messages,
            max_tokens=1024
        )
        return response.choices[0].message.content
    else:
        response = completion(
            model="openai/gpt-4o",
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