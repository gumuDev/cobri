import requests
from string import Template
import re


class MessageResponse:

    def __init__(self, bot_token):
        template_str = "- item: $item, cantidad: $quantity, precio: $price"
        self.bot_token = bot_token
        self.template = Template(template_str)

    def generate_message(self, json_array, trans_type):
        trans_header_type = ""
        if trans_type == "purchase":
            trans_header_type = "compras"
        else:
            trans_header_type = "ventas"

        message_header = f"Tus {trans_header_type} son estas:\n"
        messages = []
        for item in json_array:
            message = self.template.substitute(
                item=item["item"], quantity=item["quantity"], price=item["price"]
            )
            messages.append(message)
        return message_header + "\n".join(messages)

    def send_message(self, message_response, phone_id):
        message = self.conditional_escape_markdown_v2(message_response)
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": phone_id,
            "text": message,
            "parse_mode": "MarkdownV2",
        }
        requests.post(url, json=payload)

    def conditional_escape_markdown_v2(self, text):
       # Detecta bloques de enlaces y no los modifica
       link_pattern = re.compile(r'\[.*?\]\(.*?\)')
       matches = link_pattern.findall(text)
       
       # Escapar solo lo que no es un enlace o formato especial
       def escape_outside_links(match):
           segment = match.group(0)
           if segment in matches:
               return segment  # Devolver tal cual si ya está formateado
           # Escapar los caracteres especiales
           return re.sub(r'([_\*\[\]\(\)~`>\#\+\-\=\|\{\}\.\!])', r'\\\1', segment)
       
       # Aplicar el escape solo a las partes que no son enlaces o formatos
       return re.sub(r'[^[]+|(\[.*?\]\(.*?\))', escape_outside_links, text)
