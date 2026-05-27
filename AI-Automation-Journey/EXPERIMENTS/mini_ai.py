import requests

print("WELCOME TO MINI AI")
print("Type 'bye' to exit.")
print("------------------")

while True:

    user = input("You: ")

    if "hello" in user.lower():
        print("AI: Hey there!")

    elif "your name" in user.lower():
        print("AI: I am your mini AI assistant.")

    elif "motivate" in user.lower():

        url = "https://zenquotes.io/api/random"

        response = requests.get(url)

        data = response.json()

        print("\nAI Motivation")
        print(data[0]["q"])
        print("- ", data[0]["a"])

    elif "python" in user.lower():
        print("AI: Python is one of the best languages for AI automation.")

    elif "bye" in user.lower():
        print("AI: Goodbye!")
        break

    else:
        print("AI: I don't understand that yet.")