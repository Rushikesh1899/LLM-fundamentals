from groq import Groq
import os
from pydantic import BaseModel, ConfigDict

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# result = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",
#     messages = [{
#         "role": "user",
#         "instructions": "You are a helpful assistant.",
#         "content": "Give me the name,age and city of a fictional person."
#     }]
# )

# print(result.choices[0].message.content)
# print(type(result.choices[0].message.content))

## output is not structured, so we can use structured outputs to get a naive structured response

# result = client.chat.completions.create(
#     model = "openai/gpt-oss-20b",
#     messages = [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant. Respond in JSON format."
#         },
#         {
#             "role": "user",
#             "content": "Give me the name, age and city of a fictional person."
#         }
#     ]
# )

# print(result.choices[0].message.content)
# print(type(result.choices[0].message.content))

## it works but we can use structured outputs to get a more robust structured response

## structured outputs with pydantic 
## when you pass response_format=Person, the SDK converts this class into a
## JSON schema and sends it to OpenAI's servers. The model is contrained
## at the server level to only return responses that match the schema.

class Person(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int
    city: str

result = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Respond in JSON format."
        },
        {
            "role": "user",
            "content": "Give me the name, age and city of a fictional person."
        }
    ],
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "user_details",
            "strict": True,
            "schema": Person.model_json_schema()
        }
    }
)

person = Person.model_validate_json(
result.choices[0].message.content
)
print(person)
print(person.name)
print(type(person.name))