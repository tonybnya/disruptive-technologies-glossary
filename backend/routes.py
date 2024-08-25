"""
This file defines the routes/endpoints for the API.
"""

from __future__ import annotations

from typing import Dict, Literal, Tuple, Union

from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models import Term


def register_routes(app: Flask, db: SQLAlchemy):
    """
    Define and register the routes/endpoints of the API.
    """

    @app.route("/")
    # def root() -> Dict[str, str]:
    def root() -> str:
        """
        Define the default (root) endpoint "/".

        Input:  Nothing
        Output: a dictionary message
        """
        term: Term = Term.query.all()
        return str(term)
        return {"message": "Welcome! This is a Glossary on AI and Blockchain"}

    @app.route("/terms", methods=["POST"])
    def create_term() -> Tuple[Response, Union[Literal[201], Literal[400]]]:
        """
        Creates a new Term in the glossary database.
        POST /terms

        Input:  Nothing
        Output: (Response) | a JSON response with the created Term or an error message.
        """
        # Get the JSON data from the request body
        data = request.json

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        term: Term = Term(
            english_term=data.get("english_term"),
            french_term=data.get("french_term"),
            variant_en=data.get("variant_en"),
            variant_fr=data.get("variant_fr"),
            synonyms_en=data.get("synonyms_en"),
            synonyms_fr=data.get("synonyms_fr"),
            definition_en=data.get("definition_en"),
            definition_fr=data.get("definition_fr"),
            syntactic_cooccurrence_en=data.get("syntactic_cooccurrence_en"),
            syntactic_cooccurrence_fr=data.get("syntactic_cooccurrence_fr"),
            lexical_relations_en=data.get("lexical_relations_en"),
            lexical_relations_fr=data.get("lexical_relations_fr"),
            phraseology_en=data.get("phraseology_en"),
            phraseology_fr=data.get("phraseology_fr"),
            related_term_en=data.get("related_term_en"),
            related_term_fr=data.get("related_term_fr"),
            contexts_en=data.get("contexts_en"),
            contexts_fr=data.get("contexts_fr"),
            frequent_expression_en=data.get("frequent_expression_en"),
            frequent_expression_fr=data.get("frequent_expression_fr"),
        )

        # Add the term to the session
        db.session.add(term)
        # Commit the session to save the term
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Term created successfully!",
                    "term": term.tid,
                    "english_term": term.english_term,
                    "french_term": term.french_term,
                }
            ),
            201,
        )
