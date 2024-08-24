"""
This file creates the application.
"""

from __future__ import annotations

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Define a database object
db: SQLAlchemy = SQLAlchemy()


def create_app() -> Flask:
    """
    Create the Flask app and return it as an object.

    Input:  Nothing
    Output: an object representing the Flask application
    """
    # Define the Flask application
    app: Flask = Flask(__name__)

    # Define a string for the SQLite database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./glossary.db"

    # Initialize the Flask application
    db.init_app(app)

    # import register_routes here to avoid circular imports
    from routes import register_routes

    register_routes(app, db)

    migrate: Migrate = Migrate(app, db)

    return app
