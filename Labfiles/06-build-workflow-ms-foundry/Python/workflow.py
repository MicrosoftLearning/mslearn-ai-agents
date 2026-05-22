import os, json, re
from dotenv import load_dotenv

# Add references


def print_workflow_output(output_text):
    tickets = re.findall(r"(\{.*?\})(.*?)(?=\{|$)", output_text, re.DOTALL)

    if not tickets:
        print(output_text)
        return

    for ticket_number, (ticket_json, response_text) in enumerate(tickets, start=1):
        ticket = json.loads(ticket_json)

        print("\n" + "=" * 80)
        print(f"Ticket {ticket_number}: {ticket['category']} ({ticket['confidence']:.0%} confidence)")
        print("-" * 80)
        print(f"Issue: {ticket['customer_issue']}")
        print("\nResponse:")
        print(response_text.strip())
    print("=" * 80 + "\n")

load_dotenv()
endpoint = os.environ["PROJECT_ENDPOINT"]

# Connect to the AI Project client


    # Specify the workflow
    

    # Create a conversation and run the workflow


    # Process events from the workflow run
 

    # Clean up resources

