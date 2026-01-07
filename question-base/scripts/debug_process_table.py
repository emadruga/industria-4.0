#!/usr/bin/env python3
"""
Debug _process_question_table to see if evidence is being extracted.
"""

from pathlib import Path
from docx_to_json_converter import DOCXToJSONConverter

# Monkey-patch to add logging
original_process_question_table = DOCXToJSONConverter._process_question_table

evidence_found_count = 0

def debug_process_question_table(self, table, question_dict):
    global evidence_found_count

    # Call original method
    result = original_process_question_table(self, table, question_dict)

    # Check if evidence was added
    ev = question_dict.get('evidence_sources', {})
    if ev and (ev.get('artifacts') or ev.get('metrics') or ev.get('signals_by_level')):
        evidence_found_count += 1
        print(f"  📊 Evidence found in table for Question {question_dict.get('question_number', '?')}")
        print(f"     Artifacts: {len(ev.get('artifacts', []))}")
        print(f"     Metrics: {len(ev.get('metrics', []))}")
        print(f"     Signals: {list(ev.get('signals_by_level', {}).keys())}")

    return result

DOCXToJSONConverter._process_question_table = debug_process_question_table

# Test
test_file = Path('../docs_by_author/EwertonMadruga/Estrutura e Gestão - Ewerton/20251105_checklist_gestao_agil.docx')

print("="*80)
print("Testing with logging in _process_question_table")
print("="*80)

converter = DOCXToJSONConverter(str(test_file), author="Ewerton")
result = converter.convert()

print(f"\n✅ Total tables where evidence was found: {evidence_found_count}")
print(f"✅ Total questions in result: {len(result.get('questions', []))}")

questions_with_evidence = sum(1 for q in result['questions'] if 'evidence_sources' in q and (q['evidence_sources'].get('artifacts') or q['evidence_sources'].get('metrics') or q['evidence_sources'].get('signals_by_level')))

print(f"❌ Questions with evidence in final JSON: {questions_with_evidence}")
EOF
