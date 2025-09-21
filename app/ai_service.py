from agno.agent import Agent
from agno.models.google import Gemini
# from agno.knowledge.knowledge import Knowledge
from agno.db.sqlite import SqliteDb
# from agno.db.postgres.postgres import PostgresDb
from agno.vectordb.pgvector import PgVector


# from agno.tools.postgres import PostgresTools
# from agno.utils.pprint import pprint_run_response

from models.requests.AskRequest import AskRequest
from models.AiResponse import AiResponse


def load_instructions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


db = SqliteDb(
    db_file="temp/agno_app.db",
    knowledge_table="knowledge_contents",
)

# knowledge = Knowledge(
#     name="Basic SDK Knowledge Base",
#     description="Agno 2.0 Knowledge Implementation",
#     contents_db=db,
#     # vector_db=PgVector(
#     #     table_name="vectors", db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"
#     # ),
# )

agent = Agent(
    model=Gemini(id="gemini-2.5-pro", api_key='AIzaSyDtJ5cHO87nH_2AxWpqk-KEV68k3UpbKGw'),
    instructions=load_instructions('instructions/main-agent.md'),
    
    # Database
    db=db,
    
    # History
    add_history_to_context=True,

    # Memory
    enable_user_memories=True,

    # Session settings
    enable_session_summaries=True,
    
    # RAG
    #!add_references=True,
    #!search_knowledge=True,
    #knowledge=knowledge,

    # Response Structure
    output_schema=AiResponse,
    use_json_mode=True,

    # Debug
    #debug_mode=True
)


def ask(req: AskRequest):
    res = agent.run(req.model_dump_json())
    return res.content