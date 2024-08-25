"""
Test suite for the terms endpoints.
"""

from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from server import app as flask_app


@pytest.fixture
def app() -> Generator[Flask, Flask, Flask]:
    """
    This fixture provides a Flask application instance
    for testing purposes.
    """
    yield flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    This fixture provides a test client that can be used
    to simulate HTTP requests to the Flask application.
    """
    return app.test_client()
