import requests

print("WELCOME TO QUOTE MACHINE")
print("------------------------")

for i in range(5):

    url = "https://zenquotes.io/api/random"

    response = requests.get(url)

    data = response.json()

    print("\nQuote", i + 1)
    print("Quote:", data[0]["q"])
    print("Author:", data[0]["a"])
    print("------------------------")