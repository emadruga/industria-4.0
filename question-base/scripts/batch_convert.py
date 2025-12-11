#!/usr/bin/env python3
"""
Batch DOCX to JSON Converter
Processes multiple DOCX files and organizes output by hierarchy.

Author: Industry 4.0 Team
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse

from docx_to_json_converter import DOCXToJSONConverter


class BatchConverter:
    """Batch convert DOCX files to JSON."""

    def __init__(self, base_dir: str, output_dir: str):
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'total_questions': 0,
            'total_capacities': 0
        }
        self.results = []

    def find_docx_files(self, pattern: str = "**/*.docx") -> List[Path]:
        """Find all DOCX files matching the pattern."""
        files = list(self.base_dir.glob(pattern))
        # Exclude temporary files
        files = [f for f in files if not f.name.startswith('~$')]
        return sorted(files)

    def infer_author(self, docx_path: Path) -> str:
        """Infer author from file path or name."""
        # Check if path contains author names
        path_str = str(docx_path)

        author_mapping = {
            'EwertonMadruga': 'Ewerton Madruga',
            'Ewerton': 'Ewerton Madruga',
            'CristianoGurgelCastro': 'Cristiano Gurgel Castro',
            'cgcastro': 'Cristiano Gurgel Castro',
            'Castro': 'Cristiano Gurgel Castro',
            'FlaviaAgostini': 'Flavia Agostini',
            'Flavia': 'Flavia Agostini',
            'WilsonMeloJr': 'Wilson Melo Jr',
            'Wilson': 'Wilson Melo Jr',
        }

        # Check for author folder names (more specific matches first)
        for key, author in sorted(author_mapping.items(), key=lambda x: len(x[0]), reverse=True):
            if key in path_str:
                return author

        # Default
        return 'Unknown'

    def get_output_path(self, docx_path: Path, capacity_data: Dict) -> Path:
        """Determine output path based on hierarchy."""
        # Extract hierarchy
        block = capacity_data['capacity'].get('block', 'Unknown').replace(' ', '_')
        pilar = capacity_data['capacity'].get('pilar', 'Unknown').replace(' ', '_')
        dimension = capacity_data['capacity'].get('dimension', 'Unknown').replace(' ', '_')

        # Build path: output_dir / Block / Pilar / Dimension / filename.json
        output_path = self.output_dir / 'data' / block / pilar / dimension

        # Create filename from capacity name or original filename
        capacity_name = capacity_data['capacity'].get('name', docx_path.stem)
        filename = capacity_name.replace(' ', '_').lower() + '.json'

        return output_path / filename

    def convert_file(self, docx_path: Path) -> Optional[Dict]:
        """Convert a single DOCX file."""
        try:
            author = self.infer_author(docx_path)
            print(f"\n{'='*60}")
            print(f"Converting: {docx_path.name}")
            print(f"Author: {author}")

            converter = DOCXToJSONConverter(str(docx_path), author=author)
            data = converter.convert()

            # Get output path
            output_path = self.get_output_path(docx_path, data)

            # Save
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✅ Saved to: {output_path.relative_to(self.output_dir)}")

            # Update stats
            self.stats['successful'] += 1
            self.stats['total_capacities'] += 1
            self.stats['total_questions'] += len(data.get('questions', []))

            return {
                'source': str(docx_path),
                'output': str(output_path),
                'status': 'success',
                'capacity': data['capacity'],
                'question_count': len(data.get('questions', []))
            }

        except Exception as e:
            print(f"❌ Error converting {docx_path.name}: {str(e)}")
            self.stats['failed'] += 1
            return {
                'source': str(docx_path),
                'status': 'failed',
                'error': str(e)
            }

    def convert_all(self, pattern: str = "**/*.docx"):
        """Convert all DOCX files."""
        docx_files = self.find_docx_files(pattern)
        self.stats['total_files'] = len(docx_files)

        print(f"Found {len(docx_files)} DOCX files to convert")

        for docx_file in docx_files:
            result = self.convert_file(docx_file)
            if result:
                self.results.append(result)

    def generate_hierarchy(self) -> Dict:
        """Generate hierarchy JSON from converted files."""
        hierarchy = {
            'version': '1.0',
            'last_updated': None,
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

        # Build hierarchy from results
        blocks_dict = {}

        for result in self.results:
            if result['status'] != 'success':
                continue

            capacity = result['capacity']
            block_name = capacity['block']
            pilar_name = capacity['pilar']
            dimension_name = capacity['dimension']

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
            output_path = Path(result['output'])
            relative_path = output_path.relative_to(self.output_dir)

            capacity_ref = {
                'id': capacity['id'],
                'name': capacity['name'],
                'file_path': str(relative_path),
                'question_count': result['question_count'],
                'status': capacity['metadata'].get('status', 'draft')
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

        # Add statistics
        hierarchy['statistics'] = {
            'total_capacities': self.stats['total_capacities'],
            'total_questions': self.stats['total_questions'],
            'total_dimensions': sum(
                len(pilar['dimensions'])
                for block in hierarchy['blocks']
                for pilar in block['pilares']
            ),
            'total_pilares': sum(len(block['pilares']) for block in hierarchy['blocks'])
        }

        return hierarchy

    def save_hierarchy(self):
        """Save hierarchy JSON."""
        hierarchy = self.generate_hierarchy()

        hierarchy_path = self.output_dir / 'metadata' / 'hierarchy.json'
        hierarchy_path.parent.mkdir(parents=True, exist_ok=True)

        with open(hierarchy_path, 'w', encoding='utf-8') as f:
            json.dump(hierarchy, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Hierarchy saved to: {hierarchy_path}")

    def print_summary(self):
        """Print conversion summary."""
        print("\n" + "="*60)
        print("CONVERSION SUMMARY")
        print("="*60)
        print(f"Total files: {self.stats['total_files']}")
        print(f"Successful: {self.stats['successful']} ✅")
        print(f"Failed: {self.stats['failed']} ❌")
        print(f"Total capacities: {self.stats['total_capacities']}")
        print(f"Total questions: {self.stats['total_questions']}")

        if self.stats['total_capacities'] > 0:
            avg_questions = self.stats['total_questions'] / self.stats['total_capacities']
            print(f"Average questions per capacity: {avg_questions:.1f}")

        # Print failed files
        if self.stats['failed'] > 0:
            print("\nFailed conversions:")
            for result in self.results:
                if result['status'] == 'failed':
                    print(f"  ❌ {Path(result['source']).name}: {result.get('error', 'Unknown error')}")

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
        """Generate a short code from a name."""
        words = name.split()
        if len(words) >= 2:
            return ''.join([w[0].upper() for w in words[:2]])
        return name[:2].upper() if name else 'UN'


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Batch convert Industry 4.0 DOCX files to JSON'
    )
    parser.add_argument('input_dir', help='Directory containing DOCX files')
    parser.add_argument('-o', '--output', default='question-base',
                        help='Output directory (default: question-base)')
    parser.add_argument('-p', '--pattern', default='**/*.docx',
                        help='File pattern (default: **/*.docx)')
    parser.add_argument('--no-hierarchy', action='store_true',
                        help='Skip hierarchy generation')

    args = parser.parse_args()

    # Run batch conversion
    converter = BatchConverter(args.input_dir, args.output)
    converter.convert_all(pattern=args.pattern)

    # Generate hierarchy
    if not args.no_hierarchy:
        converter.save_hierarchy()

    # Print summary
    converter.print_summary()

    # Exit with error code if any conversions failed
    sys.exit(0 if converter.stats['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
