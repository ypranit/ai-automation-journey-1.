def get_name():
    return input("What is your name? ").strip()


def start_message(name):
    return f"{name} is starting AI automation."


def main():
    name = get_name()
    if name == "":
        print("Please enter a name next time.")
    else:
        print(start_message(name))


main()


