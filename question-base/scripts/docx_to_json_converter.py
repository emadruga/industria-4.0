#!/usr/bin/env python3
"""
DOCX to JSON Converter for Industry 4.0 Maturity Model Questions
Extracts structured question data from DOCX files into JSON format.

Author: Industry 4.0 Team
Version: 1.0.0
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    print("Error: python-docx is required. Install with: pip install python-docx")
    sys.exit(1)

# Import extraction modules
try:
    from extract_glossary import GlossaryExtractor
    from extract_references import ReferencesExtractor
    from extract_evidence import EvidenceExtractor
except ImportError:
    print("Warning: Extraction modules not found. Some features may be limited.")
    GlossaryExtractor = None
    ReferencesExtractor = None
    EvidenceExtractor = None


@dataclass
class MaturityLevel:
    """Represents a single maturity level."""
    level: int
    label: str
    description: str


@dataclass
class EvidenceSources:
    """Evidence sources for assessing a question."""
    artifacts: List[str]
    metrics: List[str]
    signals_by_level: Dict[str, str]
    sampling_guidance: str


@dataclass
class Question:
    """Represents a single assessment question."""
    id: str
    question_number: int
    title: str
    text: str
    maturity_levels: List[MaturityLevel]
    evidence_sources: Optional[EvidenceSources] = None
    notes: Optional[str] = None


@dataclass
class Metadata:
    """Metadata about the capacity."""
    source_frameworks: List[str]
    author: str
    version: str
    last_updated: str
    source_docx: str
    status: str = "draft"
    co_authors: Optional[List[str]] = None


@dataclass
class Capacity:
    """Represents a capacity with its questions."""
    id: str
    name: str
    block: str
    pilar: str
    dimension: str
    description: str
    related_capacities: List[str]
    metadata: Metadata


class DOCXToJSONConverter:
    """Converts Industry 4.0 DOCX files to structured JSON."""

    def __init__(self, docx_path: str, author: str = "Unknown"):
        self.docx_path = Path(docx_path)
        self.author = author
        self.doc = Document(str(self.docx_path))

        # Patterns for parsing
        self.question_pattern = re.compile(r'^[Qq]uest[ãa]o\s+(\d+)', re.IGNORECASE)
        self.maturity_level_pattern = re.compile(r'^(\d+)\s*$')

        # Initialize extraction modules
        self.glossary_extractor = GlossaryExtractor() if GlossaryExtractor else None
        self.references_extractor = ReferencesExtractor() if ReferencesExtractor else None
        self.evidence_extractor = EvidenceExtractor() if EvidenceExtractor else None

    def extract_table_data(self, table: Table) -> Dict[str, str]:
        """Extract key-value pairs from a table (handles both horizontal and vertical formats)."""
        data = {}
        rows = list(table.rows)

        for i, row in enumerate(rows):
            cells = row.cells
            if len(cells) >= 2:
                # Horizontal format: key in col 0, value in col 1
                key = self._clean_text(cells[0].text)
                value = self._clean_text(cells[1].text)
                if key and value:
                    data[key] = value
            elif len(cells) == 1:
                # Vertical format: check if this is a key and next row has value
                text = self._clean_text(cells[0].text)
                if text.endswith(':') and i + 1 < len(rows):
                    # This looks like a key, check next row for value
                    key = text.rstrip(':')
                    next_row_cells = rows[i + 1].cells
                    if len(next_row_cells) >= 1:
                        value = self._clean_text(next_row_cells[0].text)
                        if value:
                            data[key] = value
                elif text and not text.startswith('*'):
                    # Regular description text
                    data['_description'] = data.get('_description', '') + ' ' + text
        return data

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove markdown-like asterisks at start/end
        text = re.sub(r'^\*+|\*+$', '', text)
        # Remove italics/bold markers
        text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
        return text.strip()

    def _extract_capacity_info(self) -> Optional[Capacity]:
        """Extract capacity metadata from the document header tables."""
        capacity_data = {
            'dimension': '',
            'block': '',
            'pilar': '',
            'description': '',
            'related_capacities': [],
            'capacity_name': ''  # New: store explicit capacity name
        }

        # Search through tables at the beginning of the document
        for i, table in enumerate(self.doc.tables[:5]):  # Check first 5 tables
            table_data = self.extract_table_data(table)

            # Look for dimension
            if 'Dimensão' in table_data or 'Dimensao' in table_data:
                capacity_data['dimension'] = table_data.get('Dimensão', table_data.get('Dimensao', ''))

            # Look for block/pilar
            for key, value in table_data.items():
                if 'Bloco' in key:
                    capacity_data['block'] = value
                elif 'Pilar' in key:
                    capacity_data['pilar'] = value
                elif 'Capacidade' in key and 'Relacionada' not in key:
                    # Explicit capacity name field
                    capacity_data['capacity_name'] = value
                elif 'Resumo' in key or 'Descritivo' in key or key == '_description':
                    capacity_data['description'] += ' ' + value
                elif 'Capacidades Relacionadas' in key or 'Related' in key.lower():
                    # Split by semicolon or comma
                    caps = re.split(r'[;,]', value)
                    capacity_data['related_capacities'] = [c.strip() for c in caps if c.strip()]

        # Clean up description
        capacity_data['description'] = self._clean_text(capacity_data['description'])

        # Extract dimension from description if not found in table
        if not capacity_data['dimension'] and capacity_data['description']:
            dimension_match = re.search(
                r'Dimens[ãa]o:\s*([^()\n]+?)(?:\s*\([^)]*\))?\s*(?:Resumo|$)',
                capacity_data['description'],
                re.IGNORECASE
            )
            if dimension_match:
                capacity_data['dimension'] = dimension_match.group(1).strip()
                # Remove the "Dimensão: X" prefix from description
                capacity_data['description'] = re.sub(
                    r'Dimens[ãa]o:.*?(?:Resumo Descritivo\s*)?',
                    '',
                    capacity_data['description'],
                    count=1,
                    flags=re.IGNORECASE
                ).strip()

        # Determine capacity name (priority: explicit field > dimension > filename)
        if capacity_data['capacity_name']:
            capacity_name = capacity_data['capacity_name']
        elif capacity_data['dimension']:
            capacity_name = capacity_data['dimension']
        else:
            # Last resort: use filename but clean it up
            capacity_name = self.docx_path.stem
            # Remove date prefixes like "20251105_checklist_"
            capacity_name = re.sub(r'^\d{8}_checklist_', '', capacity_name)
            capacity_name = capacity_name.replace('_', ' ').title()

        # Generate capacity ID (after all metadata extracted)
        block_code = self._get_block_code(capacity_data['block'])
        pilar_code = self._get_pilar_code(capacity_data['pilar'])
        dim_code = self._get_dimension_code(capacity_data['dimension'])
        capacity_id = f"CAP-{block_code}-{pilar_code}-{dim_code}-001"

        metadata = Metadata(
            source_frameworks=["ACATECH", "SIRI"],
            author=self.author,
            version="1.0",
            last_updated=datetime.now().strftime("%Y-%m-%d"),
            source_docx=self.docx_path.name,
            status="draft"
        )

        return Capacity(
            id=capacity_id,
            name=capacity_name,
            block=capacity_data['block'],
            pilar=capacity_data['pilar'],
            dimension=capacity_data['dimension'],
            description=capacity_data['description'],
            related_capacities=capacity_data['related_capacities'],
            metadata=metadata
        )

    def _get_block_code(self, block: str) -> str:
        """Get short code for block."""
        mapping = {
            'Organização': 'ORG',
            'Organizacao': 'ORG',
            'Processo': 'PROC',
            'Tecnologia': 'TEC'
        }
        return mapping.get(block, 'UNK')

    def _get_pilar_code(self, pilar: str) -> str:
        """Get short code for pilar."""
        # Extract initials from pilar name
        words = pilar.split()
        if len(words) >= 2:
            return ''.join([w[0].upper() for w in words[:2]])
        return pilar[:2].upper() if pilar else 'UN'

    def _get_dimension_code(self, dimension: str) -> str:
        """Get short code for dimension."""
        # Extract initials from dimension name
        words = dimension.split()
        if len(words) >= 2:
            return ''.join([w[0].upper() for w in words[:2]])
        return dimension[:2].upper() if dimension else 'UN'

    def _extract_questions(self, capacity: Capacity) -> List[Question]:
        """Extract all questions from the document."""
        questions = []
        current_question = None
        current_section = None
        question_counter = 0

        # Process all paragraphs and tables
        for element in self.doc.element.body:
            if element.tag.endswith('p'):  # Paragraph
                para = Paragraph(element, self.doc)
                text = self._clean_text(para.text)

                if not text:
                    continue

                # Check if this is a new question
                question_match = self.question_pattern.search(text)
                if question_match:
                    # Save previous question
                    if current_question:
                        questions.append(current_question)

                    # Start new question
                    question_counter += 1
                    question_num = int(question_match.group(1))

                    # Extract title (usually after the question number)
                    title = re.sub(r'^[Qq]uest[ãa]o\s+\d+\s*[-–—]\s*', '', text)

                    question_id = f"Q-{capacity.id.split('-', 1)[1]}-{question_num:03d}"

                    current_question = {
                        'id': question_id,
                        'question_number': question_num,
                        'title': title,
                        'text': '',
                        'maturity_levels': [],
                        'evidence_sources': {
                            'artifacts': [],
                            'metrics': [],
                            'signals_by_level': {},
                            'sampling_guidance': ''
                        }
                    }
                    current_section = 'title'

            elif element.tag.endswith('tbl'):  # Table
                table = Table(element, self.doc)

                if current_question is not None:
                    # This table might contain question text, maturity levels, or evidence
                    table_data = self.extract_table_data(table)
                    self._process_question_table(table, current_question)

        # Don't forget the last question
        if current_question:
            questions.append(current_question)

        # Convert dicts to Question objects
        return self._convert_to_question_objects(questions, capacity)

    def _process_question_table(self, table: Table, question_dict: Dict):
        """Process a table that's part of a question."""
        for i, row in enumerate(table.rows):
            cells = row.cells

            if len(cells) < 1:
                continue

            cell_text = self._clean_text(cells[0].text)

            # Check if this row contains maturity level information
            if len(cells) >= 2:
                first_cell = self._clean_text(cells[0].text)
                second_cell = self._clean_text(cells[1].text)

                # Maturity levels often have a number in first cell and description in second
                level_match = self.maturity_level_pattern.match(first_cell)
                if level_match:
                    level_num = int(level_match.group(1))

                    # Extract label (often in bold at start of description)
                    label_match = re.match(r'^([^:]+):', second_cell)
                    if label_match:
                        label = label_match.group(1).strip()
                        description = second_cell[len(label)+1:].strip()
                    else:
                        label = f"Nível {level_num}"
                        description = second_cell

                    question_dict['maturity_levels'].append({
                        'level': level_num,
                        'label': label,
                        'description': description
                    })

                # Check for question text
                if 'Qual' in first_cell or 'Como' in first_cell or '?' in first_cell:
                    if not question_dict['text']:
                        question_dict['text'] = first_cell

                # Check for evidence sources
                if 'evidência' in cell_text.lower() or 'evidence' in cell_text.lower():
                    # Use the evidence extractor module if available
                    if self.evidence_extractor:
                        extracted_evidence = self.evidence_extractor.extract_from_table(table)
                        if extracted_evidence:
                            question_dict['evidence_sources'] = extracted_evidence
                    else:
                        # Fallback to old parsing method
                        content = second_cell if len(cells) >= 2 else cell_text
                        self._parse_evidence_sources(content, question_dict['evidence_sources'])
                elif 'Capacidade em medição' in cell_text or 'Capacidade em medicao' in cell_text:
                    if len(cells) >= 2:
                        question_dict['capacity_measured'] = self._clean_text(cells[1].text)

    def _parse_evidence_sources(self, text: str, evidence_dict: Dict):
        """Parse evidence sources from text."""
        # Look for sections marked with A), B), C), D)

        # Artifacts (usually marked with A))
        artifacts_match = re.search(r'A\)(.*?)(?:B\)|$)', text, re.DOTALL | re.IGNORECASE)
        if artifacts_match:
            artifacts_text = artifacts_match.group(1)
            # Split by ** markers or bullets
            artifacts = re.split(r'\*\*|\n[-•]', artifacts_text)
            evidence_dict['artifacts'].extend([a.strip() for a in artifacts if a.strip()])

        # Metrics (usually marked with B))
        metrics_match = re.search(r'B\)(.*?)(?:C\)|$)', text, re.DOTALL | re.IGNORECASE)
        if metrics_match:
            metrics_text = metrics_match.group(1)
            metrics = re.split(r'\*\*|\n[-•]', metrics_text)
            evidence_dict['metrics'].extend([m.strip() for m in metrics if m.strip()])

        # Signals by level (usually marked with C))
        signals_match = re.search(r'C\)(.*?)(?:D\)|$)', text, re.DOTALL | re.IGNORECASE)
        if signals_match:
            signals_text = signals_match.group(1)
            # Look for N0:, N1:, etc.
            level_matches = re.finditer(r'N(\d):(.*?)(?=N\d:|$)', signals_text, re.DOTALL)
            for match in level_matches:
                level = f"N{match.group(1)}"
                description = self._clean_text(match.group(2))
                evidence_dict['signals_by_level'][level] = description

        # Sampling guidance (usually marked with D))
        sampling_match = re.search(r'D\)(.*)', text, re.DOTALL | re.IGNORECASE)
        if sampling_match:
            evidence_dict['sampling_guidance'] = self._clean_text(sampling_match.group(1))

    def _convert_to_question_objects(self, questions_dicts: List[Dict], capacity: Capacity) -> List[Question]:
        """Convert question dictionaries to Question objects."""
        questions = []

        for q_dict in questions_dicts:
            # Convert maturity levels
            maturity_levels = [
                MaturityLevel(**ml) for ml in q_dict.get('maturity_levels', [])
            ]

            # Sort by level
            maturity_levels.sort(key=lambda x: x.level)

            # Convert evidence sources
            evidence_sources = None
            if q_dict.get('evidence_sources'):
                ev = q_dict['evidence_sources']
                if ev['artifacts'] or ev['metrics'] or ev['signals_by_level']:
                    evidence_sources = EvidenceSources(
                        artifacts=ev['artifacts'],
                        metrics=ev['metrics'],
                        signals_by_level=ev['signals_by_level'],
                        sampling_guidance=ev['sampling_guidance']
                    )

            question = Question(
                id=q_dict['id'],
                question_number=q_dict['question_number'],
                title=q_dict['title'],
                text=q_dict['text'],
                maturity_levels=maturity_levels,
                evidence_sources=evidence_sources
            )

            questions.append(question)

        return questions

    def convert(self) -> Dict:
        """Main conversion method."""
        print(f"Converting {self.docx_path.name}...")

        # Extract capacity information
        capacity = self._extract_capacity_info()
        if not capacity:
            raise ValueError("Could not extract capacity information from document")

        print(f"  Capacity: {capacity.name}")
        print(f"  Block: {capacity.block}, Pilar: {capacity.pilar}, Dimension: {capacity.dimension}")

        # Extract questions
        questions = self._extract_questions(capacity)
        print(f"  Found {len(questions)} questions")

        # Extract glossary
        glossary = []
        if self.glossary_extractor:
            glossary = self.glossary_extractor.extract_from_document(self.doc)
            print(f"  Extracted {len(glossary)} glossary terms")

        # Extract references
        references = []
        if self.references_extractor:
            references = self.references_extractor.extract_from_document(self.doc)
            print(f"  Extracted {len(references)} references")

        # Build final structure
        result = {
            'capacity': self._dataclass_to_dict(capacity),
            'questions': [self._dataclass_to_dict(q) for q in questions]
        }

        # Add glossary and references if found
        if glossary:
            result['glossary'] = glossary
        if references:
            result['references'] = references

        return result

    def _dataclass_to_dict(self, obj) -> Dict:
        """Convert dataclass to dict, handling nested structures and filtering None values."""
        if obj is None:
            return None

        if hasattr(obj, '__dataclass_fields__'):
            # Use asdict to convert, then recursively filter None values
            data = asdict(obj)
            return self._filter_none_values(data)

        return obj

    def _filter_none_values(self, data):
        """Recursively filter out None values from dictionaries."""
        if isinstance(data, dict):
            return {k: self._filter_none_values(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self._filter_none_values(item) for item in data]
        else:
            return data

    def save_json(self, output_path: str, indent: int = 2):
        """Convert and save to JSON file."""
        data = self.convert()

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

        print(f"✅ Saved to {output_path}")
        return data


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert Industry 4.0 DOCX files to structured JSON'
    )
    parser.add_argument('docx_file', help='Path to DOCX file')
    parser.add_argument('-o', '--output', help='Output JSON file path')
    parser.add_argument('-a', '--author', default='Unknown', help='Author name')
    parser.add_argument('--indent', type=int, default=2, help='JSON indentation (default: 2)')

    args = parser.parse_args()

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        docx_path = Path(args.docx_file)
        output_path = docx_path.with_suffix('.json')

    # Convert
    converter = DOCXToJSONConverter(args.docx_file, author=args.author)
    converter.save_json(output_path, indent=args.indent)


if __name__ == '__main__':
    main()
