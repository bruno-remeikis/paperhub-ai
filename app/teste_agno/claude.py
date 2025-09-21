# """
# Serviço de Revisão de Documentos Acadêmicos usando Agno
# Resolve problemas de: documentos longos, perda de contexto e ações globais
# """

# import json
# import re
# from typing import List, Dict, Any, Optional, Tuple
# from dataclasses import dataclass, asdict
# from enum import Enum
# import hashlib
# from bs4 import BeautifulSoup
# import math

# # Assumindo que o Agno está instalado - estrutura baseada na documentação
# from agno.agent import Agent
# from agno.models.openai import OpenAIChat
# from agno.storage.postgres import PostgresKnowledgeBase
# from agno.tools import Tool


# class ProcessingStrategy(Enum):
#     SINGLE_PASS = "single_pass"
#     CHUNKED = "chunked" 
#     HIERARCHICAL = "hierarchical"


# @dataclass
# class DocumentChunk:
#     """Representa um chunk do documento com metadados"""
#     id: str
#     content: str
#     position: int
#     section_title: str
#     context_summary: str
#     word_count: int
    
    
# @dataclass
# class DocumentContext:
#     """Contexto global do documento"""
#     title: str
#     abstract: str
#     sections: List[str]
#     main_topics: List[str]
#     writing_style: str
#     academic_level: str
#     total_words: int
    

# @dataclass
# class Suggestion:
#     """Sugestão de alteração no documento"""
#     change: str
#     explanation: str
#     chunk_id: Optional[str] = None
#     global_action: bool = False
    

# @dataclass
# class ProcessingResult:
#     """Resultado final do processamento"""
#     suggestions: List[Suggestion]
#     answer: str
#     modified_document: str
#     strategy_used: ProcessingStrategy
#     cost_estimate: float


# class DocumentAnalyzer:
#     """Analisa documentos e determina estratégia de processamento"""
    
#     # Limites para estratégias (em caracteres)
#     SINGLE_PASS_LIMIT = 15000  # ~4000 tokens
#     CHUNK_SIZE = 8000  # ~2000 tokens por chunk
#     OVERLAP_SIZE = 1000  # Overlap entre chunks
    
#     def __init__(self):
#         self.model = OpenAIChat(id="gpt-4o-mini")  # Modelo barato para análise
        
#     def analyze_document(self, html_content: str) -> Tuple[ProcessingStrategy, DocumentContext]:
#         """Analisa documento e determina estratégia de processamento"""
        
#         # Parse HTML para análise
#         soup = BeautifulSoup(html_content, 'html.parser')
#         text_content = soup.get_text()
        
#         char_count = len(html_content)
#         word_count = len(text_content.split())
        
#         # Extrai informações estruturais
#         sections = self._extract_sections(soup)
#         context = self._extract_context(soup, text_content)
        
#         # Determina estratégia baseada no tamanho
#         if char_count <= self.SINGLE_PASS_LIMIT:
#             strategy = ProcessingStrategy.SINGLE_PASS
#         elif char_count <= 100000:  # ~25k tokens
#             strategy = ProcessingStrategy.CHUNKED
#         else:
#             strategy = ProcessingStrategy.HIERARCHICAL
            
#         return strategy, DocumentContext(
#             title=self._extract_title(soup),
#             abstract=self._extract_abstract(soup),
#             sections=sections,
#             main_topics=context['topics'],
#             writing_style=context['style'],
#             academic_level=context['level'],
#             total_words=word_count
#         )
    
#     def create_chunks(self, html_content: str, context: DocumentContext) -> List[DocumentChunk]:
#         """Cria chunks inteligentes do documento"""
        
#         soup = BeautifulSoup(html_content, 'html.parser')
#         chunks = []
        
#         # Primeira tentativa: dividir por seções
#         sections = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
#         if len(sections) > 1:
#             chunks = self._chunk_by_sections(soup, sections, context)
#         else:
#             chunks = self._chunk_by_size(html_content, context)
            
#         return chunks
    
#     def _extract_sections(self, soup: BeautifulSoup) -> List[str]:
#         """Extrai títulos de seções do documento"""
#         headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
#         return [h.get_text().strip() for h in headers]
    
#     def _extract_context(self, soup: BeautifulSoup, text: str) -> Dict[str, Any]:
#         """Extrai contexto semântico do documento usando IA"""
        
