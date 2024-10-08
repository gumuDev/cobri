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

class ProcessorGptRequest:
    def __init__(self) -> None:
        self.transaction_prompt_services = {
            'purchases': prompts["text_prompt_purchase"],
            'sell':  prompts["text_prompt_sell"],
            'report': prompts["text_prompt_report"]
        }

    def get_json_from_prompt(self, message, client, response_type):

        if(isinstance(response_type, list)):
            prompt = self.transaction_prompt_services.get(response_type[0])
        else:
            prompt = self.transaction_prompt_services.get(response_type)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": prompt}],
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
