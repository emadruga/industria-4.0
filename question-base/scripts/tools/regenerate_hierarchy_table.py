#!/usr/bin/env python3
"""
Regenerate Hierarchy Files from JSON Question Base

This script scans all JSON files in the question base and regenerates:
- hierarchy.json: Complete hierarchical structure
- hierarchy_table.md: Markdown table showing all questions

Author: Industry 4.0 Team
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import argparse
from datetime import datetime


class HierarchyRegenerator:
    """Regenerates hierarchy files from existing JSON question base."""

    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.stats = {
            'total_files': 0,
            'total_capacities': 0,
            'total_questions': 0,
            'total_dimensions': 0,
            'total_pilares': 0,
            'total_blocks': 0
        }
        self.json_files = []

    def find_json_files(self) -> List[Path]:
        """Find all JSON files in the data directory."""
        files = list(self.data_dir.rglob("*.json"))
        # Exclude metadata files
        files = [f for f in files if 'metadata' not in str(f)]
        return sorted(files)

    def load_json_data(self, json_path: Path) -> Dict:
        """Load JSON file and extract relevant data."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            capacity = data.get('capacity', {})
            questions = data.get('questions', [])

            return {
                'file_path': json_path,
                'relative_path': json_path.relative_to(self.data_dir.parent),
                'capacity': capacity,
                'questions': questions,
                'question_count': len(questions)
            }
        except Exception as e:
            print(f"❌ Error loading {json_path}: {e}")
            return None

    def generate_hierarchy(self) -> Dict:
        """Generate hierarchy JSON from JSON files."""
        hierarchy = {
            'version': '1.0',
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'description': 'Industry 4.0 Maturity Model Hierarchy',
            'source_frameworks': [
                {
                    'name': 'ACATECH',
                    'version': '2020',
                    'url': 'https://en.acatech.de/publication/industrie-4-0-maturity-index-update-2020/',
                    'year': 2020
                },
                {
                    'name': 'SIRI',
                    'version': '2025',
                    'url': 'https://www.edb.gov.sg/en/about-edb/media-releases-publications/the-smart-industry-readiness-index.html',
                    'year': 2021
                }
            ],
            'blocks': []
        }

        # Build hierarchy from JSON files
        blocks_dict = {}

        for json_data in self.json_files:
            if not json_data:
                continue

            capacity = json_data['capacity']
            block_name = capacity.get('block', 'Unknown')
            pilar_name = capacity.get('pilar', 'Unknown')
            dimension_name = capacity.get('dimension', 'Unknown')

            # Initialize block
            if block_name not in blocks_dict:
                blocks_dict[block_name] = {
                    'name': block_name,
                    'code': self._get_block_code(block_name),
                    'pilares': {}
                }

            # Initialize pilar
            if pilar_name not in blocks_dict[block_name]['pilares']:
                blocks_dict[block_name]['pilares'][pilar_name] = {
                    'name': pilar_name,
                    'code': self._get_code(pilar_name),
                    'dimensions': {}
                }

            # Initialize dimension
            if dimension_name not in blocks_dict[block_name]['pilares'][pilar_name]['dimensions']:
                blocks_dict[block_name]['pilares'][pilar_name]['dimensions'][dimension_name] = {
                    'name': dimension_name,
                    'code': self._get_code(dimension_name),
                    'capacities': []
                }

            # Add capacity reference
            capacity_ref = {
                'id': capacity.get('id', 'N/A'),
                'name': capacity.get('name', 'Unknown'),
                'file_path': str(json_data['relative_path']),
                'question_count': json_data['question_count'],
                'status': capacity.get('metadata', {}).get('status', 'draft')
            }

            blocks_dict[block_name]['pilares'][pilar_name]['dimensions'][dimension_name]['capacities'].append(capacity_ref)

        # Convert to list structure
        for block_name, block_data in blocks_dict.items():
            pilares = []
            for pilar_name, pilar_data in block_data['pilares'].items():
                dimensions = []
                for dim_name, dim_data in pilar_data['dimensions'].items():
                    dimensions.append({
                        'name': dim_data['name'],
                        'code': dim_data['code'],
                        'capacities': dim_data['capacities']
                    })
                pilares.append({
                    'name': pilar_data['name'],
                    'code': pilar_data['code'],
                    'dimensions': dimensions
                })

            hierarchy['blocks'].append({
                'name': block_data['name'],
                'code': block_data['code'],
                'pilares': pilares
            })

        # Calculate statistics
        self.stats['total_blocks'] = len(hierarchy['blocks'])
        self.stats['total_pilares'] = sum(len(block['pilares']) for block in hierarchy['blocks'])
        self.stats['total_dimensions'] = sum(
            len(pilar['dimensions'])
            for block in hierarchy['blocks']
            for pilar in block['pilares']
        )

        # Add statistics to hierarchy
        hierarchy['statistics'] = {
            'total_capacities': self.stats['total_capacities'],
            'total_questions': self.stats['total_questions'],
            'total_dimensions': self.stats['total_dimensions'],
            'total_pilares': self.stats['total_pilares'],
            'total_blocks': self.stats['total_blocks']
        }

        return hierarchy

    def save_hierarchy_json(self, hierarchy: Dict):
        """Save hierarchy JSON file."""
        hierarchy_path = self.output_dir / 'hierarchy.json'
        hierarchy_path.parent.mkdir(parents=True, exist_ok=True)

        with open(hierarchy_path, 'w', encoding='utf-8') as f:
            json.dump(hierarchy, f, ensure_ascii=False, indent=2)

        print(f"✅ Hierarchy JSON saved to: {hierarchy_path}")

    def generate_hierarchy_markdown(self) -> str:
        """Generate markdown table showing hierarchical structure down to questions."""
        lines = []

        # Add header
        lines.append("# Industry 4.0 Maturity Model - Question Hierarchy")
        lines.append("")
        lines.append("Complete hierarchical view from blocks to individual questions.")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Total Questions:** {self.stats['total_questions']}")
        lines.append(f"**Total Capacities:** {self.stats['total_capacities']}")
        lines.append(f"**Total Dimensions:** {self.stats['total_dimensions']}")
        lines.append(f"**Total Pilares:** {self.stats['total_pilares']}")
        lines.append(f"**Total Blocks:** {self.stats['total_blocks']}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Add table header
        lines.append("| Block | Pilar | Dimension | Capacity | Question Code | Question Title |")
        lines.append("|-------|-------|-----------|----------|---------------|----------------|")

        # Sort JSON files by hierarchy
        sorted_files = sorted(
            [f for f in self.json_files if f],
            key=lambda f: (
                f['capacity'].get('block', ''),
                f['capacity'].get('pilar', ''),
                f['capacity'].get('dimension', ''),
                f['capacity'].get('name', '')
            )
        )

        # Process each file
        for json_data in sorted_files:
            capacity = json_data['capacity']
            block = capacity.get('block', 'Unknown')
            pilar = capacity.get('pilar', 'Unknown')
            dimension = capacity.get('dimension', 'Unknown')
            capacity_name = capacity.get('name', 'Unknown')
            questions = json_data['questions']

            if questions:
                # Add a row for each question
                for question in questions:
                    q_id = question.get('id', 'N/A')
                    q_title = question.get('title', 'N/A')

                    # Escape pipe characters in text
                    q_title = q_title.replace('|', '\\|')

                    lines.append(f"| {block} | {pilar} | {dimension} | {capacity_name} | `{q_id}` | {q_title} |")
            else:
                # Add row for capacity without questions
                lines.append(f"| {block} | {pilar} | {dimension} | {capacity_name} | - | *No questions* |")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*Generated automatically from Industry 4.0 maturity assessment JSON files*")
        lines.append("")

        return '\n'.join(lines)

    def save_hierarchy_markdown(self, markdown: str):
        """Save hierarchy markdown table."""
        md_path = self.output_dir / 'hierarchy_table.md'
        md_path.parent.mkdir(parents=True, exist_ok=True)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"✅ Hierarchy table saved to: {md_path}")

    def regenerate(self):
        """Main regeneration process."""
        print("="*60)
        print("REGENERATING HIERARCHY FILES")
        print("="*60)
        print(f"Data directory: {self.data_dir}")
        print(f"Output directory: {self.output_dir}")
        print("")

        # Find all JSON files
        print("Scanning for JSON files...")
        json_files = self.find_json_files()
        self.stats['total_files'] = len(json_files)
        print(f"Found {len(json_files)} JSON files")
        print("")

        # Load all JSON data
        print("Loading JSON files...")
        for json_path in json_files:
            json_data = self.load_json_data(json_path)
            if json_data:
                self.json_files.append(json_data)
                self.stats['total_capacities'] += 1
                self.stats['total_questions'] += json_data['question_count']

        print(f"Loaded {self.stats['total_capacities']} capacities")
        print(f"Total questions: {self.stats['total_questions']}")
        print("")

        # Generate hierarchy
        print("Generating hierarchy structure...")
        hierarchy = self.generate_hierarchy()

        # Save hierarchy JSON
        print("Saving hierarchy JSON...")
        self.save_hierarchy_json(hierarchy)
        print("")

        # Generate and save markdown
        print("Generating hierarchy markdown table...")
        markdown = self.generate_hierarchy_markdown()
        self.save_hierarchy_markdown(markdown)
        print("")

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print regeneration summary."""
        print("="*60)
        print("REGENERATION SUMMARY")
        print("="*60)
        print(f"Total JSON files processed: {self.stats['total_files']}")
        print(f"Total blocks: {self.stats['total_blocks']}")
        print(f"Total pilares: {self.stats['total_pilares']}")
        print(f"Total dimensions: {self.stats['total_dimensions']}")
        print(f"Total capacities: {self.stats['total_capacities']}")
        print(f"Total questions: {self.stats['total_questions']}")

        if self.stats['total_capacities'] > 0:
            avg_questions = self.stats['total_questions'] / self.stats['total_capacities']
            print(f"Average questions per capacity: {avg_questions:.1f}")

        print("")
        print("✅ Hierarchy files regenerated successfully!")

    def _get_block_code(self, block: str) -> str:
        """Get short code for block."""
        mapping = {
            'Organização': 'ORG',
            'Organizacao': 'ORG',
            'Processo': 'PROC',
            'Tecnologia': 'TEC'
        }
        return mapping.get(block, 'UNK')

    def _get_code(self, name: str) -> str:
        """Generate a short code from a name, ignoring '(' and other non-alphabetic chars."""
        words = name.split()

        # Get valid characters from first letters of words
        code_chars = []
        for word in words[:4]:  # Check up to 4 words to get 2 valid chars
            # Skip empty words and find first alphabetic character
            for char in word:
                if char.isalpha():  # Only use alphabetic characters
                    code_chars.append(char.upper())
                    break
            if len(code_chars) >= 2:
                break

        if len(code_chars) >= 2:
            return ''.join(code_chars[:2])

        # If we don't have 2 chars yet, get from first word with valid letters
        if len(code_chars) < 2:
            for word in words:
                clean_word = ''.join([c for c in word if c.isalpha()])
                if len(clean_word) >= 2:
                    # Use the first 2 letters from this clean word
                    return clean_word[:2].upper()
                elif len(clean_word) == 1 and len(code_chars) == 0:
                    code_chars.append(clean_word[0].upper())

        # Final fallback: get first 2 alphabetic characters from entire name
        alpha_chars = [c.upper() for c in name if c.isalpha()]
        if len(alpha_chars) >= 2:
            return ''.join(alpha_chars[:2])

        return 'UN'  # Default if nothing works


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Regenerate hierarchy files from Industry 4.0 JSON question base'
    )
    parser.add_argument(
        'data_dir',
        nargs='?',
        default='question-base/JSON/data',
        help='Directory containing JSON files (default: question-base/JSON/data)'
    )
    parser.add_argument(
        '-o', '--output',
        default='question-base/JSON/metadata',
        help='Output directory for hierarchy files (default: question-base/JSON/metadata)'
    )

    args = parser.parse_args()

    # Run regeneration
    regenerator = HierarchyRegenerator(args.data_dir, args.output)
    regenerator.regenerate()

    sys.exit(0)


if __name__ == '__main__':
    main()
