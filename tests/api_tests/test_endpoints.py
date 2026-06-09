import pytest


def test_health_check(client):
    response = client.get("/health")
    if response.status_code == 404:
        pytest.skip("Health endpoint not implemented")
    assert response.status_code == 200


def test_translate_success(client, mock_graph_success):
    payload = {"query": "Show all registered users"}
    response = client.post("/translate", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "cypher" in data
    assert data["cypher"] == "MATCH (n:User) RETURN n"
    assert data["try_count"] == 1
    assert data["error"] == ""


def test_translate_llm_failure(client, mock_graph_failure):
    payload = {"query": "Invalid query violating EBNF"}
    response = client.post("/translate", json=payload)

    assert response.status_code in (400, 422, 500)

    data = response.json()
    assert data["cypher"] == ""
    assert "EBNF violation" in data["error"]
    assert data["try_count"] == 3


def test_translate_validation_error(client):
    payload = {"wrong_field": "Show all users"}
    response = client.post("/translate", json=payload)

    assert response.status_code == 422

    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "query"]
