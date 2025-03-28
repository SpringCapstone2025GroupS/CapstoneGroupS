import os
from driver import main
import pytest


def test_invalid_env(monkeypatch: pytest.MonkeyPatch):
    """Tests if program exits on invalid env variables"""
    def mock_getenv(var: str):
        return None
    monkeypatch.setattr(os, "getenv", mock_getenv)
    
    with pytest.raises(SystemExit) as e:
        main()
    assert str(e.value) == "Error: CLIENT_ID not set in .env file"

    def mock_getenv_with_client_id(var: str):
        if var =='CLIENT_ID':
            return "MOCK_CLIENT_ID"
    monkeypatch.setattr(os, "getenv", mock_getenv_with_client_id)

    with pytest.raises(SystemExit) as e:
        main()
    assert str(e.value) == "Error: CLIENT_SECRET not set in .env file"
    


