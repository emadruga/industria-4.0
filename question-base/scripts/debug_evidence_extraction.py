#!/usr/bin/env python3
"""
Debug script to trace evidence extraction through the converter.
"""

import sys
from pathlib import Path
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from extract_evidence import EvidenceExtractor

# Test file
test_file = Path('../docs_by_author/EwertonMadruga/Estrutura e Gestão - Ewerton/20251105_checklist_gestao_agil.docx')

print("="*80)
print("DEBUG: Tracing Evidence Extraction")
print("="*80)
print(f"File: {test_file.name}\n")

doc = Document(str(test_file))
extractor = EvidenceExtractor()

# Simulate the converter's question extraction flow
questions = []
current_question = None
question_counter = 0

print("Processing document elements...\n")

for element in doc.element.body:
    if element.tag.endswith('p'):  # Paragraph
        para = Paragraph(element, doc)
        text = para.text.strip()

        if not text:
            continue

        # Check for new question (simplified pattern)
        if text.startswith('Questão') or text.startswith('Questao'):
            # Save previous question
            if current_question:
                questions.append(current_question)
                print(f"  Saved Question {current_question['question_number']}")
                if current_question['evidence_sources'].get('artifacts') or \
                   current_question['evidence_sources'].get('metrics') or \
                   current_question['evidence_sources'].get('signals_by_level'):
                    print(f"    ✅ HAS evidence!")
                else:
                    print(f"    ❌ NO evidence")

            # Start new question
            question_counter += 1
            current_question = {
                'question_number': question_counter,
                'title': text,
                'evidence_sources': {
                    'artifacts': [],
                    'metrics': [],
                    'signals_by_level': {},
                    'sampling_guidance': ''
                }
            }
            print(f"\n📝 Started Question {question_counter}")

    elif element.tag.endswith('tbl'):  # Table
        table = Table(element, doc)

        if current_question is not None:
            # Check if this table contains evidence
            for row in table.rows:
                cells = row.cells
                if len(cells) < 1:
                    continue

                cell_text = cells[0].text.strip()

                # Look for evidence keyword (line 569 logic)
                if 'evidência' in cell_text.lower() or 'evidence' in cell_text.lower():
                    print(f"  🔍 Found 'evidência' in table for Question {current_question['question_number']}")

                    # Extract evidence from table (line 572 logic)
                    extracted_evidence = extractor.extract_from_table(table)

                    if extracted_evidence:
                        print(f"  ✅ Evidence extracted!")
                        print(f"     Artifacts: {len(extracted_evidence.get('artifacts', []))}")
                        print(f"     Metrics: {len(extracted_evidence.get('metrics', []))}")
                        print(f"     Signals: {list(extracted_evidence.get('signals_by_level', {}).keys())}")
                        print(f"     Sampling: {len(extracted_evidence.get('sampling_guidance', ''))} chars")

                        # Store evidence (line 574 logic)
                        current_question['evidence_sources'] = extracted_evidence
                        print(f"  💾 Stored in current_question['evidence_sources']")
                    else:
                        print(f"  ❌ extractor.extract_from_table() returned None")

                    break  # Only process first matching row per table

# Don't forget the last question
if current_question:
    questions.append(current_question)
    print(f"\n  Saved Question {current_question['question_number']}")
    if current_question['evidence_sources'].get('artifacts') or \
       current_question['evidence_sources'].get('metrics') or \
       current_question['evidence_sources'].get('signals_by_level'):
        print(f"    ✅ HAS evidence!")
    else:
        print(f"    ❌ NO evidence")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total questions found: {len(questions)}\n")

for q in questions:
    ev = q['evidence_sources']
    has_evidence = bool(ev.get('artifacts') or ev.get('metrics') or ev.get('signals_by_level'))

    status = "✅ HAS" if has_evidence else "❌ NO"
    print(f"Question {q['question_number']}: {status} evidence")
    if has_evidence:
        print(f"  - Artifacts: {len(ev.get('artifacts', []))}")
        print(f"  - Metrics: {len(ev.get('metrics', []))}")
        print(f"  - Signals: {list(ev.get('signals_by_level', {}).keys())}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

questions_with_evidence = sum(1 for q in questions if q['evidence_sources'].get('artifacts') or q['evidence_sources'].get('metrics') or q['evidence_sources'].get('signals_by_level'))

if questions_with_evidence > 0:
    print(f"✅ Evidence extraction IS WORKING: {questions_with_evidence}/{len(questions)} questions have evidence")
    print("\nThe issue must be in the JSON serialization or conversion to dataclass objects.")
else:
    print(f"❌ Evidence extraction NOT WORKING: 0/{len(questions)} questions have evidence")
    print("\nThe issue is in the table processing or evidence extraction logic.")
