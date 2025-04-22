from ai_connectors.ai_connector import AiConnector
from ai_connectors.googleai_connector import GoogleAiCoonnector

from utils.string_utils import StringBuilder

import json


ai: AiConnector = GoogleAiCoonnector()


def ask(doc_content):
    sb = StringBuilder()
    sb.ln('O documento abaixo é uma produção acadêmico-científica.')
    sb.ln('```html')
    sb.ln(doc_content)
    sb.ln('```')
    sb.ln('Traga artigos científicos que tenham relação com o conteúdo da produção, a fim de enriquecê-la.')
    sb.ln('Sua resposta deve ser uma lista JSON; Cada referência deve ser trazida no formato JSON com a seguinte configuração:')
    sb.ln('- Deve conter o campo "title", contendo o tídulo da referência')
    sb.ln('- Deve conter o campo "link", contendo o link da referência')
    sb.ln('- Deve conter o campo "suggestion", contendo uma sugestão de citação da referência')
    sb.ln('Sua resposta deve ser apenas o JSON plano. Não utilize quebras de linha ou "Fenced Code Blocks".')

    res = ai.ask(sb.toString())
    json_res = json.loads(res)
    return json_res