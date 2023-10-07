from typing import List, Optional
from pydantic import BaseModel
import Db.DbManager as dbManager
from Db.Agents.Agent import Agent, Status


class AgentInsertInputType(BaseModel):
    ip_address: str
    encryption_key: str
    cookie: str
    status: str


class AgentUpdateStatusType(BaseModel):
    ip_address: str
    status: str


def insert_agent(agent: AgentInsertInputType):
    try:
        conn = dbManager.connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO agents (ip_address, encryption_key, cookie, status) VALUES(?, ?, ?, ?)",
                    (agent.ip_address, agent.encryption_key, agent.cookie, agent.status))
        conn.commit()
        agent_id = cur.lastrowid
    except:
        conn().rollback()
    finally:
        conn.close()

    return agent_id


def update_agent(agent: AgentUpdateStatusType):
    try:
        conn = dbManager.connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE agents SET status = ? WHERE ip_address = ?",
                    (agent.status, agent.ip_address))
        conn.commit()
        agent_id = cur.lastrowid
    except:
        conn().rollback()
    finally:
        conn.close()

    return agent_id


def set_all_agents_status_added():
    try:
        conn = dbManager.connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE agents SET status = 'added'")
        conn.commit()
    except:
        conn().rollback()
    finally:
        conn.close()


def get_agent_by_id(id: int) -> Optional[Agent]:
    try:
        conn = dbManager.connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * from agents WHERE id = ?", str(id))
        agent = cur.fetchone()
    finally:
        conn.close()

    if agent is None:
        return None

    return Agent(id=agent['id'], ip_address=agent['ip_address'], created_at=agent['created_at'],
                 encryption_key=agent['encryption_key'], cookie=agent['cookie'], status=agent['status'])


def get_agent_by_ip_address(ip_address: str) -> Optional[Agent]:
    try:
        conn = dbManager.connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * from agents WHERE ip_address = ?", (ip_address,))
        agent = cur.fetchone()
    finally:
        conn.close()

    if agent is None:
        return None

    return Agent(id=agent['id'], ip_address=agent['ip_address'], created_at=agent['created_at'],
                 encryption_key=agent['encryption_key'], cookie=agent['cookie'], status=Status[agent['status'].upper()])


def list_agents(status: str = None) -> List[Agent]:
    try:
        conn = dbManager.connect_to_db()
        cur = conn.cursor()
        if status is not None:
            sql = "SELECT * from agents WHERE status = ?"
            cur.execute(sql, (status,))
        else:
            sql = "SELECT * from agents"
            cur.execute(sql)
        results = cur.fetchall()
    finally:
        conn.close()

    agents_map = map(lambda a: Agent(id=a['id'], ip_address=a['ip_address'], created_at=a['created_at'],
                                     encryption_key=a['encryption_key'], cookie=a['cookie'], status=Status[a['status'].upper()]), results)

    return list(agents_map)


