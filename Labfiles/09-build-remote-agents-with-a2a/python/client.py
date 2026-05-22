""" Client code that connects to the routing agent """

import os
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv()

server = os.environ["SERVER_URL"]
port = os.environ["ROUTING_AGENT_PORT"]

def send_prompt(prompt: str):
    url = f"http://{server}:{port}/message"
    payload = {"message": prompt}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response from agent.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Request failed: {e}"

async def main():
    print("Enter a prompt for the agent. Type 'quit' to exit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        response = send_prompt(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
