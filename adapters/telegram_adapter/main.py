from dotenv import load_dotenv
import os
import asyncio
import sys
import boto3

# Get the current directory path (where the main.py file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(current_dir, "../.."))

# Add the project root directory to sys.path
sys.path.insert(0, project_root)

# Now you can import without issues
from database.client_supabase import ClientSupabase

# Load the .env file
load_dotenv()

# Configure environment variables
bot_token = os.getenv('BOT_TOKEN_TELEGRAM')
queue_url = os.getenv('QUEUE_TELEGRAM')
region_aws = os.getenv('REGION_AWS')

async def receive_messages(client_supabase, sqs_client):
    response = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["All"],
            MaxNumberOfMessages=10,
            MessageAttributeNames=["All"],
            VisibilityTimeout=30,  # Ajusta el VisibilityTimeout a un valor adecuado
            WaitTimeSeconds=20,
        )
    
    messages = response.get("Messages", [])
    
    while True:
        if not messages:
            continue

        tasks = []
        for message in messages:
            print(message)

def main():
    client_supabase = ClientSupabase()
    sqs_client = boto3.client("sqs", region_name=region_aws)
    asyncio.run(receive_messages(client_supabase, sqs_client))

if __name__ == "__main__":
    main()
