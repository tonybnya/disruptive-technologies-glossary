"""
This file contains the models for the database.
"""

from __future__ import annotations

from typing import Dict, List

from app import db


class Term(db.Model):
    """
    Define a class for a Term model of the glossary database.
    Each Term in the glossary is represented with both English & French equivalents.

    Attributes:
        domain (str): The domain to which all terms belong.

        subdomains (list): Subdomains to which the term belongs.
                           If not specified, belongs to 'Big Data', 'AI', and 'Blockchain'.

        tid (int): The primary key for the term.

        english_term (str): The English term.
        french_term (str): The French equivalent of the English term.

        variant_en (str): Variant of the term in English.
        variant_fr (str): Variant of the term in French.

        near_synonym_en (str): Near synonym of the term in English.
        near_synonym_fr (str): Near synonym of the term in French.

        definition_en (str): Definition of the term in English.
        definition_fr (str): Definition of the term in French.

        syntactic_cooccurrence_en (list): Syntactic cooccurrence information in English.
        syntactic_cooccurrence_fr (list): Syntactic cooccurrence information in French.

        lexical_relations_en (dict): Lexical relationships in English.
        lexical_relations_fr (dict): Lexical relationships in French.

        note_en (str): Note about the term in English.
        note_fr (str): Note about the term in French.

        not_to_be_confused_with_en (str): expression not to be confused with the term in English.
        not_to_be_confused_with_fr (str): expression not to be confused with the term in French.

        frequent_expression_en (str): Frequent expressions in English.
        frequent_expression_fr (str): Frequent expressions in French.

        phraseology_en (str): Phraseology information in English.
        phraseology_fr (str): Phraseology information in French.

        context_en (str): Context in English.
        context_fr (str): Context in French.
    """

    # Define the name of the table in the database
    __tablename__ = "terms"

    # Class attribute
    # Each single term in the database belongs to this domain
    domain: str = "Technologies Transformatrices"

    # New class attribute for subdomains
    subdomains: List[str] = ["Big Data", "AI", "Blockchain"]

    tid: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    english_term: str = db.Column(db.String(255), unique=True, nullable=False)
    french_term: str = db.Column(db.String(255), unique=True, nullable=False)

    variant_en: str = db.Column(db.String(255))
    variant_fr: str = db.Column(db.String(255))

    near_synonym_en: str = db.Column(db.String(255))
    near_synonym_fr: str = db.Column(db.String(255))

    definition_en: str = db.Column(db.Text)
    definition_fr: str = db.Column(db.Text)

    syntactic_cooccurrence_en: List[str] = db.Column(db.JSON)
    syntactic_cooccurrence_fr: List[str] = db.Column(db.JSON)

    lexical_relations_en: Dict[str, List[str]] = db.Column(db.JSON)
    lexical_relations_fr: Dict[str, List[str]] = db.Column(db.JSON)

    note_en: str = db.Column(db.Text)
    note_fr: str = db.Column(db.Text)

    not_to_be_confused_with_en: str = db.Column(db.String(255))
    not_to_be_confused_with_fr: str = db.Column(db.String(255))

    frequent_expression_en: str = db.Column(db.Text)
    frequent_expression_fr: str = db.Column(db.Text)

    phraseology_en: str = db.Column(db.Text)
    phraseology_fr: str = db.Column(db.Text)

    context_en: str = db.Column(db.Text)
    context_fr: str = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("english_term", "french_term", name="unique_terms"),
    )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Term instance.

        Input:  self (Term) | the Term instance
        Output: the string representation of the term.
        """
        return f"Term ID: {self.tid} - English Term: {self.english_term} - French Term: {self.french_term}"
