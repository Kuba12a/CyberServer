from fastapi import FastAPI
import API.AgentAPI as agentAPI
import API.InternalAPI as internalAPI


app = FastAPI()

app.include_router(agentAPI.router)
app.include_router(internalAPI.router)
