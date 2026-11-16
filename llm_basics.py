import json

from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

## 1 simplest possible API Call 
result = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    messages = [{
        "role": "user",
        "content": "what is the square of 49?"
    }]
)

# print(result.choices[0].message.content)
print(json.dumps(result.to_dict(), indent=2))

## 2 multi-turn conversation (passing a list of messages)

# result = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",
#     messages =[
#         {
#             "role": "user",
#             "content": "My Name is Rushikesh"
#         },
#         {
#             "role": "assistant",
#             "content": "Nice to meet you Rushikesh"
#         },
#         {
#             "role": "user",
#             "content": "What is my name?"
#         }
#     ]
# )

# print(result.choices[0].message.content)

## 3 Now we add system prompts, temperature, max_tokens

# result = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",
#     messages = [{
#         "role": "user",
#         "content":"what is the current year and month?"
#     }],
#     temperature = 0.7,
#     max_tokens = 10
# )

# print(result)
# print(result.choices[0].message.content)
# print("Total Tokens", result.usage.total_tokens)

## streaming responses

# stream = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",
#     messages = [{
#         "role": "user",
#         "content":"Tell me a short story about a robot?"
#     }],
#     stream = True
# )

# for event in stream:
#     if hasattr(event, "choices"):
#         print(event.choices[0].delta.content, end="", flush=True)