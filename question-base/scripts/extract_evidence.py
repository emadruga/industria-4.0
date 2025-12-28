#!/usr/bin/env python3
"""
Evidence Sources Extraction Module
Extracts evidence sources from Industry 4.0 DOCX question documents.

Author: Industry 4.0 Team
Version: 1.0.0
"""

import re
from typing import Dict, List, Optional
from docx.table import Table


class EvidenceExtractor:
    """Extracts evidence sources from question tables."""

    def __init__(self):
        self.evidence_markers = [
            'evidência', 'evidencia', 'evidence',
            'fontes de evidências', 'fontes de evidencias',
            'possíveis fontes', 'possiveis fontes'
        ]

    def extract_from_table(self, table: Table) -> Optional[Dict[str, any]]:
        """
        Extract evidence sources from a table.

        Handles two table formats:
        1. Single-row format: Evidence content in one cell
        2. Multi-row format: Evidence content spread across multiple rows

        Returns:
            Dict with artifacts, metrics, signals_by_level, sampling_guidance
            or None if no evidence found
        """
        evidence = {
            'artifacts': [],
            'metrics': [],
            'signals_by_level': {},
            'sampling_guidance': ''
        }

        # First, check if this is an evidence table by concatenating all cells
        full_table_text = ""
        for row in table.rows:
            for cell in row.cells:
                full_table_text += cell.text + "\n"

        # Check if this table contains evidence markers
        if not self._is_evidence_row(full_table_text):
            return None

        # This is an evidence table - parse the full concatenated content
        self._parse_evidence_content(full_table_text, evidence)

        # Only return if we actually found some evidence
        if (evidence['artifacts'] or evidence['metrics'] or
            evidence['signals_by_level'] or evidence['sampling_guidance']):
            return evidence

        return None

    def _is_evidence_row(self, text: str) -> bool:
        """Check if row contains evidence markers."""
        text_lower = text.lower()
        return any(marker in text_lower for marker in self.evidence_markers)

    def _parse_evidence_content(self, content: str, evidence: Dict):
        """
        Parse evidence content into structured format.

        Uses hybrid approach:
        - Section A (Artefatos): General artifacts that apply to all levels
        - Section B (Métricas): General metrics that apply to all levels
        - Section C (Sinais por nível): Level-specific observable behaviors
        - Section D (Amostragem): Sampling guidance

        Sections A & B are stored at the top level and will be mapped to
        all maturity levels during JSON conversion.
        """
        # Look for sections A), B), C), D)

        # A) Artifacts (Artefatos)
        artifacts_match = re.search(
            r'A\)(.*?)(?:B\)|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if artifacts_match:
            artifacts_text = artifacts_match.group(1)
            artifacts = self._extract_list_items(artifacts_text)
            evidence['artifacts'].extend(artifacts)

        # B) Metrics (Métricas/KPIs)
        metrics_match = re.search(
            r'B\)(.*?)(?:C\)|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if metrics_match:
            metrics_text = metrics_match.group(1)
            metrics = self._extract_list_items(metrics_text)
            evidence['metrics'].extend(metrics)

        # C) Signals by level (Sinais por nível)
        # This section contains level-specific observable behaviors
        signals_match = re.search(
            r'C\)(.*?)(?:D\)|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if signals_match:
            signals_text = signals_match.group(1)
            signals = self._extract_signals_by_level(signals_text)
            evidence['signals_by_level'].update(signals)

        # D) Sampling guidance (Amostragem)
        sampling_match = re.search(
            r'D\)(.*?)$',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if sampling_match:
            sampling_text = sampling_match.group(1)
            evidence['sampling_guidance'] = self._clean_text(sampling_text)

    def _extract_list_items(self, text: str) -> List[str]:
        """
        Extract list items from text.

        Handles multiple formats:
        1. Bold markers (**item**)
        2. Bullet points (- item or • item)
        3. Newline-separated items (one item per line)
        """
        items = []

        # Split by ** markers (bold markers in markdown-like format)
        parts = re.split(r'\*\*+', text)
        for part in parts:
            part = self._clean_text(part)
            if part and len(part) > 5:  # Ignore very short fragments
                items.append(part)

        # If no ** markers found, try other formats
        if not items:
            lines = text.split('\n')
            for line in lines:
                line = self._clean_text(line)

                # Skip empty lines and section headers
                if not line or len(line) < 5:
                    continue

                # Skip if line looks like a section header
                if re.match(r'^[A-D]\)', line, re.IGNORECASE):
                    continue
                if re.match(r'^(Artefatos|Métricas|KPIs|Sinais|Comportamentos|Perguntas|Amostragem)', line, re.IGNORECASE):
                    continue

                # Remove bullet markers if present
                if line.startswith('-') or line.startswith('•'):
                    line = line.lstrip('-•').strip()

                # Add if meaningful content
                if line and len(line) > 5:
                    items.append(line)

        # Remove duplicates while preserving order
        seen = set()
        unique_items = []
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)

        return unique_items

    def _extract_signals_by_level(self, text: str) -> Dict[str, Dict]:
        """
        Extract detailed signals organized by maturity level.

        Supports two formats:
        1. Structured format with subsections (Artefatos:, Métricas:, etc.)
        2. Prose format with semicolon-separated observable behaviors

        Returns:
            {
                "N0": {
                    "artifacts": [...],
                    "metrics": [...],
                    "observable_behaviors": [...],
                    "interview_questions": [...]
                },
                "N1": {...}
            }
        """
        signals = {}

        # Find patterns like N0:, N1:, etc.
        pattern = r'N(\d):\s*(.*?)(?=N\d:|$)'
        matches = re.finditer(pattern, text, re.DOTALL)

        for match in matches:
            level = f"N{match.group(1)}"
            content = match.group(2).strip()

            # Try structured format first (with subsection headers)
            artifacts = self._extract_subsection(content, r"Artefatos|Artifacts")
            metrics = self._extract_subsection(content, r"Métricas|KPIs|Metrics")
            behaviors = self._extract_subsection(
                content,
                r"Comportamentos|Sinais|Observable|Behaviors|Comportamentos Observáveis"
            )
            questions = self._extract_subsection(
                content,
                r"Perguntas|Questions|Interview|Perguntas para Entrevista"
            )

            # If no subsections found, treat entire content as prose observable behaviors
            if not any([artifacts, metrics, behaviors, questions]):
                # Parse prose format: split by semicolons and periods
                behaviors = self._parse_prose_behaviors(content)

            signals[level] = {
                "artifacts": artifacts,
                "metrics": metrics,
                "observable_behaviors": behaviors,
                "interview_questions": questions
            }

        return signals

    def _parse_prose_behaviors(self, text: str) -> List[str]:
        """
        Parse prose format observable behaviors.

        Handles format like:
        "liderança desconhece práticas ágeis; sem menção em estratégia."

        Splits by semicolons and periods to extract individual behaviors.

        Args:
            text: Prose text with semicolon/period-separated behaviors

        Returns:
            List of observable behavior strings
        """
        behaviors = []

        # Clean up the text first
        text = self._clean_text(text)

        # Split by semicolons first (primary delimiter)
        parts = re.split(r';', text)

        for part in parts:
            # Further split by periods (sentence boundaries)
            sentences = re.split(r'\.', part)
            for sentence in sentences:
                sentence = sentence.strip()
                # Filter out very short fragments (likely noise)
                if sentence and len(sentence) > 10:
                    behaviors.append(sentence)

        return behaviors

    def _extract_subsection(self, text: str, section_pattern: str) -> List[str]:
        """
        Extract list items from a named subsection.

        Args:
            text: The text to search
            section_pattern: Regex pattern for section headers

        Returns:
            List of extracted items
        """
        # Look for section header followed by list items
        pattern = f"({section_pattern}):\\s*(.*?)(?=\\n\\s*(?:Artefatos|Métricas|KPIs|Comportamentos|Sinais|Perguntas|Observable|Behaviors|Metrics|Artifacts|Questions|Interview)|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

        if not match:
            return []

        content = match.group(2)
        return self._extract_list_items(content)

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove markdown-like asterisks
        text = re.sub(r'\*+', '', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Remove leading colons or semicolons
        text = text.lstrip(':;').strip()
        return text


def extract_evidence_from_table(table: Table) -> Optional[Dict[str, any]]:
    """
    Convenience function to extract evidence from a table.

    Args:
        table: A python-docx Table object

    Returns:
        Dict with evidence sources or None
    """
    extractor = EvidenceExtractor()
    return extractor.extract_from_table(table)


if __name__ == '__main__':
    # Test the extractor
    print("Evidence Extractor Module - Ready")
    print("Use: from extract_evidence import EvidenceExtractor")
