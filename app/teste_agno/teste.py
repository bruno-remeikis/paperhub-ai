# """
# source venv/bin/activate
# venv/bin/python3 app/teste_agno/teste.py
# """

# from pydantic import BaseModel

# from agno.agent import Agent, RunResponse
# from agno.models.google import Gemini
# # from agno.tools.postgres import PostgresTools
# from agno.utils.pprint import pprint_run_response

# class ResponseStructure(BaseModel):
#     answer: str

# agent = Agent(
#     model=Gemini(id="gemini-2.5-pro", api_key='AIzaSyDtJ5cHO87nH_2AxWpqk-KEV68k3UpbKGw'),
#     instructions="Você é um pato. Responda como um pato responderia",
#     # Memory
#     add_history_to_messages=True,
#     enable_agentic_memory=True,
#     enable_session_summaries=True,
#     # RAG
#     add_references=True,
#     search_knowledge=True,
#     # Response structure
#     use_json_mode=True,
#     response_model=ResponseStructure,
#     # Debug
#     #debug_mode=True
# )

# while (True):
#     question = input('Pergunte à IA: ')
#     if question.lower() == 'sair' or question.lower() == 'exit':
#         break
#     response: RunResponse = agent.run(question)
#     pprint_run_response(response, markdown=True)
