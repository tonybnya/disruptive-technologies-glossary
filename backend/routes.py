"""
This file defines the routes/endpoints for the API.
"""

from __future__ import annotations

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import Term


def register_routes(app: Flask, db: SQLAlchemy):
    """
    Define and register the routes/endpoints of the API.
    """

    @app.route("/")
    # def root() -> dict[str, str]:
    def root() -> str:
        """
        Define the default (root) endpoint "/".

        Input:  Nothing
        Output: a dictionary message
        """
        term: Term = Term.query.all()
        return str(term)
        return {"message": "Welcome! This is a Glossary on AI and Blockchain"}
