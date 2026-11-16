from groq import Groq
import json
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# result = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",
#     messages = [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant."
#         },
#         {
#             "role": "user",
#             "content": "what is the current weather in Pune?"
#         }

#     ]
# )

# print(result.choices[0].message.content)

##I’m sorry, but I don’t have the ability to fetch real‑time weather data. For the most accurate and up‑to‑date information, you could check a trusted weather website or app (for example, the Weather Channel, AccuWeather, or alocal meteorological service), or use a search engine or voice assistant that’s connected to the internet.
## this will be the output of the above code snippet. The model is not able to fetch real time data, so it is giving a generic response.
## so that is why we giving a tool call to fetch the real time data. The model will call the tool and get the real time data and give the response to the user.

def get_weather(city:str):
    return {
        "city": city,
        "temperature": "30",
        "unit": "Celsius",
        "condition": "Sunny"
    }

## tool defination

tools = [
    {
        "type": "function",
        "function": {
        "name": "get_weather",
        "description": "Get the current weather in a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get the weather for"
                }
            },
            "required": ["city"]
        }
        }
    }
]

input_messages = [
        {
            "role": "user",
            "content": "what is the current weather in Pune?"
        }

    ]

result = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    messages = input_messages,
    tools = tools
)

# print(result.choices[0].message.content)
# print(json.dumps(result.to_dict(), indent=2))

tool_call = result.choices[0].message.tool_calls
function_name = tool_call[0].function.name
function_args = json.loads(tool_call[0].function.arguments)

function_result = get_weather(function_args["city"])

# print(f"reslut: {function_result}")

input_messages.append({"role": "assistant","tool_calls" : tool_call})
input_messages.append({
    "role": "tool",
    "tool_call_id": tool_call[0].id,
    "content": json.dumps(function_result)
})

final_result = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=input_messages,
    tools=tools
)

print(final_result.choices[0].message.content)

