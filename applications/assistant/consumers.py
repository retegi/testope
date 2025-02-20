import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AssistantConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Opcional: Manejar la desconexión
        pass

    async def receive(self, text_data):
        # Recibir datos del cliente
        data = json.loads(text_data)
        user_message = data.get('message', '')

        # Responder al cliente
        await self.send(json.dumps({
            'message': f"Recibí tu mensaje: {user_message}"
        }))
