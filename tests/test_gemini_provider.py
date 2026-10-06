"""Unit tests for Gemini LLM and Embedding provider factory integration."""
import pytest
from unittest.mock import MagicMock, patch

from src.config import Config
from src.rag_ingest.llm.factory import create_llm, create_embedding_provider
from src.rag_ingest.llm.gemini_provider import GeminiLLM, GeminiEmbedding


def test_create_gemini_llm():
    test_config = Config(
        pg_password="dummy",
        llm_provider="gemini",
        llm_model="gemini-2.5-flash",
        gemini_api_key="test_key_123"
    )
    with patch("src.rag_ingest.llm.gemini_provider.genai.Client") as mock_client:
        llm = create_llm(test_config, use_case="ingestion")
        assert isinstance(llm, GeminiLLM)
        mock_client.assert_called_once_with(api_key="test_key_123")


def test_create_gemini_embedding_provider():
    test_config = Config(
        pg_password="dummy",
        embedding_provider="gemini",
        embedding_model="text-embedding-004",
        embedding_dimensions=768,
        gemini_api_key="test_key_123"
    )
    with patch("src.rag_ingest.llm.gemini_provider.genai.Client") as mock_client:
        embedding_prov = create_embedding_provider(test_config)
        assert isinstance(embedding_prov, GeminiEmbedding)
        assert embedding_prov.dimensions == 768
        mock_client.assert_called_once_with(api_key="test_key_123")


def test_gemini_llm_complete():
    test_config = Config(
        pg_password="dummy",
        llm_provider="gemini",
        llm_model="gemini-2.5-flash",
        gemini_api_key="test_key_123"
    )
    with patch("src.rag_ingest.llm.gemini_provider.genai.Client") as mock_client_cls:
        mock_client_inst = MagicMock()
        mock_client_cls.return_value = mock_client_inst
        
        mock_response = MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_client_inst.models.generate_content.return_value = mock_response

        llm = GeminiLLM(test_config, model="gemini-2.5-flash")
        res = llm.complete(system_prompt="You are a helper.", user_content="Hello")
        
        assert res == '{"status": "ok"}'
        mock_client_inst.models.generate_content.assert_called_once()
