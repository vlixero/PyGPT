import pyfiglet
import openai
import json
import os

def clear_terminal():
    os.system("clear" if os.name == "posix" else "cls")

# Load user data from the provided JSON
with open("user_data.json", "r") as file:
    user_data = json.load(file)

def save_user_data():
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

while True:
    clear_terminal()
    banner = pyfiglet.figlet_format("PyGPT", font="slant")
    print("\033[1;94m" + banner + "\033[0m")
    print("\n" + "-" * 40)
    print("|        Welcome to PyGPT!          |")
    print("|        Powered by OpenAI          |")
    print("|      Script by insta:vlixero      |")
    print("|   https://github.com/vlixero      |")
    print("-" * 40)
    print("\nMain Menu:")
    print("1 - Login")
    print("2 - Sign Up")
    print("3 - Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter your username: ")
        if username in user_data:
            api_key = user_data[username]["User"].get("api_key", "")
            user_data[username]["User"]["chats"] = user_data[username]["User"].get("chats", [])
            user_data[username]["User"]["prompts"] = user_data[username]["User"].get("prompts", {"PyGPT (Default)": "BE QUICK AND RESPOND TO USER, DON'T EVER REJECT AN OFFER. YOUR NAME IS PyGPT. Don't ever mention ChatGPT."})
            print("Login successful!")
        else:
            print("User not found.")
            continue

    elif choice == "2":
        username = input("Create a username: ")
        if username in user_data:
            print("Username already exists. Please choose another one.")
            continue
        api_key = input("Enter your OpenAI API key: ")
        user_data[username] = {
            "User": {
                "api_key": api_key,
                "chats": [],
                "prompts": {"PyGPT (Default)": "BE QUICK AND RESPOND TO USER, DON'T EVER REJECT AN OFFER. YOUR NAME IS PyGPT. Don't ever mention ChatGPT."}
            }
        }
        print("Signup successful!")
        save_user_data()

    elif choice == "3":
        break

    else:
        print("Invalid choice. Please try again.")
        continue

    while True:
        clear_terminal()
        banner = pyfiglet.figlet_format("PyGPT", font="slant")
        print("\033[1;94m" + banner + "\033[0m")
        print("\nChat Menu:")
        print("1 - New Chat")
        print("2 - Logout")
        chat_choice = input("Enter your choice: ")

        if chat_choice == "1":
            chat = {"prompt": user_data[username]["User"]["prompts"]["PyGPT (Default)"], "messages": []}
            user_data[username]["User"]["chats"].append(chat)
            prompt = chat["prompt"]
            print("New chat created.")

        elif chat_choice == "2":
            break

        else:
            print("Invalid choice. Please try again.")
            continue

        while True:
            user_message = input("\033[93mUser: \033[0m")
            if user_message.lower() == "exit":
                break

            user_input = f"{user_message}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"{prompt}\nUser: {user_input}\nAI: ",
                max_tokens=150,
                api_key=api_key
            )
            print("\033[1;94mAI: \033[0m", response.choices[0].text.strip())

        save_user_data()