#         # Usa apenas os primeiros 2000 caracteres para análise de contexto
#         sample_text = text[:2000]
        
#         prompt = f"""
#         Analise este trecho de documento acadêmico e retorne um JSON com:
#         {{
#             "topics": ["tópico1", "tópico2", ...],
#             "style": "formal/informal/técnico",
#             "level": "graduação/pós-graduação/pesquisa"
#         }}
        
#         Texto: {sample_text}
#         """
        
#         try:
#             # Simulação - em produção usar o agente Agno
#             return {
#                 "topics": ["tema principal", "metodologia"],
#                 "style": "formal",
#                 "level": "pós-graduação"
#             }
#         except:
#             return {
#                 "topics": ["análise acadêmica"],
#                 "style": "formal", 
#                 "level": "graduação"
#             }
    
#     def _extract_title(self, soup: BeautifulSoup) -> str:
#         """Extrai título do documento"""
#         title_elem = soup.find('title') or soup.find('h1')
#         return title_elem.get_text().strip() if title_elem else "Documento Acadêmico"
    
#     def _extract_abstract(self, soup: BeautifulSoup) -> str:
#         """Extrai resumo/abstract do documento"""
#         # Procura por elementos que possam ser o abstract
#         abstract_candidates = soup.find_all(['div', 'section', 'p'], 
#                                           class_=lambda x: x and ('abstract' in x.lower() or 'resumo' in x.lower()))
        
#         if abstract_candidates:
#             return abstract_candidates[0].get_text().strip()[:500]
        
#         # Fallback: primeiros parágrafos
#         paragraphs = soup.find_all('p')[:3]
#         return ' '.join([p.get_text().strip() for p in paragraphs])[:500]
    
#     def _chunk_by_sections(self, soup: BeautifulSoup, sections: List, context: DocumentContext) -> List[DocumentChunk]:
#         """Divide documento por seções lógicas"""
#         chunks = []
        
#         for i, section in enumerate(sections):
#             # Encontra conteúdo da seção até a próxima
#             section_content = self._extract_section_content(soup, section, 
#                                                            sections[i+1] if i+1 < len(sections) else None)
            
#             if len(section_content) > self.CHUNK_SIZE:
#                 # Se seção muito grande, divide em sub-chunks
#                 sub_chunks = self._split_large_section(section_content, section.get_text().strip())
#                 chunks.extend(sub_chunks)
#             else:
#                 chunk = DocumentChunk(
#                     id=f"section_{i}",
#                     content=section_content,
#                     position=i,
#                     section_title=section.get_text().strip(),
#                     context_summary=self._create_context_summary(context, section.get_text()),
#                     word_count=len(section_content.split())
#                 )
#                 chunks.append(chunk)
                
#         return chunks
    
#     def _chunk_by_size(self, html_content: str, context: DocumentContext) -> List[DocumentChunk]:
#         """Divide documento por tamanho com overlap inteligente"""
#         chunks = []
        
#         # Divide mantendo tags HTML íntegras
#         soup = BeautifulSoup(html_content, 'html.parser')
#         paragraphs = soup.find_all(['p', 'div', 'section'])
        
#         current_chunk = ""
#         chunk_paras = []
        
#         for i, para in enumerate(paragraphs):
#             para_html = str(para)
            
#             if len(current_chunk + para_html) > self.CHUNK_SIZE and current_chunk:
#                 # Cria chunk atual
#                 chunk = DocumentChunk(
#                     id=f"chunk_{len(chunks)}",
#                     content=current_chunk,
#                     position=len(chunks),
#                     section_title=f"Seção {len(chunks)+1}",
#                     context_summary=self._create_context_summary(context, current_chunk[:200]),
#                     word_count=len(current_chunk.split())
#                 )
#                 chunks.append(chunk)
                
#                 # Inicia novo chunk com overlap
#                 overlap_paras = chunk_paras[-2:] if len(chunk_paras) >= 2 else chunk_paras
#                 current_chunk = ''.join([str(p) for p in overlap_paras])
#                 chunk_paras = overlap_paras.copy()
            
#             current_chunk += para_html
#             chunk_paras.append(para)
        
#         # Adiciona último chunk
#         if current_chunk:
#             chunk = DocumentChunk(
#                 id=f"chunk_{len(chunks)}",
#                 content=current_chunk,
#                 position=len(chunks),
#                 section_title=f"Seção {len(chunks)+1}",
#                 context_summary=self._create_context_summary(context, current_chunk[:200]),
#                 word_count=len(current_chunk.split())
#             )
#             chunks.append(chunk)
            
