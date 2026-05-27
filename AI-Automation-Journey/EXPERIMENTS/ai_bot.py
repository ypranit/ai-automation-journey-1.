from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY"
)

messages = [

    {
        "role": "system",
        "content": (
            "You are a smart AI mentor helping a beginner "
            "learn Python, AI automation, APIs, and software development. "
            "Explain things simply and motivate the user."
        )
    }

]

print("WELCOME TO AI CHAT")
print("Type 'bye' to exit.")
print("--------------------")

while True:

    user = input("\nYou: ")

    if user.lower() == "bye":
        print("AI: Goodbye!")
        break

    messages.append(
        {"role": "user", "content": user}
    )

    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages
    )

    reply = completion.choices[0].message.content

    messages.append(
        {"role": "assistant", "content": reply}
    )

    print("\nAI:")
    print(reply)