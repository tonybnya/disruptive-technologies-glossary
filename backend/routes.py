"""
This file defines the routes/endpoints for the API.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Tuple, Union

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
        return (
            jsonify(
                {
                    "message": "Glossaire explicatif et combinatoire anglais-francais des technologies transformatrices (Big Data, IA, blockchain) | English-French Explanatory Combinatorial Glossary for Disruptive Technologies (Big Data, AI, Blockchain)."
                }
            ),
            200,
        )
        # terms: Term = Term.query.all()
        # return str(terms)

    @app.route("/terms", methods=["POST"])
    def create_term() -> (
        Tuple[Response, Union[Literal[201], Literal[400], Literal[500]]]
    ):
        """
        Creates a new Term in the glossary database.

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
            near_synonym_en=data.get("near_synonym_en"),
            near_synonym_fr=data.get("near_synonym_fr"),
            definition_en=data.get("definition_en"),
            definition_fr=data.get("definition_fr"),
            syntactic_cooccurrence_en=data.get("syntactic_cooccurrence_en"),
            syntactic_cooccurrence_fr=data.get("syntactic_cooccurrence_fr"),
            lexical_relations_en=data.get("lexical_relations_en"),
            lexical_relations_fr=data.get("lexical_relations_fr"),
            note_en=data.get("note_en"),
            note_fr=data.get("note_fr"),
            not_to_be_confused_with_en=data.get("not_to_be_confused_with_en"),
            not_to_be_confused_with_fr=data.get("not_to_be_confused_with_fr"),
            frequent_expression_en=data.get("frequent_expression_en"),
            frequent_expression_fr=data.get("frequent_expression_fr"),
            phraseology_en=data.get("phraseology_en"),
            phraseology_fr=data.get("phraseology_fr"),
            context_en=data.get("context_en"),
            context_fr=data.get("context_fr"),
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
                    "term_id": term.tid,
                    "english_term": term.english_term,
                    "french_term": term.french_term,
                }
            ),
            201,
        )

    @app.route("/terms", methods=["GET"])
    def get_terms() -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Retrieves all Terms in the glossary database.

        Input:  Nothing
        Output: (Response) | a JSON response with all Terms or an error message.
        """
        try:
            # Fetch all the records of the table 'terms' in the database
            terms = Term.query.all()
            if not terms:
                return jsonify({"message": "No Terms found."}), 404

            # Create a list of dictionaries representing each term
            terms_list: List[Dict[str, Union[int, str]]] = [
                {
                    "term_id": term.tid,
                    "english_term": term.english_term,
                    "french_term": term.french_term,
                    "variant_en": term.variant_en,
                    "variant_fr": term.variant_fr,
                    "near_synonym_en": term.near_synonym_en,
                    "near_synonym_fr": term.near_synonym_fr,
                    "definition_en": term.definition_en,
                    "definition_fr": term.definition_fr,
                    "syntactic_cooccurrence_en": term.syntactic_cooccurrence_en,
                    "syntactic_cooccurrence_fr": term.syntactic_cooccurrence_fr,
                    "lexical_relations_en": term.lexical_relations_en,
                    "lexical_relations_fr": term.lexical_relations_fr,
                    "note_en": term.note_en,
                    "note_fr": term.note_fr,
                    "not_to_be_confused_with_en": term.not_to_be_confused_with_en,
                    "not_to_be_confused_with_fr": term.not_to_be_confused_with_fr,
                    "frequent_expression_en": term.frequent_expression_en,
                    "frequent_expression_fr": term.frequent_expression_fr,
                    "phraseology_en": term.phraseology_en,
                    "phraseology_fr": term.phraseology_fr,
                    "context_en": term.context_en,
                    "context_fr": term.context_fr,
                }
                for term in terms
            ]

            return jsonify(terms_list), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/<int:tid>", methods=["GET"])
    def get_term(
        tid: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Retrieves a single Term by its ID.

        Input:  (int) tid   | the ID of the term to retrieve.
        Output: (Response)  | a JSON response with the Term details or an error message.
        """
        try:
            # Fetch the Term with the given term ID
            term = Term.query.get(tid)
            if not term:
                return jsonify({"error": f"Term with ID {tid} not found."}), 404

            # Create a dictionary representing the term
            term_data: Dict[str, Union[int, str]] = {
                "term_id": term.tid,
                "english_term": term.english_term,
                "french_term": term.french_term,
                "variant_en": term.variant_en,
                "variant_fr": term.variant_fr,
                "near_synonym_en": term.near_synonym_en,
                "near_synonym_fr":en": term.near_synonym_fr,
                "definition_en": term.definition_en,
                "definition_fr": term.definition_fr,
                "syntactic_cooccurrence_en": term.syntactic_cooccurrence_en,
                "syntactic_cooccurrence_fr": term.syntactic_cooccurrence_fr,
                "lexical_relations_en": term.lexical_relations_en,
                "lexical_relations_fr": term.lexical_relations_fr,
                "note_en": term.note_en,
                "note_fr": term.note_fr,
                "not_to_be_confused_with_en": term.not_to_be_confused_with_en,
                "not_to_be_confused_with_fr": term.not_to_be_confused_with_fr,
                "frequent_expression_en": term.frequent_expression_en,
                "frequent_expression_fr": term.frequent_expression_fr,
                "phraseology_en": term.phraseology_en,
                "phraseology_fr": term.phraseology_fr,
                "context_en": term.context_en,
                "context_fr": term.context_fr,
            }

            return jsonify(term_data), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/<int:tid>", methods=["PUT"])
    def update_term(
        tid: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[400], Literal[404], Literal[500]]]:
        """
        Updates an existing Term by its ID.
        PUT /terms/<int:tid>

        Input:  (int) tid   | the ID of the term to update.
                JSON body with the fields to update.
        Output: (Response) | a JSON response with the updated Term or an error message.
        """
        # Get the JSON data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        # Validate required fields
        english_term: str = data.get("english_term")
        french_term: str = data.get("french_term")

        if not english_term:
            return jsonify({"error": "English Term is required."}), 400
        if not french_term:
            return jsonify({"error": "French Term is required."}), 400

        if english_term is not None and not isinstance(english_term, str):
            return (
                jsonify(
                    {"error": "Invalid data type: English term should be a string"}
                ),
                400,
            )
        if french_term is not None and not isinstance(french_term, str):
            return (
                jsonify({"error": "Invalid data type: French term should be a string"}),
                400,
            )

        try:
            term = Term.query.get(tid)
            if not term:
                return jsonify({"error": f"Term with ID {tid} not found."}), 404

            # Update the term fields
            if english_term is not None:
                term.english_term = english_term.strip()
            if french_term is not None:
                term.french_term = french_term.strip()
            if "variant_en" in data:
                term.variant_en = data.get("variant_en")
            if "variant_fr" in data:
                term.variant_fr = data.get("variant_fr")
            if "synonyms_en" in data:
                term.synonyms_en = data.get("synonyms_en")
            if "synonyms_fr" in data:
                term.synonyms_fr = data.get("synonyms_fr")
            if "definition_en" in data:
                term.definition_en = data.get("definition_en")
            if "definition_fr" in data:
                term.definition_fr = data.get("definition_fr")
            if "syntactic_cooccurrence_en" in data:
                term.syntactic_cooccurrence_en = data.get("syntactic_cooccurrence_en")
            if "syntactic_cooccurrence_fr" in data:
                term.syntactic_cooccurrence_fr = data.get("syntactic_cooccurrence_fr")
            if "lexical_relations_en" in data:
                term.lexical_relations_en = data.get("lexical_relations_en")
            if "lexical_relations_fr" in data:
                term.lexical_relations_fr = data.get("lexical_relations_fr")
            if "phraseology_en" in data:
                term.phraseology_en = data.get("phraseology_en")
            if "phraseology_fr" in data:
                term.phraseology_fr = data.get("phraseology_fr")
            if "related_term_en" in data:
                term.related_term_en = data.get("related_term_en")
            if "related_term_fr" in data:
                term.related_term_fr = data.get("related_term_fr")
            if "contexts_en" in data:
                term.contexts_en = data.get("contexts_en")
            if "contexts_fr" in data:
                term.contexts_fr = data.get("contexts_fr")
            if "frequent_expression_en" in data:
                term.frequent_expression_en = data.get("frequent_expression_en")
            if "frequent_expression_fr" in data:
                term.frequent_expression_fr = data.get("frequent_expression_fr")

            db.session.commit()

            return (
                jsonify(
                    {
                        "message": "Term updated successfully!",
                        "term_id": term.tid,
                        "english_term": term.english_term,
                        "french_term": term.french_term,
                        "variant_en": term.variant_en,
                        "variant_fr": term.variant_fr,
                        "synonyms_en": term.synonyms_en,
                        "synonyms_fr": term.synonyms_fr,
                        "definition_en": term.definition_en,
                        "definition_fr": term.definition_en,
                        "syntactic_cooccurrence_en": term.syntactic_cooccurrence_en,
                        "syntactic_cooccurrence_fr": term.syntactic_cooccurrence_fr,
                        "lexical_relations_en": term.lexical_relations_en,
                        "lexical_relations_fr": term.lexical_relations_fr,
                        "phraseology_en": term.phraseology_en,
                        "phraseology_fr": term.phraseology_fr,
                        "related_term_en": term.related_term_en,
                        "related_term_fr": term.related_term_fr,
                        "contexts_en": term.contexts_en,
                        "contexts_fr": term.contexts_fr,
                        "frequent_expression_en": term.frequent_expression_en,
                        "frequent_expression_fr": term.frequent_expression_fr,
                    }
                ),
                200,
            )
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Integrity error occurred."}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/<int:tid>", methods=["DELETE"])
    def delete_term(
        tid: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Deletes an existing Term by its ID.
        DELETE /terms/<int:tid>

        Input:  (int) tid   | the ID of the term to delete.
        Output: (Response)  | a JSON response confirming deletion or an error message.
        """
        try:
            term = Term.query.get(tid)
            if not term:
                return jsonify({"error": f"Term with ID {tid} not found."}), 404

            db.session.delete(term)
            db.session.commit()

            return jsonify({"message": "Term deleted successfully!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
