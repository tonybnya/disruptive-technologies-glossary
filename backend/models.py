"""
This file contains the models for the database.
"""

from __future__ import annotations

from typing import Dict, Union

from app import db


class EnglishTerm(db.Model):
    """
    Define a class for an English term model of the glossary database.
    Each term in the glossary is represented with both English & French equivalents.

    Attributes:
        english_term_id (int): The primary key for the English term.
        english_term (str): The English term.
        variant_en (str): Variant of the Term in English.
        synonyms_en (str): Synonyms of the term in English.
        definition_en (str): Definition of the term in English.
        syntactic_cooccurrence_en (str): Syntactic cooccurrence information in English.
        lexical_relations_en (str): Lexical relationships in English.
        phraseology_en (str): Phraseology information in English.
        related_term_en (str): Related term in English.
        contexts_en (str): Contexts in English.
        frequent_expression_en (str): Frequent expressions in English.
    """

    # Name of the table in the database
    __tablename__ = "english_terms"

    # Fields in the database for the english_terms table, their data types, and constraints
    english_term_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    english_term: str = db.Column(db.String(255), unique=True, nullable=False)
    variant_en: str = db.Column(db.String(255))
    synonyms_en: str = db.Column(db.String(255))
    definition_en: str = db.Column(db.Text)
    syntactic_cooccurrence_en: str = db.Column(db.Text)
    lexical_relations_en: str = db.Column(db.JSON)
    phraseology_en: str = db.Column(db.Text)
    related_term_en: str = db.Column(db.String(255))
    contexts_en: str = db.Column(db.Text)
    frequent_expression_en: str = db.Column(db.Text)

    # This constraint is to avoid multiple occurrences of the same English term
    __table_args__ = (db.UniqueConstraint("english_term", name="unique_terms"),)

    # Add relationship between EnglishTerm and FrenchTerm models
    french_term_id = db.Column(
        db.Integer, db.ForeignKey("french_terms.french_term_id"), nullable=True
    )
    french_term = db.relationship("FrenchTerm", back_populates="english_term")

    def __repr__(self) -> str:
        """
        Returns a string representation of the English Term instance.

        Input:  self (Term) | the English term instance
        Output: the string representation of the English term.
        """
        return f"English Term ID: {self.english_term_id} - English Term: {self.english_term}"

    def to_dict(self) -> Dict[str, Union[str, int, Dict[str, str]]]:
        """
        Conversts the English term model into a dictionary
        for easy JSON serialization.

        Input:  self (EnglishTerm) | the English term instance
        Output: a dictionary representing the English term
        """
        return {
            "english_term_id": self.english_term_id,
            "english_term": self.english_term,
            "variant_en": self.variant_en,
            "synonyms_en": self.synonyms_en,
            "definition_en": self.definition_en,
            "syntactic_cooccurrence_en": self.syntactic_cooccurrence_en,
            "lexical_relations_en": self.lexical_relations_en,
            "phraseology_en": self.phraseology_en,
            "related_term_en": self.related_term_en,
            "contexts_en": self.contexts_en,
            "frequent_expression_en": self.frequent_expression_en,
        }


class FrenchTerm(db.Model):
    """
    Define a class for an French term model of the glossary database.
    Each term in the glossary is represented with both English & French equivalents.

    Attributes:
        french_term_id (int): The primary key for the French term.
        french_term (str): The French term.
        variant_fr (str): Variant of the Term in French.
        synonyms_fr (str): Synonyms of the term in French.
        definition_fr (str): Definition of the term in French.
        syntactic_cooccurrence_fr (str): Syntactic cooccurrence information in French.
        lexical_relations_fr (str): Lexical relationships in French.
        phraseology_fr (str): Phraseology information in French.
        related_term_fr (str): Related term in French.
        contexts_fr (str): Contexts in French.
        frequent_expression_fr (str): Frequent expressions in French.
    """

    # Name of the table in the database
    __tablename__ = "french_terms"

    # Fields in the database for the french_terms table, their data types, and constraints
    french_term_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    french_term: str = db.Column(db.String(255), unique=True, nullable=False)
    variant_fr: str = db.Column(db.String(255))
    synonyms_fr: str = db.Column(db.String(255))
    definition_fr: str = db.Column(db.Text)
    syntactic_cooccurrence_fr: str = db.Column(db.Text)
    lexical_relations_fr: str = db.Column(db.JSON)
    phraseology_fr: str = db.Column(db.Text)
    related_term_fr: str = db.Column(db.String(255))
    contexts_fr: str = db.Column(db.Text)
    frequent_expression_fr: str = db.Column(db.Text)

    # This constraint is to avoid multiple occurrences of the same French term
    __table_args__ = (db.UniqueConstraint("french_term", name="unique_terms"),)

    # Link FrenchTerm to the EnglishTerm model
    english_term = db.relationship(
        "EnglishTerm", back_populates="french_term", uselist=False
    )

    def __repr__(self) -> str:
        """
        Returns a string representation of the French Term instance.

        Input:  self (Term) | the French term instance
        Output: the string representation of the French term.
        """
        return (
            f"French Term ID: {self.french_term_id} - French Term: {self.french_term}"
        )

    def to_dict(self) -> Dict[str, Union[str, int, Dict[str, str]]]:
        """
        Conversts the French term model into a dictionary
        for easy JSON serialization.

        Input:  self (French) | the French term instance
        Output: a dictionary representing the French term
        """
        return {
            "french_term_id": self.french_term_id,
            "french_term": self.french_term,
            "variant_fr": self.variant_fr,
            "synonyms_fr": self.synonyms_fr,
            "definition_fr": self.definition_fr,
            "syntactic_cooccurrence_fr": self.syntactic_cooccurrence_fr,
            "lexical_relations_fr": self.lexical_relations_fr,
            "phraseology_fr": self.phraseology_fr,
            "related_term_fr": self.related_term_fr,
            "contexts_fr": self.contexts_fr,
            "frequent_expression_fr": self.frequent_expression_fr,
        }
