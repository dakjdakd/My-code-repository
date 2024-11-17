from openai import OpenAI
client = OpenAI(
    api_key="AIzaSyCYcGaAYke3WQWfFGwiRgq0WaMRX6IAeJc",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


response = client.chat.completions.create(
    model="gemini-1.5-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "怎么成为亿万富翁"
        }
    ]
)

print(response.choices[0].message.content)