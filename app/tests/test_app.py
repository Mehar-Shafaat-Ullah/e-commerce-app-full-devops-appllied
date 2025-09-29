import os
import tempfile
import pytest
import requests
from multiprocessing import Process
import time
from app import app
from models import init_db

# We will run the Flask app locally (no DB). Use SQLite for tests or mock DB.
# For simplicity here we'll test the health endpoint.

@pytest.fixture(scope="module")
def test_client():
    # run flask app in a separate process
    proc = Process(target=app.run, kwargs={"host":"127.0.0.1","port":5001})
    proc.start()
    time.sleep(1)
    yield
    proc.terminate()
    proc.join()

def test_health(test_client):
    r = requests.get("http://127.0.0.1:5001/health", timeout=3)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
