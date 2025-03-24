import os
from driver import main, AirportCodeValidator
import pytest


def test_invalid_departure(monkeypatch: pytest.MonkeyPatch):

    def mock_getenv(var: str):
        return None
    monkeypatch.setattr(os, "getenv", mock_getenv)
    
    with pytest.raises(SystemExit) as e:
        main()
    assert str(e.value) == "Invalid departure airport XYZ. Please enter valid airport codes."


