from dotenv import load_dotenv

import os
import asyncio
import sys

import json
from openai import OpenAI

# Get the current directory path (where the main.py file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(current_dir, "../.."))

# Add the project root directory to sys.path
sys.path.insert(0, project_root)

# Now you can import without issues
from database.client_supabase import ClientSupabase
from converters.telegram_message_converter import TelegramMessageConverter
from message_response import MessageResponse
from message_dispatcher import MessageDispatcher
from aws_sqs.aws_sqs_event import AwsSqsEvent
from models.message_response_tg import MessageResponseTG
# Load the .env file
load_dotenv()

# Configure environment variables
bot_token = os.getenv("BOT_TOKEN_TELEGRAM")
queue_url = os.getenv("QUEUE_TELEGRAM")
region_aws = os.getenv("REGION_AWS")
api_key_gpt = os.getenv("OPENAI_API_KEY")

async def receive_messages(sqs_client,
    telegram_message_converter: TelegramMessageConverter, message_response: MessageResponse,
    message_dispatcher: MessageDispatcher,
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
            phone_id = body_request["message"]["from"]["id"]

            if ("text" in body_request["message"]
                and "/start" == body_request["message"]["text"]):
                message_response.send_message("¡Bienvenido! este es un bot donde puedes registrar tus compras, ventas y pedir tus reportes..\n",
                                               phone_id)

                sqs_client.delete_message(message)

                continue
            try:
               message_tg = telegram_message_converter.convert_to_message(body_request, phone_id)
            except Exception as ex:
               sqs_client.delete_message(message)
               message_response.send_message(str(ex), phone_id)
               continue

            message_response.send_message("Estamos Procesando su informacion espere la respuesta Por favor!", phone_id)
            
            task = asyncio.create_task(
                message_dispatcher.message_dispatch(message_tg, client)
            )

            tasks.append(task)


            sqs_client.delete_message(message)

        await asyncio.gather(*tasks)


def main():
    client_supabase = ClientSupabase()
    aws_sqs_event = AwsSqsEvent(queue_url, region_aws)
    telegram_message_converter = TelegramMessageConverter()
    message_response = MessageResponse(bot_token)
    message_dispatcher = MessageDispatcher(message_response, aws_sqs_event, client_supabase)
    client = OpenAI(api_key=api_key_gpt)
    asyncio.run(
        receive_messages(aws_sqs_event, telegram_message_converter,
                        message_response, message_dispatcher, client)
    )

if __name__ == "__main__":
    main()