#         return chunks
    
#     def _extract_section_content(self, soup: BeautifulSoup, current_section, next_section) -> str:
#         """Extrai conteúdo entre duas seções"""
#         # Implementação simplificada - pega todos os elementos até a próxima seção
#         content_elements = []
#         current = current_section.next_sibling
        
#         while current and current != next_section:
#             if hasattr(current, 'name') and current.name:
#                 content_elements.append(str(current))
#             current = current.next_sibling
            
#         return ''.join(content_elements)
    
#     def _split_large_section(self, content: str, section_title: str) -> List[DocumentChunk]:
#         """Divide seção muito grande em sub-chunks"""
#         # Implementação similar ao _chunk_by_size
#         return []  # Simplificado para exemplo
    
#     def _create_context_summary(self, context: DocumentContext, sample_text: str) -> str:
#         """Cria resumo do contexto para o chunk"""
#         return f"Documento: {context.title}. Tópicos: {', '.join(context.main_topics[:3])}. Estilo: {context.writing_style}."


# class AcademicDocumentService:
#     """Serviço principal de revisão de documentos acadêmicos"""
    
#     def __init__(self, openai_api_key: str, postgres_config: Dict[str, Any]):
#         self.analyzer = DocumentAnalyzer()
        
#         # Base de conhecimento compartilhada
#         self.knowledge_base = PostgresKnowledgeBase(
#             host=postgres_config["host"],
#             port=postgres_config["port"],
#             user=postgres_config["user"],
#             password=postgres_config["password"],
#             database=postgres_config["database"]
#         )
        
#         # Agentes especializados
#         self._setup_agents(openai_api_key)
        
#     def _setup_agents(self, api_key: str):
#         """Configura os agentes especializados"""
        
#         # Agente para análise de contexto global
#         self.context_agent = Agent(
#             name="DocumentContextAnalyzer",
#             model=OpenAIChat(id="gpt-4o-mini", api_key=api_key),
#             instructions="""
#             Você é especialista em analisar contexto global de documentos acadêmicos.
#             Extraia informações estruturais, temáticas e estilísticas.
#             Retorne sempre JSON válido com contexto resumido.
#             """,
#             knowledge=self.knowledge_base,
#             memory=True
#         )
        
#         # Agente revisor principal - focado no documento original
#         self.main_reviewer = Agent(
#             name="AcademicReviewer",
#             model=OpenAIChat(id="gpt-4o", api_key=api_key),
#             instructions=self._get_reviewer_instructions(),
#             knowledge=self.knowledge_base,
#             memory=True,
#             response_format="json"
#         )
        
#         # Agente para ações globais (substituições em massa)
#         self.global_action_agent = Agent(
#             name="GlobalActionProcessor",
#             model=OpenAIChat(id="gpt-4o", api_key=api_key),
#             instructions="""
#             Você processa ações globais em documentos acadêmicos (substituições, correções em massa).
#             Mantém formatação HTML e estrutura do documento.
#             Retorna documento modificado completo.
#             """,
#             knowledge=self.knowledge_base,
#             memory=True
#         )
        
#         # Agente consolidador
#         self.consolidator_agent = Agent(
#             name="SuggestionConsolidator",
#             model=OpenAIChat(id="gpt-4o-mini", api_key=api_key),
#             instructions="""
#             Você consolida sugestões de múltiplos chunks em um resultado final coerente.
#             Remove duplicatas, resolve conflitos e organiza por prioridade.
#             Retorna JSON com formato especificado.
#             """,
#             knowledge=self.knowledge_base,
#             memory=True,
#             response_format="json"
#         )
    
#     def process_document(self, document_html: str, question: str) -> ProcessingResult:
#         """Processa documento acadêmico com estratégia otimizada"""
        
#         # 1. Analisa documento e determina estratégia
#         strategy, context = self.analyzer.analyze_document(document_html)
        
#         # 2. Armazena contexto global na base de conhecimento
#         document_id = self._store_document_context(context, document_html)
        
#         # 3. Verifica se é ação global
#         is_global_action = self._is_global_action(question)
        
