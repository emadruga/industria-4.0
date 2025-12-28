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
    evidence_signals: Optional[Dict[str, List[str]]] = None


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

    def __init__(self, docx_path: str, author: str = "Unknown", capacity_number: int = 1):
        self.docx_path = Path(docx_path)
        self.author = author
        self.capacity_number = capacity_number
        self.doc = Document(str(self.docx_path))

        # Patterns for parsing
        # Match both "Questão 1" and "Questão XX" (placeholder pattern)
        self.question_pattern = re.compile(r'^[Qq]uest[ãa]o\s+(\d+|XX|xx)', re.IGNORECASE)
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

        # Normalize names before creating Capacity
        normalized_block = self._normalize_block_name(capacity_data['block'])
        normalized_pilar = self._normalize_pilar_name(capacity_data['pilar'])
        normalized_dimension = self._normalize_dimension_name(capacity_data['dimension'])

        # Generate capacity ID (after normalization) with sequential numbering
        block_code = self._get_block_code(capacity_data['block'])
        pilar_code = self._get_pilar_code(capacity_data['pilar'])
        dim_code = self._get_dimension_code(capacity_data['dimension'])
        capacity_id = f"CAP-{block_code}-{pilar_code}-{dim_code}-{self.capacity_number:03d}"

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
            block=normalized_block,
            pilar=normalized_pilar,
            dimension=normalized_dimension,
            description=capacity_data['description'],
            related_capacities=capacity_data['related_capacities'],
            metadata=metadata
        )

    def _normalize_block_name(self, block: str) -> str:
        """Normalize block name to standard Portuguese form."""
        block_clean = block.strip()
        # Mapping from various forms (English/Portuguese with accents) to canonical Portuguese
        normalization = {
            # Technology variations
            'Technology': 'Tecnologia',
            'Tecnologia': 'Tecnologia',

            # Organization variations
            'Organization': 'Organização',
            'Organização': 'Organização',
            'Organizacao': 'Organização',
            'Organization (Organização)': 'Organização',

            # Process variations
            'Process': 'Processo',
            'Processo': 'Processo',

            # Talent Readiness variations
            'Prontidão/Preparação de Talentos': 'Organização',
            'Talent Readiness': 'Organização',
        }
        return normalization.get(block_clean, block_clean)

    def _get_block_code(self, block: str) -> str:
        """Get short code for block."""
        normalized = self._normalize_block_name(block)
        mapping = {
            'Tecnologia': 'TEC',
            'Organização': 'ORG',
            'Processo': 'PROC'
        }
        return mapping.get(normalized, 'UNK')

    def _normalize_pilar_name(self, pilar: str) -> str:
        """Normalize pilar name to standard Portuguese form."""
        pilar_clean = pilar.strip()
        normalization = {
            # Intelligence variations
            'Intelligence': 'Inteligência',
            'Inteligência': 'Inteligência',
            'Inteligencia': 'Inteligência',

            # Automation variations
            'Automation': 'Automação',
            'Automação': 'Automação',
            'Automacao': 'Automação',

            # Connectivity variations
            'Connectivity': 'Conectividade',
            'Conectividade': 'Conectividade',

            # Structure & Management variations
            'Structure & Management': 'Estrutura e Gestão',
            'Structure & Management (Estrutura e Gestão)': 'Estrutura e Gestão',
            'Estrutura & Gestão': 'Estrutura e Gestão',
            'Estrutura e Gestão': 'Estrutura e Gestão',
            'Estrutura e Gestao': 'Estrutura e Gestão',

            # Talent Readiness variations
            'Talent Readiness': 'Prontidão de Talentos',
            'Talent readiness': 'Prontidão de Talentos',
            'Prontidão de Talentos': 'Prontidão de Talentos',
            'Prontidao de Talentos': 'Prontidão de Talentos',

            # Operations/Supply Chain variations
            'Operations/Supply Chain': 'Operações/Cadeia de Suprimentos',
            'Operações/Cadeia de Suprimentos': 'Operações/Cadeia de Suprimentos',

            # Organization (as pilar in some docs - map to Structure & Management)
            'Organização': 'Estrutura e Gestão',
            'Organizacao': 'Estrutura e Gestão',
        }
        return normalization.get(pilar_clean, pilar_clean)

    def _get_pilar_code(self, pilar: str) -> str:
        """Generate smart code for pilar (5-6 letters, skip articles like 'e')."""
        normalized = self._normalize_pilar_name(pilar)

        # Articles and connectors to skip
        skip_words = {'e', 'de', 'da', 'do', 'das', 'dos', '&', '-', '/'}

        # Split into words and filter
        words = normalized.split()
        meaningful_words = [w for w in words if w.lower() not in skip_words and w.strip()]

        # Extract 5-6 letters from meaningful words
        code_chars = []
        for word in meaningful_words:
            # Get only alphabetic characters
            clean_word = ''.join([c for c in word if c.isalpha()])
            if clean_word:
                code_chars.extend(list(clean_word.upper()))

        # Take 6 letters if available, otherwise 5
        if len(code_chars) >= 6:
            return ''.join(code_chars[:6])
        elif len(code_chars) >= 5:
            return ''.join(code_chars[:5])
        elif len(code_chars) >= 3:
            return ''.join(code_chars[:len(code_chars)])

        # Fallback: use all alphabetic characters
        alpha_chars = [c.upper() for c in normalized if c.isalpha()]
        if len(alpha_chars) >= 3:
            return ''.join(alpha_chars[:min(6, len(alpha_chars))])

        return 'PILAR'  # Default if nothing works

    def _normalize_dimension_name(self, dimension: str) -> str:
        """Normalize dimension name to standard Portuguese form."""
        dimension_clean = dimension.strip()
        normalization = {
            # Shopfloor variations
            'Shopfloor (D10)': 'Chão de Fábrica (D10)',
            'Shop Floor (D10)': 'Chão de Fábrica (D10)',
            'Shopfloor': 'Chão de Fábrica',
            'Shop Floor': 'Chão de Fábrica',

            # Enterprise variations
            'Enterprise (D11)': 'Corporativo (D11)',
            'Enterprise (D8)': 'Corporativo (D8)',
            'Enterprise': 'Corporativo',

            # Facility variations
            'Facility (D9)': 'Instalação (D9)',
            'Facility (Instalação) (D9)': 'Instalação (D9)',
            'Facility': 'Instalação',

            # Shop Floor D4 and D7 variations
            'Shop Floor (Chão de Fábrica) (D4)': 'Chão de Fábrica (D4)',
            'Shop Floor (Chão de Fábrica) (D7)': 'Chão de Fábrica (D7)',
            'Shop Floor (D4)': 'Chão de Fábrica (D4)',
            'Shop Floor (D7)': 'Chão de Fábrica (D7)',

            # Integrated Product Life Cycle variations
            'Ciclo de Vida de Produto Integrado (D3)': 'Ciclo de Vida de Produto Integrado (D3)',

            # Leadership Competency variations
            'Leadership Competency (D14)': 'Competência de Liderança (D14)',
            'Leadership Competency (Competência de Liderança)': 'Competência de Liderança',
            'Leadership Competency': 'Competência de Liderança',
            'Competência de Liderança': 'Competência de Liderança',
            'Competencia de Liderança': 'Competência de Liderança',
            'Competencia de Lideranca': 'Competência de Liderança',

            # Workforce Learning & Development variations
            'Workforce Learning & Development (D13)': 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)',
            'Workforce Learning & Development': 'Aprendizado e Desenvolvimento da Força de Trabalho',

            # Strategy & Governance variations
            'Strategy & Governance (D16)': 'Estratégia e Governança (D16)',
            'Strategy & Governance': 'Estratégia e Governança',
            'Estratégia e Governança': 'Estratégia e Governança',

            # Inter and Intra-Company Collaboration variations
            'Inter- and Intra-Company Collaboration (D15)': 'Colaboração Inter e Intraempresarial (D15)',
            'Inter- and Intra-Company Collaboration': 'Colaboração Inter e Intraempresarial',
            'Colaboração Inter e Intraempresarial': 'Colaboração Inter e Intraempresarial',

            # Cooperation variations
            'Cooperação dentro da Rede': 'Cooperação dentro da Rede',

            # Vertical/Horizontal variations
            'Vertical (D1) - primário': 'Vertical (D1)',
            'Vertical (D1)': 'Vertical (D1)',
            'Horizontal (D2) - Mapeamento secundário': 'Horizontal (D2)',
            'Horizontal (D2)': 'Horizontal (D2)',
        }
        return normalization.get(dimension_clean, dimension_clean)

    def _get_dimension_code(self, dimension: str) -> str:
        """Generate smart code for dimension (5-6 letters, skip articles like 'e')."""
        normalized = self._normalize_dimension_name(dimension)

        # Remove dimension codes like (D10), (D11) from the string
        clean_dimension = re.sub(r'\s*\([Dd]\d+\)\s*', '', normalized).strip()

        # Articles and connectors to skip
        skip_words = {'e', 'de', 'da', 'do', 'das', 'dos', '&', '-', '/'}

        # Split into words and filter
        words = clean_dimension.split()
        meaningful_words = [w for w in words if w.lower() not in skip_words and w.strip()]

        # Extract 5-6 letters from meaningful words
        code_chars = []
        for word in meaningful_words:
            # Get only alphabetic characters
            clean_word = ''.join([c for c in word if c.isalpha()])
            if clean_word:
                code_chars.extend(list(clean_word.upper()))

        # Take 6 letters if available, otherwise 5
        if len(code_chars) >= 6:
            return ''.join(code_chars[:6])
        elif len(code_chars) >= 5:
            return ''.join(code_chars[:5])
        elif len(code_chars) >= 3:
            return ''.join(code_chars[:len(code_chars)])

        # Fallback: use all alphabetic characters
        alpha_chars = [c.upper() for c in clean_dimension if c.isalpha()]
        if len(alpha_chars) >= 3:
            return ''.join(alpha_chars[:min(6, len(alpha_chars))])

        return 'DIMENS'  # Default if nothing works

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

                    # Handle both numeric and placeholder patterns (XX)
                    matched_num = question_match.group(1)
                    if matched_num.upper() == 'XX':
                        # Use auto-incremented counter when XX is used
                        question_num = question_counter
                    else:
                        question_num = int(matched_num)

                    # Extract title (match both patterns: "Questão 1" and "Questão XX")
                    title = re.sub(r'^[Qq]uest[ãa]o\s+(\d+|XX|xx)\s*[-–—]\s*', '', text, flags=re.IGNORECASE)

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

            # Check for evidence sources (MUST be outside len(cells) >= 2 check!)
            # Evidence tables often have single-cell rows with headers like "Possíveis fontes de evidências:"
            if 'evidência' in cell_text.lower() or 'evidence' in cell_text.lower():
                # Use the evidence extractor module if available
                if self.evidence_extractor:
                    extracted_evidence = self.evidence_extractor.extract_from_table(table)
                    if extracted_evidence:
                        question_dict['evidence_sources'] = extracted_evidence
                else:
                    # Fallback to old parsing method
                    content = cells[1].text if len(cells) >= 2 else cell_text
                    self._parse_evidence_sources(content, question_dict['evidence_sources'])

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

                # Check for capacity measurement
                if 'Capacidade em medição' in cell_text or 'Capacidade em medicao' in cell_text:
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

    def _map_evidence_to_maturity_levels(self, maturity_levels_list: List[Dict], evidence_data: Dict) -> List[Dict]:
        """
        Map evidence signals to corresponding maturity levels.

        Uses hybrid approach:
        - Sections A & B (artifacts, metrics): Applied to ALL maturity levels
        - Section C (signals_by_level): Level-specific observable behaviors
        - Section D (sampling_guidance): Stored at evidence_sources level

        Args:
            maturity_levels_list: List of maturity level dicts
            evidence_data: Evidence dict with artifacts, metrics, signals_by_level

        Returns:
            Updated maturity levels list with evidence_signals added
        """
        if not evidence_data:
            # No evidence data, add empty structure to all levels
            for ml in maturity_levels_list:
                ml['evidence_signals'] = {
                    "artifacts": [],
                    "metrics": [],
                    "observable_behaviors": [],
                    "interview_questions": []
                }
            return maturity_levels_list

        # Extract general artifacts and metrics from Sections A & B
        general_artifacts = evidence_data.get('artifacts', [])
        general_metrics = evidence_data.get('metrics', [])
        signals_by_level = evidence_data.get('signals_by_level', {})

        # Map evidence to each maturity level
        for ml in maturity_levels_list:
            level_key = f"N{ml['level']}"

            # Start with general artifacts/metrics that apply to all levels
            level_artifacts = list(general_artifacts)  # Copy general list
            level_metrics = list(general_metrics)  # Copy general list
            level_behaviors = []
            level_questions = []

            # Add level-specific evidence from Section C if available
            if level_key in signals_by_level and isinstance(signals_by_level[level_key], dict):
                level_evidence = signals_by_level[level_key]

                # Add level-specific artifacts/metrics if present (override general if specified)
                if level_evidence.get('artifacts'):
                    level_artifacts.extend(level_evidence['artifacts'])

                if level_evidence.get('metrics'):
                    level_metrics.extend(level_evidence['metrics'])

                # Level-specific observable behaviors (from prose format)
                level_behaviors = level_evidence.get('observable_behaviors', [])

                # Level-specific interview questions
                level_questions = level_evidence.get('interview_questions', [])

            ml['evidence_signals'] = {
                "artifacts": level_artifacts,
                "metrics": level_metrics,
                "observable_behaviors": level_behaviors,
                "interview_questions": level_questions
            }

        return maturity_levels_list

    def _convert_to_question_objects(self, questions_dicts: List[Dict], capacity: Capacity) -> List[Question]:
        """Convert question dictionaries to Question objects."""
        questions = []

        for q_dict in questions_dicts:
            # Map evidence to maturity levels before converting to objects
            maturity_levels_dicts = q_dict.get('maturity_levels', [])
            evidence_data = q_dict.get('evidence_sources', {})

            # Apply evidence mapping
            maturity_levels_dicts = self._map_evidence_to_maturity_levels(
                maturity_levels_dicts,
                evidence_data
            )

            # Convert maturity levels to dataclass objects
            maturity_levels = [
                MaturityLevel(**ml) for ml in maturity_levels_dicts
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
