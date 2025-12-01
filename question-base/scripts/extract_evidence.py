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

        found_evidence = False

        for row in table.rows:
            cells = row.cells
            if len(cells) < 1:
                continue

            cell_text = self._clean_text(cells[0].text)

            # Check if this row contains evidence
            if self._is_evidence_row(cell_text):
                found_evidence = True
                # Get the content (usually in the same or next cell)
                content = cell_text
                if len(cells) >= 2:
                    content = self._clean_text(cells[1].text)

                # Parse the evidence content
                self._parse_evidence_content(content, evidence)

        return evidence if found_evidence else None

    def _is_evidence_row(self, text: str) -> bool:
        """Check if row contains evidence markers."""
        text_lower = text.lower()
        return any(marker in text_lower for marker in self.evidence_markers)

    def _parse_evidence_content(self, content: str, evidence: Dict):
        """Parse evidence content into structured format."""
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
        """Extract list items from text (marked with ** or bullets)."""
        items = []

        # Split by ** markers (bold markers in markdown-like format)
        parts = re.split(r'\*\*+', text)
        for part in parts:
            part = self._clean_text(part)
            if part and len(part) > 5:  # Ignore very short fragments
                items.append(part)

        # Also try splitting by newlines with bullets
        lines = text.split('\n')
        for line in lines:
            line = self._clean_text(line)
            if line and (line.startswith('-') or line.startswith('•')):
                line = line.lstrip('-•').strip()
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

    def _extract_signals_by_level(self, text: str) -> Dict[str, str]:
        """Extract signals organized by maturity level (N0, N1, etc.)."""
        signals = {}

        # Find patterns like N0:, N1:, etc.
        pattern = r'N(\d):\s*(.*?)(?=N\d:|$)'
        matches = re.finditer(pattern, text, re.DOTALL)

        for match in matches:
            level = f"N{match.group(1)}"
            description = self._clean_text(match.group(2))
            if description:
                signals[level] = description

        return signals

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
