#!/usr/bin/env python3
"""
JSON Validation Framework for Industry 4.0 Maturity Model Questions
Validates question JSON files against the defined schemas.

Author: Industry 4.0 Team
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

try:
    import jsonschema
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema is required. Install with: pip install jsonschema")
    sys.exit(1)


@dataclass
class ValidationResult:
    """Result of validation."""
    is_valid: bool
    file_path: str
    errors: List[str]
    warnings: List[str]
    info: Dict


class QuestionValidator:
    """Validates Industry 4.0 question JSON files."""

    def __init__(self, schema_dir: str = None):
        if schema_dir is None:
            # Default to ../schema relative to this script
            script_dir = Path(__file__).parent
            schema_dir = script_dir.parent / 'schema'

        self.schema_dir = Path(schema_dir)
        self.question_schema = self._load_schema('question-schema.json')
        self.hierarchy_schema = self._load_schema('hierarchy-schema.json')

    def _load_schema(self, schema_name: str) -> Dict:
        """Load a JSON schema file."""
        schema_path = self.schema_dir / schema_name
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")

        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate_question_file(self, json_file: str) -> ValidationResult:
        """Validate a question JSON file."""
        json_path = Path(json_file)

        if not json_path.exists():
            return ValidationResult(
                is_valid=False,
                file_path=str(json_path),
                errors=[f"File not found: {json_path}"],
                warnings=[],
                info={}
            )

        # Load JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid=False,
                file_path=str(json_path),
                errors=[f"Invalid JSON: {str(e)}"],
                warnings=[],
                info={}
            )

        errors = []
        warnings = []
        info = {}

        # Validate against schema
        try:
            validate(instance=data, schema=self.question_schema)
        except ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
            errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")

        # Additional semantic validations
        if 'capacity' in data:
            capacity = data['capacity']

            # Check if capacity ID matches file structure
            expected_id_prefix = self._generate_id_prefix(capacity)
            if not capacity['id'].startswith(expected_id_prefix):
                warnings.append(
                    f"Capacity ID '{capacity['id']}' doesn't match expected prefix '{expected_id_prefix}'"
                )

            # Collect info
            info['capacity_name'] = capacity.get('name', 'Unknown')
            info['block'] = capacity.get('block', 'Unknown')
            info['pilar'] = capacity.get('pilar', 'Unknown')
            info['dimension'] = capacity.get('dimension', 'Unknown')

        if 'questions' in data:
            questions = data['questions']
            info['question_count'] = len(questions)

            # Check for duplicate question IDs
            question_ids = [q['id'] for q in questions if 'id' in q]
            if len(question_ids) != len(set(question_ids)):
                errors.append("Duplicate question IDs found")

            # Check question numbering
            question_numbers = [q['question_number'] for q in questions if 'question_number' in q]
            expected_numbers = list(range(1, len(questions) + 1))
            if question_numbers != expected_numbers:
                warnings.append(
                    f"Question numbers are not sequential: {question_numbers}"
                )

            # Check maturity levels
            for i, question in enumerate(questions, 1):
                if 'maturity_levels' in question:
                    levels = [ml['level'] for ml in question['maturity_levels']]

                    # Check if levels are sequential starting from 0
                    expected_levels = list(range(len(levels)))
                    if levels != expected_levels:
                        warnings.append(
                            f"Question {i}: Maturity levels not sequential: {levels}"
                        )

                    # Check if we have 6 or 7 levels (0-5 or 0-6)
                    if len(levels) not in [6, 7]:
                        warnings.append(
                            f"Question {i}: Expected 6-7 maturity levels, found {len(levels)}"
                        )

                    info[f'q{i}_maturity_levels'] = len(levels)

                # Check if question text is not empty
                if not question.get('text', '').strip():
                    warnings.append(f"Question {i}: Empty question text")

                # Check if title is not empty
                if not question.get('title', '').strip():
                    warnings.append(f"Question {i}: Empty title")

        # Overall validation result
        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            file_path=str(json_path),
            errors=errors,
            warnings=warnings,
            info=info
        )

    def validate_hierarchy_file(self, json_file: str) -> ValidationResult:
        """Validate a hierarchy JSON file."""
        json_path = Path(json_file)

        if not json_path.exists():
            return ValidationResult(
                is_valid=False,
                file_path=str(json_path),
                errors=[f"File not found: {json_path}"],
                warnings=[],
                info={}
            )

        # Load JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid=False,
                file_path=str(json_path),
                errors=[f"Invalid JSON: {str(e)}"],
                warnings=[],
                info={}
            )

        errors = []
        warnings = []
        info = {}

        # Validate against schema
        try:
            validate(instance=data, schema=self.hierarchy_schema)
        except ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
            errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")

        # Count elements
        if 'blocks' in data:
            info['block_count'] = len(data['blocks'])

            total_pilares = 0
            total_dimensions = 0
            total_capacities = 0

            for block in data['blocks']:
                pilares = block.get('pilares', [])
                total_pilares += len(pilares)

                for pilar in pilares:
                    dimensions = pilar.get('dimensions', [])
                    total_dimensions += len(dimensions)

                    for dimension in dimensions:
                        capacities = dimension.get('capacities', [])
                        total_capacities += len(capacities)

            info['pilar_count'] = total_pilares
            info['dimension_count'] = total_dimensions
            info['capacity_count'] = total_capacities

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            file_path=str(json_path),
            errors=errors,
            warnings=warnings,
            info=info
        )

    def validate_directory(self, directory: str, pattern: str = "*.json") -> List[ValidationResult]:
        """Validate all JSON files in a directory."""
        dir_path = Path(directory)

        if not dir_path.exists():
            print(f"Error: Directory not found: {dir_path}")
            return []

        results = []
        json_files = list(dir_path.glob(pattern))

        if not json_files:
            print(f"No JSON files found in {dir_path}")
            return []

        print(f"Validating {len(json_files)} files in {dir_path}...")

        for json_file in json_files:
            # Determine if this is a hierarchy or question file
            if 'hierarchy' in json_file.name.lower():
                result = self.validate_hierarchy_file(str(json_file))
            else:
                result = self.validate_question_file(str(json_file))

            results.append(result)

        return results

    def _generate_id_prefix(self, capacity: Dict) -> str:
        """Generate expected ID prefix from capacity metadata."""
        block = capacity.get('block', '')
        pilar = capacity.get('pilar', '')
        dimension = capacity.get('dimension', '')

        block_code = self._get_block_code(block)
        pilar_code = self._get_pilar_code(pilar)
        dim_code = self._get_dimension_code(dimension)

        return f"CAP-{block_code}-{pilar_code}-{dim_code}"

    def _get_block_code(self, block: str) -> str:
        """Get short code for block."""
        mapping = {
            'Organização': 'ORG',
            'Organizacao': 'ORG',
            'Processo': 'PROC',
            'Tecnologia': 'TEC'
        }
        return mapping.get(block, 'UNK')

    def _get_pilar_code(self, pilar: str) -> str:
        """Get short code for pilar."""
        words = pilar.split()
        if len(words) >= 2:
            return ''.join([w[0].upper() for w in words[:2]])
        return pilar[:2].upper() if pilar else 'UN'

    def _get_dimension_code(self, dimension: str) -> str:
        """Get short code for dimension."""
        words = dimension.split()
        if len(words) >= 2:
            return ''.join([w[0].upper() for w in words[:2]])
        return dimension[:2].upper() if dimension else 'UN'


def print_validation_result(result: ValidationResult, verbose: bool = False):
    """Print a validation result in a formatted way."""
    status = "✅ VALID" if result.is_valid else "❌ INVALID"
    file_name = Path(result.file_path).name

    print(f"\n{status}: {file_name}")

    if result.errors:
        print("  Errors:")
        for error in result.errors:
            print(f"    • {error}")

    if result.warnings:
        print("  Warnings:")
        for warning in result.warnings:
            print(f"    ⚠ {warning}")

    if verbose and result.info:
        print("  Info:")
        for key, value in result.info.items():
            print(f"    • {key}: {value}")


def print_summary(results: List[ValidationResult]):
    """Print a summary of validation results."""
    total = len(results)
    valid = sum(1 for r in results if r.is_valid)
    invalid = total - valid

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {total}")
    print(f"Valid: {valid} ✅")
    print(f"Invalid: {invalid} ❌")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")

    # Count questions
    total_questions = 0
    total_capacities = 0

    for result in results:
        if 'question_count' in result.info:
            total_questions += result.info['question_count']
        if 'capacity_name' in result.info:
            total_capacities += 1

    if total_capacities > 0:
        print(f"\nTotal capacities: {total_capacities}")
        print(f"Total questions: {total_questions}")
        if total_capacities > 0:
            print(f"Average questions per capacity: {total_questions / total_capacities:.1f}")


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate Industry 4.0 question JSON files'
    )
    parser.add_argument('path', help='JSON file or directory to validate')
    parser.add_argument('-s', '--schema-dir', help='Directory containing schemas')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively validate directories')
    parser.add_argument('--pattern', default='*.json', help='File pattern for directory validation')

    args = parser.parse_args()

    # Initialize validator
    validator = QuestionValidator(schema_dir=args.schema_dir)

    path = Path(args.path)
    results = []

    if path.is_file():
        # Validate single file
        if 'hierarchy' in path.name.lower():
            result = validator.validate_hierarchy_file(str(path))
        else:
            result = validator.validate_question_file(str(path))
        results.append(result)
        print_validation_result(result, verbose=args.verbose)

    elif path.is_dir():
        # Validate directory
        if args.recursive:
            pattern = f"**/{args.pattern}"
        else:
            pattern = args.pattern

        json_files = list(path.glob(pattern))

        for json_file in json_files:
            if 'hierarchy' in json_file.name.lower():
                result = validator.validate_hierarchy_file(str(json_file))
            else:
                result = validator.validate_question_file(str(json_file))
            results.append(result)
            print_validation_result(result, verbose=args.verbose)

    else:
        print(f"Error: Path not found: {path}")
        sys.exit(1)

    # Print summary
    if len(results) > 1:
        print_summary(results)

    # Exit code
    if all(r.is_valid for r in results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
