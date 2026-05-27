import requests

username = input("Enter GitHub username: ")

url = f"https://api.github.com/users/{username}"

response = requests.get(url)

data = response.json()

print("\nGitHub User Info")
print("----------------")
print("Name:", data.get("name"))
print("Bio:", data.get("bio"))
print("Followers:", data.get("followers"))
print("Public Repos:", data.get("public_repos"))
print("Following:", data.get("following"))
print("Followers:", data.get("followers"))
print("Location:", data.get("location"))
print("Account Created:", data.get("created_at"))
print("Profile URL:", data.get("html_url")) 
