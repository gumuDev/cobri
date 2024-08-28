from dotenv import load_dotenv
import json
import os
import asyncio
import sys
from openai import OpenAI

# Get the current directory path (where the main.py file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(current_dir, "../.."))

# Add the project root directory to sys.path
sys.path.insert(0, project_root)

from aws_sqs.aws_sqs_event import AwsSqsEvent
from converters.whatsapp_message_converter import WhatsappMessageConverter
from whatsapp_message_response import WhatsappMessageResponse
from message_dispatcher import MessageDispatcher
from database.client_supabase import ClientSupabase

# Load the .env file
load_dotenv()

# Configure environment variables
queue_url = os.getenv("QUEUE_WHATSAPP")
region_aws = os.getenv("REGION_AWS")
wa_token = os.getenv("WHATSAPP_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")
api_key_gpt = os.getenv("OPENAI_API_KEY")


async def receive_messages(sqs_client, whatsapp_message_converter, message_response, message_dispatcher,
    client
):
    while True:
        response = sqs_client.receive_message()
        messages = response.get("Messages", [])

        if not messages:
            continue

        tasks = []
        for message in messages:
            body_request = json.loads(message["Body"])

            if "statuses" in body_request["entry"][0]["changes"][0]["value"]:
                sqs_client.delete_message(message)
                continue

            phone_id = body_request["entry"][0]["changes"][0]["value"]["contacts"][0][
                "wa_id"
            ]

            try:
                message_tg = whatsapp_message_converter.convert_to_message(
                    body_request["entry"][0]["changes"][0]["value"]["messages"][0],
                    phone_id,
                )
            except Exception as ex:
                sqs_client.delete_message(message)
                message_response.send_message(str(ex), phone_id)
                continue

            message_response.send_message(
                "Estamos Procesando su informacion espere la respuesta Por favor!",
                phone_id,
            )

            task = asyncio.create_task(
                message_dispatcher.message_dispatch(message_tg, client)
            )

            tasks.append(task)

            sqs_client.delete_message(message)
        await asyncio.gather(*tasks)


def main():
    client_supabase = ClientSupabase()
    sqs_client = AwsSqsEvent(queue_url, region_aws)
    whatsapp_message_converter = WhatsappMessageConverter()
    whatsapp_message_response = WhatsappMessageResponse(wa_token, phone_number_id)
    message_dispatcher = MessageDispatcher(
        whatsapp_message_response, sqs_client, client_supabase
    )
    client = OpenAI(api_key=api_key_gpt)

    asyncio.run(
        receive_messages(
            sqs_client,
            whatsapp_message_converter,
            whatsapp_message_response,
            message_dispatcher,
            client
        )
    )


if __name__ == "__main__":
    main()
