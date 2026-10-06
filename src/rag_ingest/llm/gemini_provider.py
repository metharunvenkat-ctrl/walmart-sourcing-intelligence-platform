"""Gemini Provider module for Document Gap Analysis pipeline."""
import logging
import os
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError

from src.config import Config
from .base import LLMProvider, EmbeddingProvider
from src.rag_ingest.exceptions import LLMExtractionError, EmbeddingError

logger = logging.getLogger(__name__)


class GeminiLLM(LLMProvider):
    """Google Gemini LLM provider."""

    def __init__(self, settings: Config, model: str, base_url: str | None = None):
        self.settings = settings
        if not model or model.startswith("gpt-") or model == "gemini-2.5-flash":
            model = "gemini-3.8-flash"
        self._model = model
        api_key = settings.gemini_api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in settings or environment variables.")
        self.client = genai.Client(api_key=api_key)
        self.temperature = settings.llm_temperature



    def complete(self, system_prompt: str, user_content: str, temperature: float | None = None) -> str:
        effective_temperature = temperature if temperature is not None else self.temperature

        @retry(
            retry=retry_if_exception_type((APIError, Exception)),
            wait=wait_exponential(multiplier=self.settings.retry_backoff_multiplier, max=self.settings.retry_max_wait),
            stop=stop_after_attempt(self.settings.max_retries),
            before_sleep=lambda retry_state: logger.warning(
                "Retrying Gemini LLM complete",
                extra={
                    "attempt": retry_state.attempt_number,
                    "error_type": type(retry_state.outcome.exception()).__name__
                }
            ),
            reraise=True
        )
        def _call_api():
            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                temperature=effective_temperature,
                max_output_tokens=self.settings.llm_max_tokens,
                response_mime_type="application/json",
            )
            response = self.client.models.generate_content(
                model=self._model,
                contents=user_content,
                config=config,
            )
            return response.text

        try:
            start_time = time.time()
            content = _call_api()
            duration = time.time() - start_time
            logger.info(
                "Gemini LLM call completed",
                extra={
                    "model": self._model,
                    "estimated_input_tokens": len(system_prompt + user_content) // 4,
                    "response_time_seconds": round(duration, 2),
                },
            )
            return content
        except RetryError as e:
            raise LLMExtractionError("Gemini LLM API exhausted retries") from e.last_attempt.exception()


class GeminiEmbedding(EmbeddingProvider):
    """Google Gemini Embedding provider."""

    def __init__(self, settings: Config):
        self.settings = settings
        emb_model = settings.embedding_model if settings.embedding_provider.lower() == "gemini" else "gemini-embedding-001"
        if not emb_model or emb_model.startswith("text-embedding-"):
            emb_model = "gemini-embedding-001"
        self._model = emb_model
        api_key = settings.gemini_api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in settings or environment variables.")
        self.client = genai.Client(api_key=api_key)
        self._dimensions = settings.embedding_dimensions or 3072



    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        @retry(
            retry=retry_if_exception_type((APIError, Exception)),
            wait=wait_exponential(multiplier=self.settings.retry_backoff_multiplier, max=self.settings.retry_max_wait),
            stop=stop_after_attempt(self.settings.max_retries),
            before_sleep=lambda retry_state: logger.warning(
                "Retrying Gemini Embedding",
                extra={
                    "attempt": retry_state.attempt_number,
                    "error_type": type(retry_state.outcome.exception()).__name__
                }
            ),
            reraise=True
        )
        def _call_api_batch(batch_texts: list[str]) -> list[list[float]]:
            config = types.EmbedContentConfig(
                output_dimensionality=self._dimensions
            )
            response = self.client.models.embed_content(
                model=self._model,
                contents=batch_texts,
                config=config,
            )
            return [e.values for e in response.embeddings]

        all_embeddings: list[list[float]] = []
        batch_size = self.settings.embedding_batch_size
        total_texts = len(texts)

        try:
            for i in range(0, total_texts, batch_size):
                batch = texts[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (total_texts + batch_size - 1) // batch_size

                logger.info(f"Processing Gemini embedding batch {batch_num}/{total_batches} ({len(batch)} texts).")
                start_time = time.time()
                batch_embeddings = _call_api_batch(batch)
                duration = time.time() - start_time
                all_embeddings.extend(batch_embeddings)

                logger.info(
                    "Gemini Embedding batch completed",
                    extra={
                        "batch_number": batch_num,
                        "text_count": len(batch),
                        "response_time_seconds": round(duration, 2)
                    }
                )
        except RetryError as e:
            raise EmbeddingError("Gemini Embedding API exhausted retries") from e.last_attempt.exception()

        return all_embeddings
