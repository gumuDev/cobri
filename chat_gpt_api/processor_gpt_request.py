from openai import OpenAI
import json
import datetime
import os
import json

# Get the current directory path (where the main.py file is located)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the JSON file
json_file_path = os.path.join(current_dir, "prompts.json")

with open(json_file_path, "r") as file:
    prompts = json.load(file)

system_prompt = prompts["text_prompt"]

class ProcessorGptRequest:

    @staticmethod
    def get_json_from_prompt(message, client):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": system_prompt}],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{message}, fecha actual: {datetime.datetime.now().date()}",
                        }
                    ],
                },
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
