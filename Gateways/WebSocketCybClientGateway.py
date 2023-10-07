import websockets
import config


async def send_message(message: str):
    async with websockets.connect(f'ws://{config.client_web_socket_ip}:{config.client_web_socket_port}') as web_socket:
        await web_socket.send(message)
        print('message sent')
