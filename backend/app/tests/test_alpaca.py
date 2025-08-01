import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def auth_header():
    return {"Authorization": "Bearer test-token"}

@patch("app.services.alpaca_adapter.AlpacaAdapter.get_history")
@patch("app.services.alpaca_adapter.AlpacaAdapter.get_account")
def test_alpaca_history(mock_account, mock_hist, auth_header):
    mock_hist.return_value = [100000, 100500, 101000]
    mock_account.return_value = {"equity": 101000}
    resp = client.get("/api/v1/portfolio/alpaca/history", headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert "equity" in data and isinstance(data["equity"], list)
    assert "metrics" in data
