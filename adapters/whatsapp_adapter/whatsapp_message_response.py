import requests
from string import Template


class WhatsappMessageResponse:

    def __init__(self, wa_token, phone_number_id) -> None:
        template_str = "- item: $item, cantidad: $quantity, precio: $price"
        self.wa_token = wa_token
        self.template = Template(template_str)
        self.phone_number_id = phone_number_id
        
    def generate_message(self, json_array, trans_type):
        trans_header_type = ''
        if (trans_type == 'purchase'):
            trans_header_type = "compras"
        else:
            trans_header_type = 'ventas'
            
        message_header = f"Tus {trans_header_type} son estas:\n"
        messages = []
        for item in json_array:
            message = self.template.substitute(
                item=item['item'],
                quantity=item['quantity'],
                price=item['price']
            )
            messages.append(message)
        return message_header + "\n".join(messages)

    def send_message(self, message_response, chat_id):
        url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.wa_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": chat_id,
            "type": "text",
            "text": {"body": message_response},
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Mensaje enviado con éxito:", response.json())
        else:
            print("Error al enviar el mensaje:", response.status_code, response.json())