#         try:
#             if is_global_action:
#                 result = self._process_global_action(document_html, question, context)
#             elif strategy == ProcessingStrategy.SINGLE_PASS:
#                 result = self._process_single_pass(document_html, question, context)
#             else:
#                 result = self._process_chunked(document_html, question, context, strategy)
            
#             result.strategy_used = strategy
#             return result
            
#         finally:
#             # Limpa contexto temporal da sessão
#             self._cleanup_session_context(document_id)
    
#     def _is_global_action(self, question: str) -> bool:
#         """Detecta se a pergunta requer ação global no documento"""
#         global_keywords = [
#             'todas as ocorrências', 'altere todas', 'substitua todos',
#             'mude todas', 'corrija todas', 'replace all', 'change all',
#             'documento inteiro', 'todo o documento', 'globalmente'
#         ]
        
#         question_lower = question.lower()
#         return any(keyword in question_lower for keyword in global_keywords)
    
#     def _process_global_action(self, document_html: str, question: str, context: DocumentContext) -> ProcessingResult:
#         """Processa ações que afetam o documento inteiro"""
        
#         # Primeiro, identifica a ação específica
#         action_prompt = f"""
#         Contexto do documento: {context.title}
#         Pergunta do usuário: {question}
        
#         Esta é uma ação global. Processe a seguinte ação no documento completo:
        
#         Documento HTML:
#         {document_html}
        
#         Retorne JSON no formato:
#         {{
#             "suggestions": [{{
#                 "change": "documento HTML modificado completo",
#                 "explanation": "explicação da alteração global realizada"
#             }}],
#             "answer": "resposta explicando as alterações feitas",
#             "modifiedDocument": "HTML com marcações de alteração"
#         }}
#         """
        
#         response = self.global_action_agent.run(action_prompt)
        
#         # Parse da resposta JSON
#         try:
#             result_data = json.loads(response.content if hasattr(response, 'content') else str(response))
            
#             suggestions = [
#                 Suggestion(
#                     change=s["change"],
#                     explanation=s["explanation"],
#                     global_action=True
#                 ) for s in result_data["suggestions"]
#             ]
            
#             return ProcessingResult(
#                 suggestions=suggestions,
#                 answer=result_data["answer"],
#                 modified_document=result_data["modifiedDocument"],
#                 strategy_used=ProcessingStrategy.SINGLE_PASS,
#                 cost_estimate=self._estimate_cost(len(document_html), "global_action")
#             )
            
#         except (json.JSONDecodeError, KeyError) as e:
#             # Fallback para formato texto
#             return ProcessingResult(
#                 suggestions=[Suggestion(
#                     change=document_html,
#                     explanation="Erro ao processar ação global",
#                     global_action=True
#                 )],
#                 answer=f"Erro ao processar ação global: {str(e)}",
#                 modified_document=document_html,
#                 strategy_used=ProcessingStrategy.SINGLE_PASS,
#                 cost_estimate=0.0
#             )
    
#     def _process_single_pass(self, document_html: str, question: str, context: DocumentContext) -> ProcessingResult:
#         """Processa documento pequeno em uma única passada"""
        
#         prompt = f"""
#         Você é um especialista em revisão de documentos acadêmicos.
        
#         Contexto do documento:
#         - Título: {context.title}
#         - Nível acadêmico: {context.academic_level}
#         - Estilo: {context.writing_style}
#         - Palavras: {context.total_words}
        
#         Documento HTML:
#         {document_html}
        
#         Pergunta: {question}
        
#         {self._get_output_format_instructions()}
#         """
        
#         response = self.main_reviewer.run(prompt)
        
#         return self._parse_agent_response(response, context, len(document_html))
    
#     def _process_chunked(self, document_html: str, question: str, context: DocumentContext, strategy: ProcessingStrategy) -> ProcessingResult:
#         """Processa documento grande usando chunks"""
        
#         # 1. Cria chunks
#         chunks = self.analyzer.create_chunks(document_html, context)
        
#         # 2. Processa cada chunk mantendo contexto
#         all_suggestions = []
#         chunk_results = []
        
#         for chunk in chunks:
#             chunk_result = self._process_single_chunk(chunk, question, context, chunks)
#             chunk_results.append(chunk_result)
#             all_suggestions.extend(chunk_result.suggestions)
        
#         # 3. Consolida resultados
#         consolidated_result = self._consolidate_chunk_results(
#             chunk_results, document_html, question, context
#         )
        
