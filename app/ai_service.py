# from pydantic import BaseModel

from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
# from agno.tools.postgres import PostgresTools
# from agno.utils.pprint import pprint_run_response

import json

from models.requests.AskRequest import AskRequest
from models.AiResponse import AiResponse


def load_instructions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


agent = Agent(
    model=Gemini(id="gemini-2.5-pro", api_key='AIzaSyDtJ5cHO87nH_2AxWpqk-KEV68k3UpbKGw'),
    instructions=load_instructions('instructions/main-agent.md'),
    # Memory
    add_history_to_messages=True,
    enable_agentic_memory=True,
    enable_session_summaries=True,
    # RAG
    add_references=True,
    search_knowledge=True,
    # Response structure
    use_json_mode=True,
    response_model=AiResponse,
    # Debug
    #debug_mode=True
)


def ask(req: AskRequest):
    res = agent.run(req.model_dump_json())
    # return json.loads(res)
    return res