#!/usr/bin/env python3
"""
Script to reformat Ewerton's artifacts and metrics from single-blob strings to line-by-line arrays.
Based on Wilson's format seen in the screenshot and JSON files.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any

def split_artifacts_blob(blob: str) -> List[str]:
    """
    Split a single blob of artifacts text into individual line items.

    Handles patterns like:
    - "Artefatos e onde buscar <item1>. <item2>. <item3>."
    - Multiple sentences separated by periods
    """
    # Remove the "Artefatos e onde buscar" prefix if present
    blob = re.sub(r'^Artefatos e onde buscar\s+', '', blob.strip())

    # Split by period followed by space or capital letter
    # This preserves periods within abbreviations or URLs
    items = re.split(r'\.\s+(?=[A-Z])', blob)

    # Clean up each item
    cleaned_items = []
    for item in items:
        item = item.strip()
        if item and not item.endswith('.'):
            item += '.'
        if item and len(item) > 3:  # Skip very short fragments
            cleaned_items.append(item)

    return cleaned_items


def split_metrics_blob(blob: str) -> List[str]:
    """
    Split a single blob of metrics/KPIs text into individual line items.

    Handles patterns like:
    - "Métricas/KPIs <metric1>. <metric2>. <metric3>."
    - Multiple sentences separated by periods
    """
    # Remove the "Métricas/KPIs" prefix if present
    blob = re.sub(r'^Métricas/KPIs\s+', '', blob.strip())

    # Split by period followed by space or capital letter/number
    # This preserves periods within metrics like "3.5%" or "N0:"
    items = re.split(r'\.\s+(?=[A-Z0-9%])', blob)

    # Clean up each item
    cleaned_items = []
    for item in items:
        item = item.strip()
        if item and not item.endswith('.'):
            item += '.'
        if item and len(item) > 3:  # Skip very short fragments
            cleaned_items.append(item)

    return cleaned_items


def process_question(question: Dict[str, Any]) -> bool:
    """
    Process a single question, converting blob artifacts/metrics to arrays.
    Returns True if any changes were made.
    """
    changed = False

    # Process artifacts
    if 'artifacts' in question:
        artifacts = question['artifacts']
        if isinstance(artifacts, list) and len(artifacts) == 1 and isinstance(artifacts[0], str):
            # Single blob string in array
            blob = artifacts[0]
            if len(blob) > 200:  # Likely a blob if very long
                question['artifacts'] = split_artifacts_blob(blob)
                changed = True
                print(f"  - Converted artifacts from blob to {len(question['artifacts'])} items")

    # Process metrics
    if 'metrics' in question:
        metrics = question['metrics']
        if isinstance(metrics, list) and len(metrics) == 1 and isinstance(metrics[0], str):
            # Single blob string in array
            blob = metrics[0]
            if len(blob) > 200:  # Likely a blob if very long
                question['metrics'] = split_metrics_blob(blob)
                changed = True
                print(f"  - Converted metrics from blob to {len(question['metrics'])} items")

    return changed


def process_json_file(file_path: Path) -> bool:
    """
    Process a single JSON file, checking if it's authored by Ewerton and needs reformatting.
    Returns True if the file was modified.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if this is an Ewerton file
        author = data.get('capacity', {}).get('metadata', {}).get('author', '')
        if 'Ewerton' not in author:
            return False

        print(f"\nProcessing: {file_path.name}")
        print(f"  Author: {author}")

        # Process all questions
        questions = data.get('questions', [])
        file_changed = False

        for i, question in enumerate(questions, 1):
            print(f"  Question {i}: {question.get('title', 'Untitled')}")
            if process_question(question):
                file_changed = True

        # Save if changed
        if file_changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  ✓ File updated!")
            return True
        else:
            print(f"  - No changes needed")
            return False

    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all JSON files in the JSON7 data directory."""
    # Find the JSON7 data directory
    script_dir = Path(__file__).parent
    json7_data_dir = script_dir.parent / 'JSON7_20260105_164046' / 'data'

    if not json7_data_dir.exists():
        print(f"Error: Directory not found: {json7_data_dir}")
        return

    print(f"Searching for Ewerton's JSON files in: {json7_data_dir}")
    print("=" * 80)

    # Find all JSON files
    json_files = list(json7_data_dir.rglob('*.json'))
    print(f"Found {len(json_files)} total JSON files")

    # Process each file
    modified_count = 0
    for json_file in json_files:
        if process_json_file(json_file):
            modified_count += 1

    print("\n" + "=" * 80)
    print(f"Summary: Modified {modified_count} file(s)")


if __name__ == '__main__':
    main()
