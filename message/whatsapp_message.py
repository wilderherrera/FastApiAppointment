import requests

import models.models
import settings


class WhatsappMessage:
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'AccessKey {settings.WHATSAPP_API_KEY}',
        }

    def get_body(self, client, template_name, variables):
        return {
            'to': "+57" + client.cellphone,
            'channelId': settings.WHATSAPP_CHANNEL_ID,
            'type': 'hsm',
            'content': {
                'hsm': {
                    'namespace': settings.WHATSAPP_NAMESPACE,
                    'templateName': template_name,
                    'language': {
                        'policy': 'deterministic',
                        'code': 'es',
                    },
                    'params': [{"default": name} for name in variables],
                },
            },
        }

    def send(self, client: models.models.Client, template_name, variables: list):
        response = requests.post(
            settings.WHATSAPP_START_CONVERSATION_URL,
            json=self.get_body(client, template_name, variables),
            headers=self.get_headers()
        )
        print(response.json())
