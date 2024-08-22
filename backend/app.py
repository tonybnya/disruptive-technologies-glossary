"""
Main file of the application.
"""

from __future__ import annotations

from flask import Flask

# Create a Flask application
app: Flask = Flask(__name__)


@app.route("/")
def index() -> dict[str, str]:
    """
    Define the default (root) endpoint "/".

    Input:  Nothing
    Output: a dictionary message
    """
    return {"message": "Welcome! This is a Glossary on AI and Blockchain"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5003)
