#!/usr/bin/env python3
"""
Check Evidence Format in DOCX Files
Examines 4 sample DOCX files from different authors to verify evidence format consistency.
"""

import sys
from pathlib import Path
from docx import Document

# Sample files from 4 authors
SAMPLE_FILES = [
    "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/EwertonMadruga/Estrutura e Gestão - Ewerton/20251106_checklist_abertura_inovacao.docx",
    "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/CristianoGurgelCastro/0890_Dimensão Shopfloor_cgcastro.docx",
    "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/FlaviaAgostini/Prontidão-Preparação de Talentos/Competência de Liderança.docx",
    "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author/WilsonMeloJr/Processo/Ciclo de Vida de Produto/Ciclo de Vida de Produto Integrado (D3).docx"
]

def check_file(file_path):
    """Check evidence format in a DOCX file."""
    print(f"\n{'='*80}")
    print(f"File: {Path(file_path).name}")
    print(f"Author: {Path(file_path).parts[-3]}")
    print(f"{'='*80}")

    try:
        doc = Document(file_path)

        # Look for evidence sections in tables
        evidence_found = False
        evidence_patterns = []

        for table_idx, table in enumerate(doc.tables):
            for row_idx, row in enumerate(table.rows):
                for cell in row.cells:
                    text = cell.text.lower()

                    # Check for evidence markers
                    if any(marker in text for marker in ['evidência', 'evidencia', 'evidence', 'sinais por nível']):
                        evidence_found = True
                        print(f"\n✓ Evidence section found in Table {table_idx}, Row {row_idx}")

                        # Extract a sample of the content
                        sample = cell.text[:500]
                        print(f"\nSample content:")
                        print("-" * 80)
                        print(sample)
                        print("-" * 80)

                        # Check for level patterns (N0, N1, etc.)
                        if 'n0:' in text or 'n1:' in text or 'n2:' in text:
                            print("✓ Found maturity level markers (N0:, N1:, N2:, etc.)")
                            evidence_patterns.append("maturity_levels")

                        # Check for category patterns
                        if 'artefatos' in text or 'artifacts' in text:
                            print("✓ Found 'Artefatos' category")
                            evidence_patterns.append("artifacts")

                        if 'métricas' in text or 'kpis' in text or 'metrics' in text:
                            print("✓ Found 'Métricas/KPIs' category")
                            evidence_patterns.append("metrics")

                        if 'comportamentos' in text or 'behaviors' in text or 'sinais' in text:
                            print("✓ Found 'Comportamentos/Sinais' category")
                            evidence_patterns.append("behaviors")

                        if 'perguntas' in text or 'questions' in text or 'interview' in text:
                            print("✓ Found 'Perguntas/Questions' category")
                            evidence_patterns.append("questions")

                        # Only show first evidence section
                        break
                if evidence_found:
                    break
            if evidence_found:
                break

        if not evidence_found:
            print("\n⚠ No evidence section found in this file")
        else:
            print(f"\n✓ Evidence patterns detected: {', '.join(set(evidence_patterns))}")

        return evidence_found, evidence_patterns

    except Exception as e:
        print(f"\n✗ Error reading file: {e}")
        return False, []

def main():
    """Main function."""
    print("\n" + "="*80)
    print("EVIDENCE FORMAT CHECK - 4 Authors")
    print("="*80)

    results = []

    for file_path in SAMPLE_FILES:
        if not Path(file_path).exists():
            print(f"\n⚠ File not found: {file_path}")
            continue

        found, patterns = check_file(file_path)
        results.append({
            'file': Path(file_path).name,
            'author': Path(file_path).parts[-3],
            'found': found,
            'patterns': patterns
        })

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    for result in results:
        status = "✓" if result['found'] else "✗"
        print(f"{status} {result['author']:25} | {result['file']}")
        if result['patterns']:
            print(f"  Patterns: {', '.join(set(result['patterns']))}")

    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    all_have_evidence = all(r['found'] for r in results)

    if all_have_evidence:
        print("✓ All authors include evidence sections")
        print("✓ Enhanced extraction script should work")
    else:
        print("⚠ Not all authors include evidence sections")
        print("⚠ Some manual evidence entry may be required")

    # Check consistency
    all_patterns = [p for r in results for p in r['patterns']]
    if 'maturity_levels' in all_patterns:
        print("✓ Maturity level markers (N0:, N1:, etc.) are used")
    else:
        print("⚠ Maturity level markers may be inconsistent")

if __name__ == '__main__':
    main()
