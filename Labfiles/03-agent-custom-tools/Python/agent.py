import os
import json
from dotenv import load_dotenv

# Add references


def main(): 
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Connect to the project client
    

        # Define the event function tool
        

        # Define the observation cost function tool
        

        # Define the observation report generation function tool
        

        # Create a new agent with the function tools
        
        
        # Create a thread for the chat session
        

        # Create a list to hold function call outputs that will be sent back as input to the agent
        
        
        while True:
            user_input = input("Enter a prompt for the astronomy agent. Use 'quit' to exit.\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("Exiting chat.")
                break

            # Send a prompt to the agent
           
        
            # Retrieve the agent's response, which may include function calls


            # Process function calls
            

            # Send function call outputs back to the model and retrieve a response
            

        # Delete the agent when done
        

if __name__ == '__main__': 
    main()