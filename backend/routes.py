"""
This file defines the routes/endpoints for the API.
"""

from __future__ import annotations

from typing import Dict, Literal, Tuple, Union

from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from models import Term


def register_routes(app: Flask, db: SQLAlchemy):
    """
    Define and register the routes/endpoints of the API.
    """

    @app.route("/")
    def root() -> Tuple[Response, Literal[200]]:
        """
        Define the default (root) endpoint "/".

        Input:  Nothing
        Output: a dictionary message
        """
        # return (
        #     jsonify(
        #         {"message": "Welcome! This is a LEC-Glossary API on AI and Blockchain."}
        #     ),
        #     200,
        # )
        terms: Term = Term.query.all()
        return str(terms)

    @app.route("/terms", methods=["POST"])
    def create_term() -> Tuple[Response, Union[Literal[201], Literal[400]]]:
        """
        Creates a new Term in the glossary database.
        POST /terms

        Input:  Nothing
        Output: (Response) | a JSON response with the created Term or an error message.
        """
        # Get the JSON data from the request body
        data = request.get_json()

        # Validate the presence of required data
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        english_term: str = data.get("english_term")
        french_term: str = data.get("french_term")

        if not english_term:
            return jsonify({"error": "English Term is required."}), 400
        if not french_term:
            return jsonify({"error": "French Term is required."}), 400

        # Validate data types of the the required fields
        if not isinstance(english_term, str) or not isinstance(french_term, str):
            return (
                jsonify(
                    {
                        "error": "Invalid data types: English and French terms should be strings"
                    }
                ),
                400,
            )

        term: Term = Term(
            english_term=english_term.strip(),
            french_term=french_term.strip(),
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

        try:
            # Add the term to the session
            db.session.add(term)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return (
                jsonify(
                    {
                        "error": "Term with the same english_term and french_term already exists."
                    }
                ),
                400,
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

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
