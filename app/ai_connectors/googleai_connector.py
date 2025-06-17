import google.generativeai as genai
import os
from ai_connectors.ai_connector import AiConnector


genai.configure(api_key=os.environ["GOOGLEAI_API_KEY"])
MODEL = "gemini-2.5-flash"


class GoogleAiCoonnector(AiConnector):
    def __init__(self, agent: str = None):
        self.model = genai.GenerativeModel(
            MODEL,
            system_instruction = agent,
            generation_config = {"response_mime_type": "application/json"}
        )

    def ask(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
