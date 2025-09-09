# """
# source venv/bin/activate
# venv/bin/python3 app/teste_agno/teste.py
# """

# from pydantic import BaseModel

# from agno.agent import Agent, RunResponse
# from agno.models.google import Gemini
# from agno.tools import tool
# # from agno.tools.postgres import PostgresTools
# from agno.utils.pprint import pprint_run_response

# from typing import List, Dict, Optional


# class ResponseStructure(BaseModel):
#     answer: str


# @tool
# def _search_google_scholar(query: str, max_results: int = 5) -> List[Dict[str, str]]:
#     print()


# agent = Agent(
#     model=Gemini(id="gemini-2.5-pro", api_key='AIzaSyDtJ5cHO87nH_2AxWpqk-KEV68k3UpbKGw'),
#     #instructions="Você é um pato. Responda como um pato responderia",
#     tools=[
#         # self.extract_document_content,
#         # self.identify_key_concepts,
#         # self.search_google_scholar,
#         # self.analyze_relevance,
#         # self.format_references
#         _search_google_scholar
#     ],
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
