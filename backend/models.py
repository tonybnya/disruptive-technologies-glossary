"""
This file contains the models for the database.
"""

from __future__ import annotations

from typing import Any, Dict, List

from app import db


class Term(db.Model):
    """
    Define a class for a Term model of the glossary database.
    Each Term in the glossary is represented with both English & French equivalents.

    Attributes:
        tid (int): The primary key for the term.

        domain (str): The domain to which all terms belong.

        subdomains (list): Subdomains to which the term belongs.
                           If not specified, belongs to 'Big Data', 'AI', and 'Blockchain'.

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

    tid: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    domain: str = db.Column(db.String(255), nullable=False)
    subdomains: List[str] = db.Column(db.JSON)

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

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts models for easier JSON serialization.

        Input:  model (Term) | the instance of the Term
        Output: a dictionary representing the model
        """
        return {
            "tid": self.tid,
            "domain": self.domain,
            "subdomains": self.subdomains,
            "english_term": self.english_term,
            "french_term": self.french_term,
            "variant_en": self.variant_en,
            "variant_fr": self.variant_fr,
            "near_synonym_en": self.near_synonym_en,
            "near_synonym_fr": self.near_synonym_fr,
            "definition_en": self.definition_en,
            "definition_fr": self.definition_fr,
            "syntactic_cooccurrence_en": self.syntactic_cooccurrence_en,
            "syntactic_cooccurrence_fr": self.syntactic_cooccurrence_fr,
            "lexical_relations_en": self.lexical_relations_en,
            "lexical_relations_fr": self.lexical_relations_fr,
            "note_en": self.note_en,
            "note_fr": self.note_fr,
            "not_to_be_confused_with_en": self.not_to_be_confused_with_en,
            "not_to_be_confused_with_fr": self.not_to_be_confused_with_fr,
            "frequent_expression_en": self.frequent_expression_en,
            "frequent_expression_fr": self.frequent_expression_fr,
            "phraseology_en": self.phraseology_en,
            "phraseology_fr": self.phraseology_fr,
            "context_en": self.context_en,
            "context_fr": self.context_fr,
        }
