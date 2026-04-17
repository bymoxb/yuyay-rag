import os

from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from src.infra.adapters.llamaindex_adapter import LLMAdapter  # Tu wrapper
from src.domain.port import LLMPort


class LLMFactory:
    @staticmethod
    def get_llm(model_name: str) -> LLMPort:
        if model_name == "gpt-4o-mini":
            llm = OpenAI(model=model_name, api_key=os.getenv("OPENAI_API_KEY"))
        elif model_name == "mistral":
            llm = Ollama(model=model_name, request_timeout=120)
        else:
            raise ValueError(f"Unsupported model: {model_name}")

        return LLMAdapter(llm)
