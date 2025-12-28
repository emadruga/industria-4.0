#!/usr/bin/env python3
"""
Test Evidence Extraction Across Multiple Authors
Tests extraction on sample DOCX files from 4 different authors to identify format patterns.
"""

import sys
from pathlib import Path
from docx import Document
import re
import json

# Sample files from 4 authors
TEST_FILES = [
    {
        "author": "Ewerton Madruga",
        "file": "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/EwertonMadruga/Estrutura e Gestão - Ewerton/20251105_checklist_gestao_agil.docx",
        "capacity": "Gestão ágil"
    },
    {
        "author": "Cristiano Gurgel Castro",
        "file": "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/CristianoGurgelCastro/0890_Dimensão Shopfloor_cgcastro.docx",
        "capacity": "Shopfloor"
    },
    {
        "author": "Flavia Agostini",
        "file": "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/FlaviaAgostini/Prontidão-Preparação de Talentos/Competência de Liderança.docx",
        "capacity": "Competência de Liderança"
    },
    {
        "author": "Wilson Melo Jr",
        "file": "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/WilsonMeloJr/Processo/Ciclo de Vida de Produto/Ciclo de Vida de Produto Integrado (D3).docx",
        "capacity": "Ciclo de Vida de Produto"
    }
]

def analyze_evidence_format(file_path, author, capacity):
    """Analyze evidence format in a DOCX file."""
    print(f"\n{'='*80}")
    print(f"AUTHOR: {author}")
    print(f"CAPACITY: {capacity}")
    print(f"FILE: {Path(file_path).name}")
    print(f"{'='*80}")

    if not Path(file_path).exists():
        print(f"⚠ File not found: {file_path}")
        return None

    try:
        doc = Document(file_path)

        # Find evidence sections
        evidence_tables = []

        for table_idx, table in enumerate(doc.tables):
            # Concatenate all rows of the table
            table_text = ""
            for row in table.rows:
                for cell in row.cells:
                    table_text += cell.text + "\n"

            # Check if this table contains evidence
            if any(marker in table_text.lower() for marker in ['possíveis fontes de evidências', 'fontes de evidência']):
                evidence_tables.append({
                    'table_idx': table_idx,
                    'content': table_text  # Full table content
                })

        if not evidence_tables:
            print("⚠ No evidence sections found")
            return {
                'author': author,
                'capacity': capacity,
                'evidence_found': False,
                'format_analysis': None
            }

        # Analyze format of first evidence section
        evidence_text = evidence_tables[0]['content']

        print(f"\n✓ Found {len(evidence_tables)} evidence section(s)")
        print(f"\nFIRST EVIDENCE SECTION (Table {evidence_tables[0]['table_idx']}):")
        print("-" * 80)
        print(evidence_text[:800])
        print("-" * 80)

        # Pattern detection
        patterns = {
            'has_section_headers': {
                'A)': bool(re.search(r'A\)', evidence_text, re.IGNORECASE)),
                'B)': bool(re.search(r'B\)', evidence_text, re.IGNORECASE)),
                'C)': bool(re.search(r'C\)', evidence_text, re.IGNORECASE)),
                'D)': bool(re.search(r'D\)', evidence_text, re.IGNORECASE))
            },
            'has_category_names': {
                'Artefatos': bool(re.search(r'artefatos', evidence_text, re.IGNORECASE)),
                'Métricas': bool(re.search(r'métricas|kpis', evidence_text, re.IGNORECASE)),
                'Sinais': bool(re.search(r'sinais|comportamentos', evidence_text, re.IGNORECASE)),
                'Amostragem': bool(re.search(r'amostragem|sampling', evidence_text, re.IGNORECASE))
            },
            'has_level_markers': {
                'N0': bool(re.search(r'\bN0:', evidence_text, re.IGNORECASE)),
                'N1': bool(re.search(r'\bN1:', evidence_text, re.IGNORECASE)),
                'N2': bool(re.search(r'\bN2:', evidence_text, re.IGNORECASE)),
                'N3': bool(re.search(r'\bN3:', evidence_text, re.IGNORECASE)),
                'N4': bool(re.search(r'\bN4:', evidence_text, re.IGNORECASE)),
                'N5': bool(re.search(r'\bN5:', evidence_text, re.IGNORECASE))
            },
            'structure_type': None
        }

        # Determine structure type
        if any(patterns['has_section_headers'].values()):
            if patterns['has_section_headers']['C)'] and any(patterns['has_level_markers'].values()):
                patterns['structure_type'] = "SECTION_WITH_LEVELS (A/B/C/D format with N0:N1: in section C)"
            else:
                patterns['structure_type'] = "SECTION_HEADERS (A/B/C/D format)"
        elif any(patterns['has_level_markers'].values()):
            patterns['structure_type'] = "LEVEL_MARKERS_ONLY (N0:N1:N2: format)"
        else:
            patterns['structure_type'] = "PROSE_FORMAT (no clear structure)"

        print(f"\n📊 FORMAT ANALYSIS:")
        print(f"  Structure Type: {patterns['structure_type']}")
        print(f"\n  Section Headers (A/B/C/D):")
        for key, val in patterns['has_section_headers'].items():
            print(f"    {key}: {'✓' if val else '✗'}")
        print(f"\n  Category Names:")
        for key, val in patterns['has_category_names'].items():
            print(f"    {key}: {'✓' if val else '✗'}")
        print(f"\n  Level Markers (N0-N5):")
        for key, val in patterns['has_level_markers'].items():
            print(f"    {key}: {'✓' if val else '✗'}")

        return {
            'author': author,
            'capacity': capacity,
            'evidence_found': True,
            'format_analysis': patterns,
            'evidence_count': len(evidence_tables),
            'sample_text': evidence_text[:500]
        }

    except Exception as e:
        print(f"\n✗ Error analyzing file: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function."""
    print("\n" + "="*80)
    print("EVIDENCE EXTRACTION FORMAT TEST - 4 Authors")
    print("="*80)

    results = []

    for test_file in TEST_FILES:
        result = analyze_evidence_format(
            test_file['file'],
            test_file['author'],
            test_file['capacity']
        )
        if result:
            results.append(result)

    # Summary report
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)

    print(f"\nTotal files analyzed: {len(results)}")
    print(f"Files with evidence: {sum(1 for r in results if r['evidence_found'])}")

    # Structure type distribution
    print(f"\n📊 Structure Type Distribution:")
    structure_types = {}
    for r in results:
        if r['evidence_found']:
            stype = r['format_analysis']['structure_type']
            structure_types[stype] = structure_types.get(stype, 0) + 1

    for stype, count in structure_types.items():
        print(f"  {stype}: {count} file(s)")

    # Recommendations
    print(f"\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    if 'SECTION_WITH_LEVELS (A/B/C/D format with N0:N1: in section C)' in structure_types:
        print("\n✓ Good news! Most authors use A/B/C/D sections with level markers")
        print("  → The current extraction script should work with enhancements")
        print("  → Focus on improving section C parsing for N0:N1:N2: markers")

    if 'PROSE_FORMAT (no clear structure)' in structure_types:
        print("\n⚠ Some authors use prose format without structure")
        print("  → These will require manual evidence entry or LLM-assisted extraction")

    # Save results to JSON
    output_file = Path(__file__).parent.parent / 'JSON6' / 'evidence_extraction_test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Results saved to: {output_file}")

    return 0 if all(r['evidence_found'] for r in results) else 1

if __name__ == '__main__':
    sys.exit(main())
