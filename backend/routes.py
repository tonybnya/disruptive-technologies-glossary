"""
This file defines the routes/endpoints for the API.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Tuple, Union

from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from models import EnglishTerm, FrenchTerm


def register_routes(app: Flask, db: SQLAlchemy):
    """
    Define and register the routes/endpoints of the API.

    Input:  app (Flask)     | the Flask application
    Input:  db (SQLAlchemy) | SQLAlchemy object for the database
    """

    #####################
    ###               ###
    ### Root endpoint ###
    ###               ###
    #####################

    @app.route("/")
    def root() -> Tuple[Response, Literal[200]]:
        """
        Define the default (root) endpoint "/".

        Input:  Nothing
        Output: a dictionary message
        """
        return (
            jsonify(
                {"message": "Welcome! This is a LEC-Glossary API on AI and Blockchain."}
            ),
            200,
        )

    ##############################
    ###                        ###
    ### English term endpoints ###
    ###                        ###
    ##############################

    @app.route("/terms/english", methods=["POST"])
    def create_english_term() -> (
        Tuple[Response, Union[Literal[201], Literal[400], Literal[500]]]
    ):
        """
        Creates a new English ierm in the glossary database.

        Input:  Nothing
        Output: (Response) | a JSON response with the created English term or an error message.
        """
        # Get the JSON data from the request body
        data = request.get_json()

        # Validate the presence of required data
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        english_term: str = data.get("english_term")

        if not english_term:
            return jsonify({"error": "English Term is required."}), 400

        # Validate data types of the the required fields
        if not isinstance(english_term, str):
            return (
                jsonify(
                    {"error": "Invalid data types: English terms should be a string."}
                ),
                400,
            )

        new_term: EnglishTerm = EnglishTerm(
            english_term=english_term.strip(),
            variant_en=data.get("variant_en"),
            synonyms_en=data.get("synonyms_en"),
            definition_en=data.get("definition_en"),
            syntactic_cooccurrence_en=data.get("syntactic_cooccurrence_en"),
            lexical_relations_en=data.get("lexical_relations_en"),
            phraseology_en=data.get("phraseology_en"),
            related_term_en=data.get("related_term_en"),
            contexts_en=data.get("contexts_en"),
            frequent_expression_en=data.get("frequent_expression_en"),
        )

        try:
            # Add the new term to the session
            db.session.add(new_term)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return (
                jsonify({"error": "This English term already exists."}),
                400,
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

        return (
            jsonify(
                {
                    "message": "English term created successfully!",
                    "english_term_id": new_term.english_term_id,
                    "english_term": new_term.english_term,
                }
            ),
            201,
        )

    @app.route("/terms/english", methods=["GET"])
    def get_all_english_terms() -> (
        Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]
    ):
        """
        Retrieves all English terms in the glossary database.

        Input:  Nothing
        Output: (Response) | a JSON response with all English terms or an error message.
        """
        try:
            # Fetch all the records of the table 'terms' in the database
            terms = EnglishTerm.query.all()
            if not terms:
                return jsonify({"message": "No English terms found."}), 404

            return jsonify([term.to_dict() for term in terms]), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/english/<int:english_term_id>", methods=["GET"])
    def get_english_term(
        english_term_id: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Retrieves a single English term by its ID.

        Input:  (int) english_term_id   | the ID of the English term to retrieve.
        Output: (Response)              | a JSON response with the English term details or an error message.
        """
        try:
            # Fetch the English term with the given term ID
            term = EnglishTerm.query.get(english_term_id)
            if not term:
                return (
                    jsonify(
                        {"error": f"English term with ID {english_term_id} not found."}
                    ),
                    404,
                )

            return jsonify(term.to_dict()), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/english/<int:english_term_id>", methods=["PUT"])
    def update_english_term(
        english_term_id: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[400], Literal[404], Literal[500]]]:
        """
        Updates an existing English term by its ID.

        Input:  (int) english_term_id   | the ID of the English term to update.
                request body with the fields to update.
        Output: (Response) | a JSON response with the updated English term or an error message.
        """
        # Get the JSON data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        # Validate required fields
        english_term: str = data.get("english_term")

        if not english_term:
            return jsonify({"error": "English Term is required."}), 400

        if english_term is not None and not isinstance(english_term, str):
            return (
                jsonify(
                    {"error": "Invalid data type: English term should be a string"}
                ),
                400,
            )

        try:
            term = EnglishTerm.query.get(english_term_id)
            if not term:
                return (
                    jsonify(
                        {"error": f"English term with ID {english_term_id} not found."}
                    ),
                    404,
                )

            # Update the term fields
            if english_term is not None:
                term.english_term = english_term.strip()
            if "variant_en" in data:
                term.variant_en = data.get("variant_en")
            if "synonyms_en" in data:
                term.synonyms_en = data.get("synonyms_en")
            if "definition_en" in data:
                term.definition_en = data.get("definition_en")
            if "syntactic_cooccurrence_en" in data:
                term.syntactic_cooccurrence_en = data.get("syntactic_cooccurrence_en")
            if "lexical_relations_en" in data:
                term.lexical_relations_en = data.get("lexical_relations_en")
            if "phraseology_en" in data:
                term.phraseology_en = data.get("phraseology_en")
            if "related_term_en" in data:
                term.related_term_en = data.get("related_term_en")
            if "contexts_en" in data:
                term.contexts_en = data.get("contexts_en")
            if "frequent_expression_en" in data:
                term.frequent_expression_en = data.get("frequent_expression_en")

            db.session.commit()

            return (
                jsonify(
                    {
                        "message": "English term updated successfully!",
                        "term": term.to_dict(),
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

    @app.route("/terms/english/<int:english_term_id>", methods=["DELETE"])
    def delete_english_term(
        english_term_id: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Deletes an existing English term by its ID.

        Input:  (int) english_term_id   | the ID of the English term to delete.
        Output: (Response)              | a JSON response confirming deletion or an error message.
        """
        try:
            term = EnglishTerm.query.get(english_term_id)
            if not term:
                return (
                    jsonify(
                        {"error": f"English term with ID {english_term_id} not found."}
                    ),
                    404,
                )

            db.session.delete(term)
            db.session.commit()

            return (
                jsonify(
                    {
                        "message": f"English term with ID {english_term_id} deleted successfully!"
                    }
                ),
                200,
            )

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    #############################
    ###                       ###
    ### French term endpoints ###
    ###                       ###
    #############################

    @app.route("/terms/french", methods=["POST"])
    def create_french_term() -> (
        Tuple[Response, Union[Literal[201], Literal[400], Literal[500]]]
    ):
        """
        Creates a new French term in the glossary database.

        Input:  Nothing
        Output: (Response) | a JSON response with the created French term or an error message.
        """
        # Get the JSON data from the request body
        data = request.get_json()

        # Validate the presence of required data
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        french_term: str = data.get("french_term")

        if not french_term:
            return jsonify({"error": "French Term is required."}), 400

        # Validate data types of the the required fields
        if not isinstance(french_term, str):
            return (
                jsonify(
                    {"error": "Invalid data types: French terms should be a string."}
                ),
                400,
            )

        new_term: FrenchTerm = FrenchTerm(
            french_term=french_term.strip(),
            variant_fr=data.get("variant_fr"),
            synonyms_fr=data.get("synonyms_fr"),
            definition_fr=data.get("definition_fr"),
            syntactic_cooccurrence_fr=data.get("syntactic_cooccurrence_fr"),
            lexical_relations_fr=data.get("lexical_relations_fr"),
            phraseology_fr=data.get("phraseology_fr"),
            related_term_fr=data.get("related_term_fr"),
            contexts_fr=data.get("contexts_fr"),
            frequent_expression_fr=data.get("frequent_expression_fr"),
        )

        try:
            # Add the new term to the session
            db.session.add(new_term)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return (
                jsonify({"error": "This French term already exists."}),
                400,
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

        return (
            jsonify(
                {
                    "message": "French term created successfully!",
                    "english_term_id": new_term.french_term_id,
                    "english_term": new_term.french_term,
                }
            ),
            201,
        )

    @app.route("/terms/french", methods=["GET"])
    def get_all_french_terms() -> (
        Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]
    ):
        """
        Retrieves all French terms in the glossary database.

        Input:  Nothing
        Output: (Response) | a JSON response with all French terms or an error message.
        """
        try:
            # Fetch all the records of the table 'terms' in the database
            terms = FrenchTerm.query.all()
            if not terms:
                return jsonify({"message": "No French terms found."}), 404

            return jsonify([term.to_dict() for term in terms]), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/french/<int:french_term_id>", methods=["GET"])
    def get_french_term(
        french_term_id: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Retrieves a single French term by its ID.

        Input:  (int) french_term_id    | the ID of the French term to retrieve.
        Output: (Response)              | a JSON response with the French term details or an error message.
        """
        try:
            # Fetch the French term with the given term ID
            term = FrenchTerm.query.get(french_term_id)
            if not term:
                return (
                    jsonify(
                        {"error": f"French term with ID {french_term_id} not found."}
                    ),
                    404,
                )

            return jsonify(term.to_dict()), 200

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    @app.route("/terms/french/<int:french_term_id>", methods=["PUT"])
    def update_french_term(
        french_term_id: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[400], Literal[404], Literal[500]]]:
        """
        Updates an existing French term by its ID.

        Input:  (int) french_term_id   | the ID of the French term to update.
                request body with the fields to update.
        Output: (Response) | a JSON response with the updated French term or an error message.
        """
        # Get the JSON data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        # Validate required fields
        french_term: str = data.get("french_term")

        if not french_term:
            return jsonify({"error": "French Term is required."}), 400

        if french_term is not None and not isinstance(french_term, str):
            return (
                jsonify({"error": "Invalid data type: French term should be a string"}),
                400,
            )

        try:
            term = FrenchTerm.query.get(french_term_id)
            if not term:
                return (
                    jsonify(
                        {"error": f"French term with ID {french_term_id} not found."}
                    ),
                    404,
                )

            # Update the term fields
            if french_term is not None:
                term.french_term = french_term.strip()
            if "variant_fr" in data:
                term.variant_fr = data.get("variant_fr")
            if "synonyms_fr" in data:
                term.synonyms_fr = data.get("synonyms_fr")
            if "definition_fr" in data:
                term.definition_fr = data.get("definition_fr")
            if "syntactic_cooccurrence_fr" in data:
                term.syntactic_cooccurrence_fr = data.get("syntactic_cooccurrence_fr")
            if "lexical_relations_fr" in data:
                term.lexical_relations_fr = data.get("lexical_relations_fr")
            if "phraseology_fr" in data:
                term.phraseology_fr = data.get("phraseology_fr")
            if "related_term_fr" in data:
                term.related_term_fr = data.get("related_term_fr")
            if "contexts_fr" in data:
                term.contexts_fr = data.get("contexts_fr")
            if "frequent_expression_fr" in data:
                term.frequent_expression_fr = data.get("frequent_expression_fr")

            db.session.commit()

            return (
                jsonify(
                    {
                        "message": "French term updated successfully!",
                        "term": term.to_dict(),
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

    @app.route("/terms/french/<int:french_term_id>", methods=["DELETE"])
    def delete_french_term(
        french_term_id: int,
    ) -> Tuple[Response, Union[Literal[200], Literal[404], Literal[500]]]:
        """
        Deletes an existing French term by its ID.

        Input:  (int) french_term_id   | the ID of the French term to delete.
        Output: (Response)              | a JSON response confirming deletion or an error message.
        """
        try:
            term = FrenchTerm.query.get(french_term_id)
            if not term:
                return (
                    jsonify(
                        {"error": f"French term with ID {french_term_id} not found."}
                    ),
                    404,
                )

            db.session.delete(term)
            db.session.commit()

            return (
                jsonify(
                    {
                        "message": f"French term with ID {french_term_id} deleted successfully!"
                    }
                ),
                200,
            )

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
