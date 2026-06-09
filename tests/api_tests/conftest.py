import os
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from src.api import app

load_dotenv()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_graph_success():
    mock_state = {
        "generated_cypher": MagicMock(query="MATCH (n:User) RETURN n", note="OK"),
        "final_error": "",
        "try_count": 1,
        "final_warnings": "",
        "attempts": MagicMock(attempts=["MATCH (n:User) RETURN n"]),
    }

    with patch("src.api.build_graph") as mock_build:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = mock_state
        mock_build.return_value = mock_instance
        yield mock_build


@pytest.fixture
def mock_graph_failure():
    mock_state = {
        "generated_cypher": MagicMock(query="", note=""),
        "final_error": "SyntaxError: EBNF violation",
        "try_count": 3,
        "final_warnings": "Failed to generate valid query",
        "attempts": MagicMock(attempts=["MATCH error", "MATCH error", "MATCH error"]),
    }

    with patch("src.api.build_graph") as mock_build:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = mock_state
        mock_build.return_value = mock_instance
        yield mock_build
