

import re
import time
import tiktoken

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.prompts import PromptTemplate
from llama_index.core import QueryBundle
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler

from src.domain.port import LLMPort
from src.domain.valueobject import Answer, Intent

prompt_rag = PromptTemplate(
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
        self.llm = llamaindex_llm_instance

    def generate_answer(self, prompt: str, context: list) -> str:

        token_counter = self.__get_token_counter(self.llm.model)
        callback_manager = CallbackManager([token_counter])

        synthesizer_rag = get_response_synthesizer(
            llm=self.llm,
            text_qa_template=prompt_rag,
            callback_manager=callback_manager
        )

        start_time = time.perf_counter()

        response = synthesizer_rag.synthesize(
            query=QueryBundle(prompt),
            nodes=context)

        end_time = time.perf_counter()

        latency = int((end_time - start_time) * 1000)

        print(f"latency: {latency}")
        print(
            f"Tokens Prompt (Usuario + Contexto): {token_counter.prompt_llm_token_count}")
        print(
            f"Tokens Respuesta (LLM): {token_counter.completion_llm_token_count}")

        return Answer(content=response.response,
                      latency=latency,
                      tokens_prompt=token_counter.prompt_llm_token_count,
                      tokens_completion=token_counter.completion_llm_token_count)

    def __get_token_counter(self, model_name: str):
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")

        return TokenCountingHandler(tokenizer=encoding.encode)
