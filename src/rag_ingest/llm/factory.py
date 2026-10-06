"""Factory module for Document Gap Analysis pipeline."""
from typing import Literal

from src.config import Config
from .base import LLMProvider, EmbeddingProvider
from .openai_provider import OpenAILLM, OpenAIEmbedding
from .gemini_provider import GeminiLLM, GeminiEmbedding
from .resolve import resolve_llm_connection

LLMUseCase = Literal["ingestion", "comparison", "chat"]


def create_llm(settings: Config, use_case: LLMUseCase) -> LLMProvider:
    provider_name = settings.llm_provider.lower()
    model, base_url = resolve_llm_connection(settings, use_case)
    if provider_name == "openai":
        return OpenAILLM(settings, model, base_url)
    elif provider_name == "gemini":
        return GeminiLLM(settings, model, base_url)
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Supported: openai, gemini")

def create_embedding_provider(settings: Config) -> EmbeddingProvider:
    provider_name = settings.embedding_provider.lower()
    if provider_name == "openai":
        return OpenAIEmbedding(settings)
    elif provider_name == "gemini":
        return GeminiEmbedding(settings)
    else:
        raise ValueError(f"Unknown Embedding provider: {provider_name}. Supported: openai, gemini")

