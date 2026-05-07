

import re
import time
import tiktoken

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.prompts import PromptTemplate
from llama_index.core import QueryBundle
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler

from src.domain.port import LLMPort
from src.domain.valueobject import Answer, Intent

prompt_router = ("""Eres un clasificador de intención.

Tu tarea es decidir si el mensaje del usuario debe ir a un sistema RAG de la empresa.

Reglas:
- Solo es "company_query" si pregunta sobre documentación, procesos, políticas o información interna.
- Todo lo demás NO es company_query.

Consulta:
{query_str}

Formato de la respuesta:

{
  "is_company_query": true/false,
  "type": "company_query | greeting | out_of_scope | unclear"
}
""")

prompt_fallback = PromptTemplate("""
Eres un asistente interno de una empresa.

Responde al usuario cuando su mensaje NO requiere consulta en documentación interna.

Reglas:
- Si es saludo, responde de forma breve y amable.
- Si está fuera del contexto de la empresa, indica que solo puedes ayudar con temas internos.
- No menciones sistemas internos.
- Mantén la respuesta en 1-2 frases.

Mensaje del usuario:
{query_str}
""")

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

        self.synthesizer_router = get_response_synthesizer(
            llm=llamaindex_llm_instance,
            text_qa_template=prompt_router,
        )

    def determine_intent(self, query: str) -> Intent:
        try:
            prompt = prompt_router.replace("{query_str}", query)
            response = self.llm.complete(prompt)

            print(f"LLM response for intent determination: {response.text}")

            texto = response.text

            match = re.search(r'"type"\s*:\s*"([^"]+)"', texto)
            type = match.group(1) if match else "out_of_scope"

            match = re.search(r'"is_company_query"\s*:\s*(true|false)', texto)
            is_company = match.group(1) == "true" if match else True

            print(
                f"Extracted intent - is_company_query: {is_company}, type: {type}")

            return Intent(is_company_query=is_company, type=type)
        except Exception as e:
            print("Error in determine_intent:", e)
            return Intent.out_of_scope()

    def fallback_answer(self, query: str):
        start_time = time.perf_counter()
        response = self.llm.complete(prompt_fallback.format(query_str=query))
        end_time = time.perf_counter()

        latency = int((end_time - start_time) * 1000)
        return Answer(content=response.text,
                      latency=latency,
                      tokens_prompt=0,
                      tokens_completion=0)

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

    def stream_fallback_answer(self, query: str):
        # Configuramos el contador de tokens para el fallback
        token_counter = self.__get_token_counter(self.llm.model)
        self.llm.callback_manager = CallbackManager([token_counter])

        start_time = time.perf_counter()

        # Formateamos el prompt de fallback
        prompt = prompt_fallback.format(query_str=query)

        # stream_complete se usa para completar texto plano (sin RAG)
        response_gen = self.llm.stream_complete(prompt)

        for response in response_gen:
            # En stream_complete, el fragmento está en response.delta
            yield {
                "type": "chunk",
                "data": response.delta or ""
            }

        end_time = time.perf_counter()
        latency = int((end_time - start_time) * 1000)

        yield {
            "type": "end",
            "data": {
                "latency": latency,
                "tokens_prompt": token_counter.prompt_llm_token_count,
                "tokens_completion": token_counter.completion_llm_token_count
            }
        }

    def stream_answer(self, prompt: str, context: list):
        token_counter = self.__get_token_counter(self.llm.model)
        callback_manager = CallbackManager([token_counter])

        synthesizer_rag = get_response_synthesizer(
            llm=self.llm,
            text_qa_template=prompt_rag,
            callback_manager=callback_manager,
            streaming=True,
        )

        start_time = time.perf_counter()

        response = synthesizer_rag.synthesize(
            query=QueryBundle(prompt),
            nodes=context
        )

        for token in response.response_gen:
            yield {
                "type": "chunk",
                "data": token
            }

        end_time = time.perf_counter()
        latency = int((end_time - start_time) * 1000)

        yield {
            "type": "end",
            "data": {
                "latency": latency,
                "tokens_prompt": token_counter.prompt_llm_token_count,
                "tokens_completion": token_counter.completion_llm_token_count
            }
        }