#         # 4. Reconstrói documento com alterações
#         modified_document = self._reconstruct_document_with_suggestions(
#             document_html, chunks, chunk_results
#         )
        
#         consolidated_result.modified_document = modified_document
#         consolidated_result.strategy_used = strategy
        
#         return consolidated_result
    
#     def _process_single_chunk(self, chunk: DocumentChunk, question: str, global_context: DocumentContext, all_chunks: List[DocumentChunk]) -> ProcessingResult:
#         """Processa um único chunk mantendo contexto global"""
        
#         # Contexto adicional dos chunks vizinhos
#         neighbor_context = self._get_neighbor_context(chunk, all_chunks)
        
#         prompt = f"""
#         Você está revisando parte de um documento acadêmico. Mantenha o contexto global.
        
#         CONTEXTO GLOBAL:
#         - Documento: {global_context.title}
#         - Nível: {global_context.academic_level}
#         - Tópicos principais: {', '.join(global_context.main_topics)}
#         - Total de palavras: {global_context.total_words}
        
#         CONTEXTO LOCAL:
#         - Seção: {chunk.section_title}
#         - Posição no documento: {chunk.position + 1} de {len(all_chunks)}
#         - Contexto vizinho: {neighbor_context}
        
#         CONTEÚDO ATUAL (Chunk {chunk.id}):
#         {chunk.content}
        
#         PERGUNTA: {question}
        
#         IMPORTANTE: Suas sugestões devem considerar o contexto global do documento.
#         Não faça alterações que quebrem a coerência com outras seções.
        
#         {self._get_output_format_instructions()}
#         """
        
#         response = self.main_reviewer.run(prompt)
#         result = self._parse_agent_response(response, global_context, len(chunk.content))
        
#         # Marca sugestões com ID do chunk
#         for suggestion in result.suggestions:
#             suggestion.chunk_id = chunk.id
            
#         return result
    
#     def _get_neighbor_context(self, current_chunk: DocumentChunk, all_chunks: List[DocumentChunk]) -> str:
#         """Obtém contexto dos chunks vizinhos"""
#         context_parts = []
        
#         # Chunk anterior
#         if current_chunk.position > 0:
#             prev_chunk = all_chunks[current_chunk.position - 1]
#             context_parts.append(f"Seção anterior: {prev_chunk.section_title}")
        
#         # Chunk posterior
#         if current_chunk.position < len(all_chunks) - 1:
#             next_chunk = all_chunks[current_chunk.position + 1]
#             context_parts.append(f"Próxima seção: {next_chunk.section_title}")
        
#         return " | ".join(context_parts) if context_parts else "Chunk isolado"
    
#     def _consolidate_chunk_results(self, chunk_results: List[ProcessingResult], original_html: str, question: str, context: DocumentContext) -> ProcessingResult:
#         """Consolida resultados de múltiplos chunks"""
        
#         # Combina todas as sugestões
#         all_suggestions = []
#         all_answers = []
        
#         for result in chunk_results:
#             all_suggestions.extend(result.suggestions)
#             all_answers.append(result.answer)
        
#         # Prompt para consolidação
#         consolidation_prompt = f"""
#         Consolide as seguintes sugestões de revisão de um documento acadêmico.
        
#         Documento: {context.title}
#         Pergunta original: {question}
        
#         Sugestões por chunk:
#         {json.dumps([{
#             'chunk_id': s.chunk_id,
#             'change': s.change[:200] + '...' if len(s.change) > 200 else s.change,
#             'explanation': s.explanation
#         } for s in all_suggestions], indent=2, ensure_ascii=False)}
        
#         Tarefas:
#         1. Remove sugestões duplicadas ou conflitantes
#         2. Prioriza sugestões mais impactantes
#         3. Garante coerência global
#         4. Cria resposta consolidada
        
#         {self._get_output_format_instructions()}
#         """
        
#         response = self.consolidator_agent.run(consolidation_prompt)
#         consolidated = self._parse_agent_response(response, context, len(original_html))
        
#         # Calcula custo total
#         total_cost = sum(result.cost_estimate for result in chunk_results)
#         consolidated.cost_estimate = total_cost
        
#         return consolidated
    
#     def _reconstruct_document_with_suggestions(self, original_html: str, chunks: List[DocumentChunk], chunk_results: List[ProcessingResult]) -> str:
#         """Reconstrói documento aplicando sugestões dos chunks"""
        
