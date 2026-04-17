

import time

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.prompts import PromptTemplate
from llama_index.core import QueryBundle

from src.domain.port import LLMPort

prompt = PromptTemplate(
    """
Eres un asistente digital experto en facturación electrónica.

Tu tarea es responder preguntas utilizando únicamente la información proporcionada en el contexto.

Contexto:
---------------------
{context_str}
---------------------

Consulta:
{query_str}

Instrucciones:
- Responde SOLO con información presente en el contexto.
- No uses conocimiento externo.
- Si la información no está en el contexto, responde: "No dispongo de información suficiente para responder esta consulta."
- Si hay múltiples fragmentos relevantes, intégralos en una única respuesta coherente.
- Prioriza precisión sobre cantidad de información.
- Sé claro, directo y evita redundancias.
- Cuando sea posible, indica la fuente (documento y página) de la información.

Formato de respuesta:
- Usa formato Markdown.
- Estructura la respuesta en párrafos o listas si es necesario.
- Destaca conceptos importantes en **negrita** cuando aporte claridad.
    """
)


class LLMAdapter(LLMPort):
    def __init__(self, llamaindex_llm_instance):
        # self.llm = llamaindex_llm_instance
        self.synthesizer = get_response_synthesizer(
            llm=llamaindex_llm_instance,
            text_qa_template=prompt,
            # streaming=True,
        )

    def generate_answer(self, prompt: str, context: list) -> str:
        start_gen = time.time()
        response = self.synthesizer.synthesize(
            query=QueryBundle(prompt),
            nodes=context)
        end_gen = time.time()

        # print(response)

        return response.response
