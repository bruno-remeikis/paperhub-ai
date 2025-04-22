from ai_connectors.ai_connector import AiConnector
from ai_connectors.googleai_connector import GoogleAiCoonnector

from utils.string_utils import StringBuilder


ai: AiConnector = GoogleAiCoonnector()


def ask(doc_content):
    sb = StringBuilder()
    sb.ln('O documento abaixo é uma produção acadêmico-científica.')
    sb.ln('Traga artigos científicos que tenham relação com o conteúdo da produção.')
    sb.ln('```html')
    sb.ln(doc_content)
    sb.ln('```')

    res = ai.ask(sb.toString())
    return res