#         # Cria mapa de sugestões por posição
#         suggestions_map = {}
#         suggestion_counter = 0
        
#         for i, result in enumerate(chunk_results):
#             chunk = chunks[i]
#             for suggestion in result.suggestions:
#                 if suggestion.change:
#                     suggestions_map[chunk.id] = {
#                         'original': chunk.content,
#                         'modified': suggestion.change,
#                         'index': suggestion_counter
#                     }
#                     suggestion_counter += 1
        
#         # Reconstrói HTML marcando alterações
#         modified_html = original_html
        
#         # Aplica marcações de sugestão
#         for chunk_id, suggestion_data in suggestions_map.items():
#             original_content = suggestion_data['original']
#             modified_content = suggestion_data['modified']
#             index = suggestion_data['index']
            
#             # Encontra e substitui o conteúdo original
#             if original_content in modified_html:
#                 marked_content = f'<suggestion data-idx="{index}">{original_content}</suggestion>'
#                 modified_html = modified_html.replace(original_content, marked_content, 1)
        
#         return modified_html
    
#     def _store_document_context(self, context: DocumentContext, document_html: str) -> str:
#         """Armazena contexto do documento na base de conhecimento"""
#         document_id = hashlib.md5(document_html.encode()).hexdigest()[:12]
        
#         context_data = {
#             "id": document_id,
#             "context": asdict(context),
#             "html_sample": document_html[:1000],  # Apenas amostra
#             "timestamp": "2024-01-01"  # Em produção usar datetime real
#         }
        
#         try:
#             self.knowledge_base.upsert([context_data])
#         except Exception as e:
#             print(f"Erro ao armazenar contexto: {e}")
        
#         return document_id
    
#     def _cleanup_session_context(self, document_id: str):
#         """Remove contexto temporal da sessão"""
#         try:
#             # Em produção, implementar limpeza da base de conhecimento
#             pass
#         except Exception as e:
#             print(f"Erro na limpeza: {e}")
    
#     def _parse_agent_response(self, response, context: DocumentContext, content_length: int) -> ProcessingResult:
#         """Converte resposta do agente para ProcessingResult"""
        
#         try:
#             # Tenta parsear como JSON
#             if hasattr(response, 'content'):
#                 response_text = response.content
#             else:
#                 response_text = str(response)
            
#             # Remove markdown se presente
#             if response_text.startswith('```json'):
#                 response_text = response_text.strip('```json').strip('```').strip()
            
#             data = json.loads(response_text)
            
#             suggestions = [
#                 Suggestion(
#                     change=s.get("change", ""),
#                     explanation=s.get("explanation", "")
#                 ) for s in data.get("suggestions", [])
#             ]
            
#             return ProcessingResult(
#                 suggestions=suggestions,
#                 answer=data.get("answer", "Processamento concluído"),
#                 modified_document=data.get("modifiedDocument", ""),
#                 strategy_used=ProcessingStrategy.SINGLE_PASS,
#                 cost_estimate=self._estimate_cost(content_length, "review")
#             )
            
#         except (json.JSONDecodeError, AttributeError) as e:
#             # Fallback para resposta em texto
#             return ProcessingResult(
#                 suggestions=[],
#                 answer=f"Erro ao processar resposta: {str(e)}",
#                 modified_document="",
#                 strategy_used=ProcessingStrategy.SINGLE_PASS,
#                 cost_estimate=0.0
#             )
    
#     def _estimate_cost(self, content_length: int, operation_type: str) -> float:
#         """Estima custo do processamento"""
        
#         # Estimativas baseadas em preços OpenAI (Janeiro 2024)
#         costs = {
#             "gpt-4o": {"input": 2.50, "output": 10.00},  # por 1M tokens
#             "gpt-4o-mini": {"input": 0.15, "output": 0.60}
#         }
        
#         # Estima tokens (aproximadamente 4 caracteres por token)
#         tokens = content_length / 4
        
#         if operation_type == "global_action":
#             # Usa GPT-4o para ações globais
#             cost = (tokens * costs["gpt-4o"]["input"] + tokens * 0.5 * costs["gpt-4o"]["output"]) / 1_000_000
#         else:
#             # Usa mix de modelos
#             cost = (tokens * costs["gpt-4o-mini"]["input"] + tokens * 0.3 * costs["gpt-4o"]["output"]) / 1_000_000
        
