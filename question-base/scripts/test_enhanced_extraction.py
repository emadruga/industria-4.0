#!/usr/bin/env python3
"""
Test Enhanced Evidence Extraction - Phase 2, Task 4
Tests the enhanced extraction script on all 4 authors' DOCX files to validate:
1. Section C prose format parsing works correctly
2. Artifacts and metrics from Sections A & B are mapped to all levels
3. Observable behaviors from Section C are level-specific
"""

import sys
import json
from pathlib import Path
from docx import Document
from extract_evidence import EvidenceExtractor

# Sample files from 4 authors (same as test_evidence_extraction.py)
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


def test_extraction_on_file(file_path, author, capacity):
    """Test extraction on a single DOCX file."""
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
        extractor = EvidenceExtractor()

        # Find evidence tables
        evidence_results = []

        for table_idx, table in enumerate(doc.tables):
            evidence = extractor.extract_from_table(table)

            if evidence:
                evidence_results.append({
                    'table_idx': table_idx,
                    'evidence': evidence
                })

        if not evidence_results:
            print("⚠ No evidence found in any tables")
            return {
                'author': author,
                'capacity': capacity,
                'evidence_found': False,
                'evidence_count': 0
            }

        print(f"\n✓ Found {len(evidence_results)} evidence section(s)")

        # Analyze first evidence section in detail
        first_evidence = evidence_results[0]['evidence']

        print(f"\n📊 EXTRACTION RESULTS (Table {evidence_results[0]['table_idx']}):")
        print(f"\n  A) General Artifacts (Section A - apply to all levels):")
        print(f"     Count: {len(first_evidence['artifacts'])}")
        if first_evidence['artifacts']:
            for i, artifact in enumerate(first_evidence['artifacts'][:3], 1):
                print(f"     {i}. {artifact[:80]}...")

        print(f"\n  B) General Metrics (Section B - apply to all levels):")
        print(f"     Count: {len(first_evidence['metrics'])}")
        if first_evidence['metrics']:
            for i, metric in enumerate(first_evidence['metrics'][:3], 1):
                print(f"     {i}. {metric[:80]}...")

        print(f"\n  C) Signals by Level (Section C - level-specific):")
        signals_by_level = first_evidence['signals_by_level']
        print(f"     Levels found: {sorted(signals_by_level.keys())}")

        # Show first level in detail
        if signals_by_level:
            first_level = sorted(signals_by_level.keys())[0]
            level_data = signals_by_level[first_level]

            print(f"\n     Example: {first_level}")
            print(f"       - Observable behaviors: {len(level_data.get('observable_behaviors', []))}")
            if level_data.get('observable_behaviors'):
                for i, behavior in enumerate(level_data['observable_behaviors'][:3], 1):
                    print(f"         {i}. {behavior[:70]}...")

            print(f"       - Artifacts (level-specific): {len(level_data.get('artifacts', []))}")
            print(f"       - Metrics (level-specific): {len(level_data.get('metrics', []))}")
            print(f"       - Interview questions: {len(level_data.get('interview_questions', []))}")

        print(f"\n  D) Sampling Guidance (Section D):")
        sampling = first_evidence.get('sampling_guidance', '')
        if sampling:
            print(f"     {sampling[:150]}...")
        else:
            print(f"     (none)")

        # Validation checks
        print(f"\n✅ VALIDATION:")

        checks = {
            "Section A artifacts extracted": len(first_evidence['artifacts']) > 0,
            "Section B metrics extracted": len(first_evidence['metrics']) > 0,
            "Section C levels detected": len(signals_by_level) > 0,
            "Prose behaviors parsed": any(
                len(level_data.get('observable_behaviors', [])) > 0
                for level_data in signals_by_level.values()
            )
        }

        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"     {status} {check}")

        return {
            'author': author,
            'capacity': capacity,
            'evidence_found': True,
            'evidence_count': len(evidence_results),
            'general_artifacts_count': len(first_evidence['artifacts']),
            'general_metrics_count': len(first_evidence['metrics']),
            'levels_found': sorted(signals_by_level.keys()),
            'levels_count': len(signals_by_level),
            'validation_checks': checks,
            'all_checks_passed': all(checks.values())
        }

    except Exception as e:
        print(f"\n✗ Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function."""
    print("\n" + "="*80)
    print("PHASE 2, TASK 4: ENHANCED EVIDENCE EXTRACTION TEST")
    print("="*80)
    print("\nTesting enhanced extraction with:")
    print("  1. Section C prose format parsing (semicolon-separated)")
    print("  2. Hybrid approach (Sections A & B general, Section C level-specific)")
    print("="*80)

    results = []

    for test_file in TEST_FILES:
        result = test_extraction_on_file(
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

    print(f"\nTotal files tested: {len(results)}")
    print(f"Files with evidence: {sum(1 for r in results if r['evidence_found'])}")

    # Aggregate statistics
    if results:
        total_artifacts = sum(r.get('general_artifacts_count', 0) for r in results)
        total_metrics = sum(r.get('general_metrics_count', 0) for r in results)
        total_levels = sum(r.get('levels_count', 0) for r in results)

        print(f"\n📊 Extraction Statistics:")
        print(f"  Total general artifacts extracted: {total_artifacts}")
        print(f"  Total general metrics extracted: {total_metrics}")
        print(f"  Total maturity levels with evidence: {total_levels}")
        print(f"  Average levels per file: {total_levels / len(results):.1f}")

    # Validation summary
    print(f"\n✅ Validation Results:")
    all_passed = sum(1 for r in results if r.get('all_checks_passed', False))
    print(f"  Files passing all checks: {all_passed}/{len(results)}")

    if all_passed == len(results):
        print(f"\n  🎉 ALL FILES PASSED ALL VALIDATION CHECKS!")
    else:
        print(f"\n  ⚠️ Some files failed validation checks")
        for r in results:
            if not r.get('all_checks_passed', False):
                print(f"    - {r['author']}: {r['capacity']}")

    # Recommendations
    print(f"\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)

    if all_passed == len(results):
        print("\n✅ Enhanced extraction working correctly!")
        print("\nNext steps:")
        print("  1. ✅ Prose format parsing implemented successfully")
        print("  2. ✅ Hybrid approach (general + level-specific) working")
        print("  3. 📝 Ready to proceed with batch conversion (Phase 3)")
        print("\n  Suggested action: Update INTEGRATE_EVIDENCE_PLAN.md to mark Phase 2, Task 4 complete")
    else:
        print("\n⚠️ Some improvements needed:")
        print("  1. Review extraction logic for failed files")
        print("  2. Check if additional parsing patterns are needed")
        print("  3. Validate DOCX format consistency")

    # Save results to JSON
    output_file = Path(__file__).parent.parent / 'JSON6' / 'enhanced_extraction_test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Detailed results saved to: {output_file}")

    return 0 if all_passed == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
