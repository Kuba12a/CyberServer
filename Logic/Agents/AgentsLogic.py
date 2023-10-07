from typing import List
from cryptography.fernet import Fernet
from pydantic import BaseModel
import Gateways.WebSocketCybClientGateway as webSocketCybClientGateway
import Db.Agents.AgentRepository as agentRepository
from Db.Agents.Agent import Agent, Status
from Utils.Exceptions.LogicException import LogicException
from Utils import StringUtils


class AddAgentInputType(BaseModel):
    ip_address: str


class ConnectAgentInputType(BaseModel):
    ip_address: str


class DisconnectAgentInputType(BaseModel):
    ip_address: str


def add_agent(input: AddAgentInputType):
    agent = get_agent_by_ip_address(input.ip_address)

    if agent is not None:
        raise LogicException('Agent with given ip address already exists')

    key = Fernet.generate_key()
    cookie = StringUtils.generate_random_string(20)
    return agentRepository.insert_agent(agentRepository
                                        .AgentInsertInputType(ip_address=input.ip_address, encryption_key=key,
                                                              cookie=cookie, status=Status.ADDED.name.lower()))


def connect_agent(input: ConnectAgentInputType):
    agent = get_agent_by_ip_address(input.ip_address)
    if agent is None:
        webSocketCybClientGateway.send_message(f'Agent {input.ip_address} requested to be connected but was not found')
        return None
    return agentRepository.update_agent(agentRepository
                                        .AgentUpdateStatusType(ip_address=agent.ip_address,
                                                               status=Status.CONNECTED.name.lower()))


def disconnect_agent(input: DisconnectAgentInputType):
    agentRepository.update_agent(agentRepository.AgentUpdateStatusType(ip_address=input.ip_address,
                                                                       status=Status.ADDED.name.lower()))


def get_agent_by_id(id: int) -> Agent:
    return agentRepository.get_agent_by_id(id)


def get_agent_by_ip_address(ip_address: str) -> Agent:
    return agentRepository.get_agent_by_ip_address(ip_address)


def list_agents(status: Status = None) -> List[Agent]:
    if status is not None:
        return agentRepository.list_agents(status.name.lower())

    return agentRepository.list_agents()