#         return round(cost, 4)
    
#     def _get_reviewer_instructions(self) -> str:
#         """Retorna as instruções do agente revisor (baseadas no prompt original)"""
#         return """
#         Você é um **Especialista em Revisão de Documentos Acadêmicos e Científicos** com expertise avançada em:
#         - Análise crítica de conteúdo acadêmico (artigos, teses, monografias)
#         - Melhoria de clareza, legibilidade e estrutura textual
#         - Conformidade com normas acadêmicas e científicas
#         - Sugestões de referências e conteúdo adicional
#         - Otimização da organização e fluxo de informações

#         CRITÉRIOS DE ANÁLISE ACADÊMICA:

#         Prioridades de Revisão:
#         1. **Clareza e Precisão**: Linguagem clara, terminologia adequada, ausência de ambiguidades
#         2. **Estrutura Lógica**: Organização coerente, transições efetivas, hierarquia de ideias
#         3. **Rigor Acadêmico**: Argumentação consistente, evidências adequadas, neutralidade científica
#         4. **Normas e Convenções**: Formatação, citações, referências, estrutura disciplinar
#         5. **Completude**: Lacunas de conteúdo, necessidade de exemplos ou explicações adicionais

#         Tipos de Sugestões Permitidas:
#         - **Melhoria de clareza**: Reformulação de frases complexas ou ambíguas
#         - **Reorganização estrutural**: Reordenação de parágrafos, seções ou argumentos
#         - **Adição de conteúdo**: Exemplos, explicações, transições, referências
#         - **Remoção de redundâncias**: Repetições, informações irrelevantes
#         - **Correção de fluxo**: Conexões lógicas entre ideias
#         - **Adequação de registro**: Formalidade, tom acadêmico apropriado

#         IMPORTANTE: Sempre considere o contexto global do documento ao fazer sugestões.
#         Mantenha coerência com o estilo e nível acadêmico identificado.
#         """
    
#     def _get_output_format_instructions(self) -> str:
#         """Retorna instruções de formato de saída JSON"""
#         return """
#         FORMATO DE SAÍDA OBRIGATÓRIO - Retorne EXCLUSIVAMENTE um JSON válido:

#         {
#             "suggestions": [
#                 {
#                     "change": "HTML completo da alteração sugerida",
#                     "explanation": "Justificativa técnica e acadêmica da sugestão"
#                 }
#             ],
#             "answer": "Resposta direta à pergunta, incluindo explicações das sugestões",
#             "modifiedDocument": "HTML modificado com tags <suggestion> ou null"
#         }

#         REGRAS PARA SUGESTÕES:
#         - Cada sugestão deve abranger no máximo elementos da raiz do HTML
#         - Mudanças relacionadas = 1 sugestão
#         - Mudanças independentes = sugestões separadas
#         - Preserve formatação HTML original quando possível
#         - Use tags <suggestion data-idx="i"> para marcações
#         """


# # Exemplo de uso e teste da classe
# def create_service_example():
#     """Exemplo de como instanciar e usar o serviço"""
    
#     # Configuração
#     postgres_config = {
#         "host": "localhost",
#         "port": 5432,
#         "user": "agno_user",
#         "password": "password",
#         "database": "academic_docs"
#     }
    
#     openai_api_key = "sk-your-openai-key-here"
    
#     # Instancia o serviço
#     service = AcademicDocumentService(openai_api_key, postgres_config)
    
#     return service


# def test_document_processing():
#     """Função de teste com diferentes cenários"""
    
#     service = create_service_example()
    
#     # Teste 1: Documento pequeno
#     small_document = """
#     <h1>Introdução ao Machine Learning</h1>
#     <p>Este trabalho analiza os principais algoritmos de aprendizado de máquina.</p>
#     <p>Os resultados são importantes para a área.</p>
#     """
    
#     result1 = service.process_document(
#         small_document, 
#         "Corrija erros ortográficos e melhore a conexão entre as ideias"
#     )
    
#     print("=== RESULTADO DOCUMENTO PEQUENO ===")
#     print(f"Estratégia: {result1.strategy_used.value}")
#     print(f"Custo estimado: ${result1.cost_estimate}")
#     print(f"Sugestões: {len(result1.suggestions)}")
#     print(f"Resposta: {result1.answer[:200]}...")
#     print()
    
