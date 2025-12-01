#!/usr/bin/env python3
"""
Glossary Extraction Module
Extracts glossary terms from Industry 4.0 DOCX documents.

Author: Industry 4.0 Team
Version: 1.0.0
"""

import re
from typing import List, Dict, Optional
from docx import Document
from docx.table import Table


class GlossaryExtractor:
    """Extracts glossary terms and definitions from DOCX documents."""

    def __init__(self):
        self.glossary_markers = [
            'glossário', 'glossario', 'glossary',
            'termo', 'termos', 'term', 'terms',
            'definição', 'definicao', 'definition'
        ]

    def extract_from_document(self, doc: Document) -> List[Dict[str, str]]:
        """
        Extract glossary from entire document.

        Args:
            doc: python-docx Document object

        Returns:
            List of dicts with 'term' and 'definition' keys
        """
        glossary = []

        # Check all tables for glossary
        for table in doc.tables:
            table_glossary = self.extract_from_table(table)
            if table_glossary:
                glossary.extend(table_glossary)

        return glossary

    def extract_from_table(self, table: Table) -> Optional[List[Dict[str, str]]]:
        """
        Extract glossary from a single table.

        Args:
            table: python-docx Table object

        Returns:
            List of glossary entries or None if not a glossary table
        """
        if not self._is_glossary_table(table):
            return None

        glossary = []

        # Skip header row (first row)
        for row in table.rows[1:]:
            cells = row.cells

            if len(cells) < 2:
                continue

            term = self._clean_text(cells[0].text)
            definition = self._clean_text(cells[1].text)

            # Validate entry
            if self._is_valid_entry(term, definition):
                glossary.append({
                    'term': term,
                    'definition': definition
                })

        return glossary if glossary else None

    def _is_glossary_table(self, table: Table) -> bool:
        """Check if table is a glossary table."""
        if len(table.rows) < 2:  # Must have header + at least one entry
            return False

        # Check first row for glossary markers
        first_row_text = ' '.join([
            cell.text.lower() for cell in table.rows[0].cells
        ])

        return any(marker in first_row_text for marker in self.glossary_markers)

    def _is_valid_entry(self, term: str, definition: str) -> bool:
        """Validate that term and definition are legitimate entries."""
        if not term or not definition:
            return False

        # Filter out header-like entries
        term_lower = term.lower()
        if term_lower in ['termo', 'term', 'termos', 'terms']:
            return False

        # Filter out very short entries (likely fragments)
        if len(term) < 2 or len(definition) < 10:
            return False

        return True

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove markdown-like asterisks and bold markers
        text = re.sub(r'\*+', '', text)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text


def extract_glossary_from_document(doc: Document) -> List[Dict[str, str]]:
    """
    Convenience function to extract glossary from a document.

    Args:
        doc: python-docx Document object

    Returns:
        List of glossary entries
    """
    extractor = GlossaryExtractor()
    return extractor.extract_from_document(doc)


if __name__ == '__main__':
    # Test the extractor
    import sys
    from pathlib import Path

    if len(sys.argv) > 1:
        docx_path = Path(sys.argv[1])
        if docx_path.exists():
            doc = Document(str(docx_path))
            extractor = GlossaryExtractor()
            glossary = extractor.extract_from_document(doc)

            print(f"Found {len(glossary)} glossary terms:")
            for entry in glossary[:5]:  # Show first 5
                print(f"  • {entry['term']}: {entry['definition'][:60]}...")
        else:
            print(f"File not found: {docx_path}")
    else:
        print("Glossary Extractor Module - Ready")
        print("Usage: python extract_glossary.py <docx_file>")
        print("   Or: from extract_glossary import GlossaryExtractor")
