#!/usr/bin/env python3
"""
Debug script to check intermediate data in converter flow.
"""

import json
from pathlib import Path
from docx_to_json_converter import DOCXToJSONConverter

# Monkey-patch the converter to add logging
original_convert_to_question_objects = DOCXToJSONConverter._convert_to_question_objects

def debug_convert_to_question_objects(self, questions_dicts, capacity):
    print("\n" + "="*80)
    print("DEBUG: Inside _convert_to_question_objects")
    print("="*80)
    print(f"Number of questions_dicts: {len(questions_dicts)}\n")

    for i, q_dict in enumerate(questions_dicts, 1):
        print(f"Question {i}:")
        print(f"  ID: {q_dict.get('id')}")
        print(f"  Title: {q_dict.get('title', '')[:50]}...")

        ev = q_dict.get('evidence_sources', {})
        print(f"  evidence_sources type: {type(ev)}")
        print(f"  evidence_sources keys: {list(ev.keys()) if isinstance(ev, dict) else 'N/A'}")

        if isinstance(ev, dict):
            print(f"  artifacts: {len(ev.get('artifacts', []))} items")
            print(f"  metrics: {len(ev.get('metrics', []))} items")
            print(f"  signals_by_level: {list(ev.get('signals_by_level', {}).keys())}")
            print(f"  sampling_guidance: {len(ev.get('sampling_guidance', ''))} chars")

            # Check the condition at line 713
            has_content = bool(ev.get('artifacts') or ev.get('metrics') or ev.get('signals_by_level'))
            print(f"  Condition (line 713) evaluates to: {has_content}")
        print()

    # Call original function
    result = original_convert_to_question_objects(self, questions_dicts, capacity)

    print("\n" + "="*80)
    print("DEBUG: After _convert_to_question_objects")
    print("="*80)
    print(f"Number of Question objects returned: {len(result)}\n")

    for i, q_obj in enumerate(result, 1):
        print(f"Question {i}:")
        print(f"  has evidence_sources attribute: {hasattr(q_obj, 'evidence_sources')}")
        print(f"  evidence_sources value: {q_obj.evidence_sources}")
        print(f"  evidence_sources is None: {q_obj.evidence_sources is None}")
        print()

    return result

# Apply monkey patch
DOCXToJSONConverter._convert_to_question_objects = debug_convert_to_question_objects

# Test file
test_file = Path('../docs_by_author/EwertonMadruga/Estrutura e Gestão - Ewerton/20251105_checklist_gestao_agil.docx')

print("="*80)
print("Converting file with debug logging")
print("="*80)
print(f"File: {test_file.name}\n")

converter = DOCXToJSONConverter(str(test_file), author="Ewerton Madruga")
result = converter.convert()

print("\n" + "="*80)
print("FINAL JSON RESULT")
print("="*80)

for i, q in enumerate(result.get('questions', []), 1):
    print(f"Question {i}:")
    print(f"  'evidence_sources' in dict: {'evidence_sources' in q}")
    if 'evidence_sources' in q:
        ev = q['evidence_sources']
        print(f"  Evidence content:")
        print(f"    artifacts: {len(ev.get('artifacts', []))}")
        print(f"    metrics: {len(ev.get('metrics', []))}")
        print(f"    signals_by_level: {list(ev.get('signals_by_level', {}).keys())}")
    else:
        print(f"  NO evidence_sources field in JSON!")
    print()

print("="*80)
