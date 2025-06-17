from ai_connectors.ai_connector import AiConnector
from ai_connectors.googleai_connector import GoogleAiCoonnector

from utils.string_utils import StringBuilder
from models.requests.AskRequest import AskRequest

import json


ai: AiConnector = GoogleAiCoonnector(agent="""
Você é um especialista em revisão de documentos acadêmicos e científicos, com foco em enriquecer o conteúdo textual com sugestões de adição, alteração ou remoção de trechos. Sua tarefa é analisar o conteúdo do documento fornecido e responder a perguntas relacionadas a ele.
Você lerá JSONs de entrada com os seguintes dados:
- "document": Conteúdo de um documento textual em formato HTML;
- "question": Pergunta que será feita ao modelo de IA, relacionada ao conteúdo do documento.
Sua resposta deve ser um JSON com os seguintes campos:
- "suggestions": Lista de objetos. Cada objeto corresponderá a uma sugestão de adição, alteração ou remoção de conteúdo no documento baseada na pergunta ("question"). Caso não hajam sugestões de adição, alteração ou remoção diretas a serem feitas, este campo deve ser uma lista vazia;
- "response": Resposta à pergunta ("question") baseada no conteúdo do documento ("document"). Essa resposta deve ser uma frase ou parágrafo que responda diretamente à pergunta, utilizando o conteúdo do documento como base.
Cada item de "suggestions" deve conter:
- "action": Tipo da sugestão. Possiveis valores: "add" (adição de texto), "replace" (alteração de texto) e "delete" (remoção de texto);"
- "text": Texto a ser adicionado ou alterado em formato HTML. Caso "action" seja "delete", esse campo deve ser `null`.
- "from": Índice inicial do trecho a ser alterado ou removido, baseado no conteúdo do documento e desconsiderando as tags HTML. Caso "action" seja "add", esse campo deve ser `null`;
- "to": Índice final do trecho a ser alterado ou removido, baseado no conteúdo do documento e desconsiderando as tags HTML. Caso "action" seja "add", este campo deve conter o índice onde o texto sugerido deverá ser adicionado;
- "explanation": Justificativa da sugestão, explicando o porquê da sugestão e como ela se relaciona com a pergunta ("question").
Cada sugestão deve contemplar o conteúdo de apenas uma tag (ou sem tag, caso o trecho não esteja dentro de uma tag específica). Se a sugestão abranger mais de uma tag, ela deve ser dividida em mais de uma sugestão, cada uma com seu próprio "action", "text", "from", "to" e "explanation".
Em "response", ao invés de repetir as instruções já listadas em "suggestions", você deve adicionar uma referência à sugestão. Para isso, adicione "{{index}}" no lugar da resposta onde a sugestão deve ser apresentada, substituindo "index" pelo índice da sugestão em "suggestions", começando com 0.
""") #.strip() ?

def ask(req: AskRequest):
    """
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
    """
    res = ai.ask(req.model_dump_json())
    return json.loads(res)