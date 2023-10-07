import uvicorn
import config
from API.API import app
import Db.DbManager as dbManager
import Db.Agents.AgentRepository as agentRepository


if __name__ == '__main__':
    dbManager.setup_database()
    agentRepository.set_all_agents_status_added()
    uvicorn.run(app, port=config.server_port, host=config.server_ip)
