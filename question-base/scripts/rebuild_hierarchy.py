#!/usr/bin/env python3
"""
Rebuild hierarchy.json from existing JSON files in a directory.
"""

import json
from pathlib import Path
from collections import defaultdict
import sys

def rebuild_hierarchy(base_dir):
    """Rebuild hierarchy from JSON files."""
    base_dir = Path(base_dir)
    data_dir = base_dir / 'data'
    metadata_dir = base_dir / 'metadata'

    # Find all JSON files
    json_files = sorted(data_dir.rglob('*.json'))
    print(f"Found {len(json_files)} JSON files\n")

    # Build hierarchy structure
    hierarchy = {
        "version": "1.0",
        "last_updated": None,
        "description": "Industry 4.0 Maturity Model Hierarchy",
        "source_frameworks": [
            {"name": "ACATECH", "version": "2020", "url": "https://en.acatech.de/publication/industrie-4-0-maturity-index-update-2020/", "year": 2020},
            {"name": "SIRI", "version": "2025", "url": "https://www.edb.gov.sg/en/about-edb/media-releases-publications/the-smart-industry-readiness-index.html", "year": 2021}
        ],
        "blocks": []
    }

    # Organize capacities and keep full JSON data for markdown generation
    blocks_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    json_data_map = {}  # Map file path to full JSON data
    total_questions = 0

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        json_data_map[str(json_file)] = data

        capacity = data.get('capacity', {})
        block = capacity.get('block', 'Unknown')
        pilar = capacity.get('pilar', 'Unknown')
        dimension = capacity.get('dimension', 'Unknown')

        capacity_entry = {
            "id": capacity.get('id', ''),
            "name": capacity.get('name', ''),
            "file_path": str(json_file.relative_to(base_dir)),
            "question_count": len(data.get('questions', [])),
            "status": capacity.get('metadata', {}).get('status', 'draft')
        }

        blocks_dict[block][pilar][dimension].append(capacity_entry)
        total_questions += capacity_entry['question_count']

    # Build blocks structure
    for block_name in sorted(blocks_dict.keys()):
        block_entry = {
            "name": block_name,
            "code": block_name[:3].upper(),
            "pilares": []
        }

        for pilar_name in sorted(blocks_dict[block_name].keys()):
            pilar_entry = {
                "name": pilar_name,
                "code": pilar_name[:2].upper(),
                "dimensions": []
            }

            for dimension_name in sorted(blocks_dict[block_name][pilar_name].keys()):
                dimension_entry = {
                    "name": dimension_name,
                    "code": dimension_name[:2].upper(),
                    "capacities": blocks_dict[block_name][pilar_name][dimension_name]
                }
                pilar_entry["dimensions"].append(dimension_entry)

            block_entry["pilares"].append(pilar_entry)

        hierarchy["blocks"].append(block_entry)

    # Add statistics
    hierarchy["statistics"] = {
        "total_capacities": len(json_files),
        "total_questions": total_questions,
        "total_dimensions": sum(len(blocks_dict[b][p]) for b in blocks_dict for p in blocks_dict[b]),
        "total_pilares": sum(len(blocks_dict[b]) for b in blocks_dict)
    }

    # Save hierarchy
    output_file = metadata_dir / 'hierarchy.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hierarchy, f, ensure_ascii=False, indent=2)

    print(f"✅ Hierarchy saved to: {output_file}")

    # Generate hierarchy table markdown
    table_file = metadata_dir / 'hierarchy_table.md'
    with open(table_file, 'w', encoding='utf-8') as f:
        f.write("# Industry 4.0 Maturity Model - Question Hierarchy\n\n")
        f.write("Complete hierarchical view from blocks to individual questions.\n\n")
        f.write(f"**Total Questions:** {total_questions}\n")
        f.write(f"**Total Capacities:** {len(json_files)}\n\n")
        f.write("---\n\n")
        f.write("| Block | Pilar | Dimension | Capacity | Question Code | Question Title |\n")
        f.write("|-------|-------|-----------|----------|---------------|----------------|\n")

        # Iterate through hierarchy and generate table rows
        for block_name in sorted(blocks_dict.keys()):
            for pilar_name in sorted(blocks_dict[block_name].keys()):
                for dimension_name in sorted(blocks_dict[block_name][pilar_name].keys()):
                    for capacity_entry in blocks_dict[block_name][pilar_name][dimension_name]:
                        # Load full JSON data for this capacity
                        json_file_path = base_dir / capacity_entry['file_path']
                        full_data = json_data_map[str(json_file_path)]
                        capacity_name = full_data['capacity']['name']

                        # Get all questions for this capacity
                        questions = full_data.get('questions', [])
                        for question in questions:
                            question_code = question.get('id', '')
                            question_title = question.get('title', '')
                            f.write(f"| {block_name} | {pilar_name} | {dimension_name} | {capacity_name} | `{question_code}` | {question_title} |\n")

        f.write("\n---\n\n")
        f.write("*Generated automatically from Industry 4.0 maturity assessment documents*\n")

    print(f"✅ Hierarchy table saved to: {table_file}")

    print(f"\nStatistics:")
    print(f"  Total capacities: {hierarchy['statistics']['total_capacities']}")
    print(f"  Total questions: {hierarchy['statistics']['total_questions']}")
    print(f"  Total dimensions: {hierarchy['statistics']['total_dimensions']}")
    print(f"  Total pilares: {hierarchy['statistics']['total_pilares']}")
    print(f"  Total blocks: {len(hierarchy['blocks'])}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python rebuild_hierarchy.py <path_to_json_base_dir>")
        sys.exit(1)

    rebuild_hierarchy(sys.argv[1])