#     # Teste 2: Ação global
#     medium_document = """
#     <h1>Análise de Carros Elétricos</h1>
#     <p>O carro elétrico representa uma revolução no transporte.</p>
#     <h2>Tipos de Carro</h2>
#     <p>Existem diversos tipos de carro no mercado atual.</p>
#     <p>Cada carro possui características específicas.</p>
#     """
    
#     result2 = service.process_document(
#         medium_document,
#         "Altere todas as ocorrências da palavra 'carro' por 'veículo'"
#     )
    
#     print("=== RESULTADO AÇÃO GLOBAL ===")
#     print(f"Estratégia: {result2.strategy_used.value}")
#     print(f"Custo estimado: ${result2.cost_estimate}")
#     print(f"É ação global: {result2.suggestions[0].global_action if result2.suggestions else False}")
#     print(f"Resposta: {result2.answer[:200]}...")
#     print()
    
#     # Teste 3: Documento longo (simulado)
#     large_document = """
#     <h1>Tese de Doutorado: Inteligência Artificial na Medicina</h1>
#     <h2>Resumo</h2>
#     <p>Esta tese investiga aplicações de IA na medicina moderna...</p>
#     """ + "<p>Parágrafo de conteúdo acadêmico. " * 1000 + "</p>"
    
#     result3 = service.process_document(
#         large_document,
#         "Melhore a clareza e organização do documento"
#     )
    
#     print("=== RESULTADO DOCUMENTO LONGO ===")
#     print(f"Estratégia: {result3.strategy_used.value}")
#     print(f"Custo estimado: ${result3.cost_estimate}")
#     print(f"Sugestões: {len(result3.suggestions)}")
#     print(f"Documento modificado possui marcações: {'<suggestion' in result3.modified_document}")
    
#     return [result1, result2, result3]


# # Classe utilitária para integração com API REST
# class APIIntegrationHelper:
#     """Helper para integração com API REST FastAPI/Flask"""
    
#     def __init__(self, service: AcademicDocumentService):
#         self.service = service
    
#     def format_api_response(self, result: ProcessingResult) -> Dict[str, Any]:
#         """Converte ProcessingResult para formato da API original"""
        
#         return {
#             "suggestions": [
#                 {
#                     "change": suggestion.change,
#                     "explanation": suggestion.explanation
#                 } for suggestion in result.suggestions
#             ],
#             "answer": result.answer,
#             "modifiedDocument": result.modified_document,
#             "metadata": {
#                 "strategy_used": result.strategy_used.value,
#                 "cost_estimate": result.cost_estimate,
#                 "total_suggestions": len(result.suggestions)
#             }
#         }
    
#     def process_api_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Processa requisição da API no formato original"""
        
#         document_html = request_data.get("document", "")
#         question = request_data.get("question", "")
        
#         if not document_html or not question:
#             return {
#                 "error": "Documento e pergunta são obrigatórios",
#                 "suggestions": [],
#                 "answer": "",
#                 "modifiedDocument": None
#             }
        
#         try:
#             result = self.service.process_document(document_html, question)
#             return self.format_api_response(result)
            
#         except Exception as e:
#             return {
#                 "error": f"Erro no processamento: {str(e)}",
#                 "suggestions": [],
#                 "answer": f"Erro interno: {str(e)}",
#                 "modifiedDocument": None
#             }


# # Exemplo de uso com FastAPI (estrutura)
# """
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# class DocumentRequest(BaseModel):
#     document: str
#     question: str

# # Instancia o serviço globalmente
# service = create_service_example()
# api_helper = APIIntegrationHelper(service)

# @app.post("/review-document")
# async def review_document(request: DocumentRequest):
#     try:
#         request_data = {
#             "document": request.document,
#             "question": request.question
#         }
        
#         result = api_helper.process_api_request(request_data)
        
#         if "error" in result:
#             raise HTTPException(status_code=400, detail=result["error"])
        
#         return result
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
# """


# if __name__ == "__main__":
#     # Executa testes de exemplo
#     print("🚀 Testando Serviço de Revisão Acadêmica com Agno")
#     print("=" * 60)
    
#     try:
#         results = test_document_processing()
#         print("\n✅ Todos os testes executados com sucesso!")
#         print(f"📊 Resultados gerados: {len(results)}")
        
#     except Exception as e:
#         print(f"❌ Erro durante os testes: {e}")
#         print("💡 Certifique-se de que o Agno está instalado e configurado corretamente")