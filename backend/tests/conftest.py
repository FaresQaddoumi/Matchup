
import pytest

@pytest.fixture
def app(monkeypatch, tmp_path):
    # temp db paths for tests so we don't mess up real data
    test_db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE", str(test_db_path))

    
    from backend.db import init_db
    init_db()

    
    from backend.app import app as flask_app
    flask_app.config.update(TESTING=True)
    return flask_app

@pytest.fixture
def client(app):
    
    return app.test_client()

