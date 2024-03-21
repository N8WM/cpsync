"""Set up the environment file"""

import sys

if __name__ == "__main__":
    ans = ""
    accepted = ["y", "n", "yes", "no"]
    while ans.lower() not in accepted:
        ans = input("This will overwrite any existing .env file. Continue? (y/n) ")
    if ans.lower() == "n":
        print("Exiting...")
        sys.exit(0)
    try:
        with open(".env", "w") as file:
            openai_api_key = input("\nEnter your OpenAI API key:\n")
            file.write(f'OPENAI_API_KEY="{openai_api_key}"\n')
            discord_token = input("\nEnter your Discord bot's token (Bot tab):\n")
            file.write(f'DISCORD_TOKEN="{discord_token}"\n')
            discord_client_id = input(
                "\nEnter your Discord bot's client ID (OAuth2 tab):\n"
            )
            file.write(f'CLIENT_ID="{discord_client_id}"\n')
            print("\n.env file created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    sys.exit(0)
