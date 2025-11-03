import os

from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb

from app.models.AiResponse import AiResponse
from app.models.requests.AskRequest import AskRequest


def load_instructions(file_path):
    # Convert relative path to absolute path based on this file's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(base_dir, file_path)
    
    with open(absolute_path, "r", encoding="utf-8") as file:
        return file.read()

db = SqliteDb(
    db_file="temp/agno_app.db",
    knowledge_table="knowledge_contents",
)


google_api_key = os.getenv("GOOGLE_API_KEY")

agent = Agent(
    model=Gemini(id="gemini-2.5-pro", api_key=google_api_key),
    instructions=load_instructions("instructions/main-agent.md"),  # Removed leading './'
    # Database
    db=db,
    # History
    add_history_to_context=True,
    # Memory
    enable_user_memories=True,
    enable_session_summaries=True,
    output_schema=AiResponse,
    use_json_mode=True,
)


def ask(req: AskRequest):
    res = agent.run(req.model_dump_json())
    return res.content
