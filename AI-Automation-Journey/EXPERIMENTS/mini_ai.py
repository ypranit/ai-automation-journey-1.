
print("WELCOME TO MINI AI")
print("------------------")

user = input("You: ")

if "hello" in user.lower():
    print("AI: Hey there!")

elif "your name" in user.lower():
    print("AI: I am your mini AI assistant.")

elif "motivate" in user.lower():
    print("AI: Keep building. Small progress daily becomes massive later.")

elif "python" in user.lower():
    print("AI: Python is one of the best languages for AI automation.")

else:
    print("AI: I don't understand that yet.")