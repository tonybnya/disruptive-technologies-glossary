"""
This file contains the models for the database.
"""

from app import db


class Term(db.Model):
    """
    Define a class for a Term model of the glossary database.
    Each Term in the glossary is represented with both English & French equivalents.

    Attributes:
        tid (int): The primary key for the term.

        english_term (str): The English term.
        french_term (str): The French equivalent of the English term.

        variant_en (str): Variant of the term in English.
        variant_fr (str): Variant of the term in French.

        synonyms_en (str): Synonyms of the term in English.
        synonyms_fr (str): Synonyms of the term in French.

        definition_en (str): Definition of the term in English.
        definition_fr (str): Definition of the term in French.

        syntactic_cooccurrence_en (str): Syntactic cooccurrence information in English.
        syntactic_cooccurrence_fr (str): Syntactic cooccurrence information in French.

        lexical_relations_en (str): Lexical relationships in English.
        lexical_relations_fr (str): Lexical relationships in French.

        phraseology_en (str): Phraseology information in English.
        phraseology_fr (str): Phraseology information in French.

        related_term_en (str): Related term in English.
        related_term_fr (str): Related term in French.

        contexts_en (str): Contexts in English.
        contexts_fr (str): Contexts in French.

        frequent_expression_en (str): Frequent expressions in English.
        frequent_expression_fr (str): Frequent expressions in French.
    """

    __tablename__ = "terms"

    tid: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    english_term: str = db.Column(db.String(255), nullable=False)
    french_term: str = db.Column(db.String(255), nullable=False)

    variant_en: str = db.Column(db.String(255))
    variant_fr: str = db.Column(db.String(255))

    synonyms_en: str = db.Column(db.String(255))
    synonyms_fr: str = db.Column(db.String(255))

    definition_en: str = db.Column(db.Text)
    definition_fr: str = db.Column(db.Text)

    syntactic_cooccurrence_en: str = db.Column(db.Text)
    syntactic_cooccurrence_fr: str = db.Column(db.Text)

    lexical_relations_en: str = db.Column(db.Text)
    lexical_relations_fr: str = db.Column(db.Text)

    phraseology_en: str = db.Column(db.Text)
    phraseology_fr: str = db.Column(db.Text)

    related_term_en: str = db.Column(db.String(255))
    related_term_fr: str = db.Column(db.String(255))

    contexts_en: str = db.Column(db.Text)
    contexts_fr: str = db.Column(db.Text)

    frequent_expression_en: str = db.Column(db.Text)
    frequent_expression_fr: str = db.Column(db.Text)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Term instance.

        Input:  self (Term) | the Term instance
        Output: the string representation of the term.
        """
        return f"<Term {self.english_term} - {self.french_term}>"
