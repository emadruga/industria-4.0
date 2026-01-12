#!/usr/bin/env python3
"""
JSON Consistency Checker for Industry 4.0 Maturity Questions Catalog

This script validates the consistency and completeness of JSON files in the maturity
questions catalog, checking for:
- Schema compliance
- Required fields presence
- Data type consistency
- Value format validation
- Cross-file consistency
- Author-specific patterns

Usage:
    python json_consistency_check.py <data_directory>
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class ValidationIssue:
    """Represents a validation issue found in a JSON file"""
    file_path: str
    severity: str  # 'ERROR', 'WARNING', 'INFO'
    category: str
    message: str
    location: str = ""


@dataclass
class ValidationReport:
    """Aggregates validation results"""
    total_files: int = 0
    valid_files: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    authors: Set[str] = field(default_factory=set)
    frameworks: Set[str] = field(default_factory=set)

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)

    def get_errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == 'ERROR']

    def get_warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == 'WARNING']

    def get_info(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == 'INFO']


class JSONConsistencyChecker:
    """Main validator class for JSON catalog consistency"""

    # Expected schema structure
    REQUIRED_TOP_LEVEL_KEYS = {'capacity', 'questions', 'references'}

    REQUIRED_CAPACITY_KEYS = {
        'id', 'name', 'block', 'pilar', 'dimension',
        'description', 'related_capacities', 'metadata'
    }

    REQUIRED_METADATA_KEYS = {
        'source_frameworks', 'author', 'version',
        'last_updated', 'source_docx', 'status'
    }

    REQUIRED_QUESTION_KEYS = {
        'id', 'question_number', 'title', 'text',
        'maturity_levels', 'artifacts', 'metrics', 'sampling_guidance'
    }

    REQUIRED_MATURITY_LEVEL_KEYS = {
        'level', 'label', 'description', 'evidence_signals'
    }

    REQUIRED_EVIDENCE_SIGNALS_KEYS = {'observable_behaviors'}

    REQUIRED_REFERENCE_KEYS = {'citation'}

    VALID_BLOCKS = {'Organização', 'Processo', 'Tecnologia'}
    VALID_FRAMEWORKS = {'ACATECH', 'SIRI'}
    VALID_STATUSES = {'draft', 'review', 'approved', 'published'}

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.report = ValidationReport()

    def validate_all_files(self) -> ValidationReport:
        """Validate all JSON files in the data directory"""
        json_files = list(self.data_dir.rglob('*.json'))

        if not json_files:
            print(f"No JSON files found in {self.data_dir}")
            return self.report

        self.report.total_files = len(json_files)
        print(f"Found {len(json_files)} JSON files to validate\n")

        for json_file in sorted(json_files):
            self._validate_file(json_file)

        self.report.valid_files = self.report.total_files - len([
            i for i in self.report.issues if i.severity == 'ERROR'
        ])

        return self.report

    def _validate_file(self, file_path: Path):
        """Validate a single JSON file"""
        rel_path = file_path.relative_to(self.data_dir.parent)
        print(f"Validating: {rel_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.report.add_issue(ValidationIssue(
                file_path=str(rel_path),
                severity='ERROR',
                category='JSON_SYNTAX',
                message=f"Invalid JSON syntax: {str(e)}"
            ))
            return
        except Exception as e:
            self.report.add_issue(ValidationIssue(
                file_path=str(rel_path),
                severity='ERROR',
                category='FILE_ACCESS',
                message=f"Cannot read file: {str(e)}"
            ))
            return

        # Validate structure
        self._validate_top_level_structure(data, rel_path)
        self._validate_capacity(data.get('capacity', {}), rel_path)
        self._validate_questions(data.get('questions', []), rel_path)
        self._validate_references(data.get('references', []), rel_path)

    def _validate_top_level_structure(self, data: Dict, file_path: Path):
        """Validate top-level structure"""
        missing_keys = self.REQUIRED_TOP_LEVEL_KEYS - set(data.keys())
        if missing_keys:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='STRUCTURE',
                message=f"Missing top-level keys: {', '.join(missing_keys)}"
            ))

        extra_keys = set(data.keys()) - self.REQUIRED_TOP_LEVEL_KEYS
        if extra_keys:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='INFO',
                category='STRUCTURE',
                message=f"Extra top-level keys: {', '.join(extra_keys)}"
            ))

    def _validate_capacity(self, capacity: Dict, file_path: Path):
        """Validate capacity section"""
        if not capacity:
            return

        # Check required fields
        missing_keys = self.REQUIRED_CAPACITY_KEYS - set(capacity.keys())
        if missing_keys:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='CAPACITY',
                location='capacity',
                message=f"Missing capacity fields: {', '.join(missing_keys)}"
            ))

        # Validate ID format
        cap_id = capacity.get('id', '')
        if cap_id and not cap_id.startswith('CAP-'):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='CAPACITY_ID',
                location='capacity.id',
                message=f"Capacity ID should start with 'CAP-': {cap_id}"
            ))

        # Validate block
        block = capacity.get('block', '')
        if block and block not in self.VALID_BLOCKS:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='CAPACITY_BLOCK',
                location='capacity.block',
                message=f"Invalid block value: '{block}'. Must be one of {self.VALID_BLOCKS}"
            ))

        # Validate description length
        description = capacity.get('description', '')
        if description and len(description) < 100:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='CAPACITY_DESCRIPTION',
                location='capacity.description',
                message=f"Description is too short ({len(description)} chars). Consider expanding."
            ))

        # Validate related_capacities
        related = capacity.get('related_capacities', [])
        if not isinstance(related, list):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='CAPACITY_RELATED',
                location='capacity.related_capacities',
                message="related_capacities must be a list"
            ))

        # Validate metadata
        self._validate_metadata(capacity.get('metadata', {}), file_path)

    def _validate_metadata(self, metadata: Dict, file_path: Path):
        """Validate metadata section"""
        if not metadata:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='METADATA',
                location='capacity.metadata',
                message="Missing metadata section"
            ))
            return

        # Check required fields
        missing_keys = self.REQUIRED_METADATA_KEYS - set(metadata.keys())
        if missing_keys:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='METADATA',
                location='capacity.metadata',
                message=f"Missing metadata fields: {', '.join(missing_keys)}"
            ))

        # Track author
        author = metadata.get('author', '')
        if author:
            self.report.authors.add(author)

        # Validate frameworks
        frameworks = metadata.get('source_frameworks', [])
        if not isinstance(frameworks, list):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='METADATA_FRAMEWORKS',
                location='capacity.metadata.source_frameworks',
                message="source_frameworks must be a list"
            ))
        else:
            for fw in frameworks:
                self.report.frameworks.add(fw)
                if fw not in self.VALID_FRAMEWORKS:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='WARNING',
                        category='METADATA_FRAMEWORKS',
                        location='capacity.metadata.source_frameworks',
                        message=f"Unknown framework: '{fw}'. Expected: {self.VALID_FRAMEWORKS}"
                    ))

        # Validate version format
        version = metadata.get('version', '')
        if version and not self._is_valid_version(version):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='METADATA_VERSION',
                location='capacity.metadata.version',
                message=f"Version format should be semantic (e.g., '1.0'): {version}"
            ))

        # Validate date format
        last_updated = metadata.get('last_updated', '')
        if last_updated and not self._is_valid_date(last_updated):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='METADATA_DATE',
                location='capacity.metadata.last_updated',
                message=f"Date should be in YYYY-MM-DD format: {last_updated}"
            ))

        # Validate status
        status = metadata.get('status', '')
        if status and status not in self.VALID_STATUSES:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='METADATA_STATUS',
                location='capacity.metadata.status',
                message=f"Unknown status: '{status}'. Expected: {self.VALID_STATUSES}"
            ))

    def _validate_questions(self, questions: List[Dict], file_path: Path):
        """Validate questions array"""
        if not isinstance(questions, list):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='QUESTIONS',
                location='questions',
                message="questions must be a list"
            ))
            return

        if not questions:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='QUESTIONS',
                location='questions',
                message="No questions defined"
            ))
            return

        question_numbers = set()
        question_ids = set()

        for idx, question in enumerate(questions):
            loc = f"questions[{idx}]"

            # Check required fields
            missing_keys = self.REQUIRED_QUESTION_KEYS - set(question.keys())
            if missing_keys:
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='ERROR',
                    category='QUESTION',
                    location=loc,
                    message=f"Missing question fields: {', '.join(missing_keys)}"
                ))

            # Validate ID format
            q_id = question.get('id', '')
            if q_id:
                if not q_id.startswith('Q-'):
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='WARNING',
                        category='QUESTION_ID',
                        location=f"{loc}.id",
                        message=f"Question ID should start with 'Q-': {q_id}"
                    ))
                if q_id in question_ids:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='QUESTION_ID',
                        location=f"{loc}.id",
                        message=f"Duplicate question ID: {q_id}"
                    ))
                question_ids.add(q_id)

            # Check question number sequence
            q_num = question.get('question_number')
            if q_num is not None:
                if not isinstance(q_num, int):
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='QUESTION_NUMBER',
                        location=f"{loc}.question_number",
                        message=f"question_number must be an integer: {q_num}"
                    ))
                elif q_num in question_numbers:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='QUESTION_NUMBER',
                        location=f"{loc}.question_number",
                        message=f"Duplicate question number: {q_num}"
                    ))
                question_numbers.add(q_num)

            # Validate maturity levels
            self._validate_maturity_levels(
                question.get('maturity_levels', []),
                file_path,
                f"{loc}.maturity_levels"
            )

            # Validate artifacts, metrics, sampling_guidance are present
            for field in ['artifacts', 'metrics', 'sampling_guidance']:
                value = question.get(field)
                if value is None:
                    continue

                if field in ['artifacts', 'metrics']:
                    if not isinstance(value, list):
                        self.report.add_issue(ValidationIssue(
                            file_path=str(file_path),
                            severity='WARNING',
                            category='QUESTION_FIELD',
                            location=f"{loc}.{field}",
                            message=f"{field} should be a list"
                        ))
                    elif not value:
                        self.report.add_issue(ValidationIssue(
                            file_path=str(file_path),
                            severity='INFO',
                            category='QUESTION_FIELD',
                            location=f"{loc}.{field}",
                            message=f"{field} list is empty"
                        ))
                elif field == 'sampling_guidance':
                    if not isinstance(value, str):
                        self.report.add_issue(ValidationIssue(
                            file_path=str(file_path),
                            severity='WARNING',
                            category='QUESTION_FIELD',
                            location=f"{loc}.{field}",
                            message=f"{field} should be a string"
                        ))
                    elif not value.strip():
                        self.report.add_issue(ValidationIssue(
                            file_path=str(file_path),
                            severity='INFO',
                            category='QUESTION_FIELD',
                            location=f"{loc}.{field}",
                            message=f"{field} is empty"
                        ))

        # Check question number sequence
        if question_numbers:
            expected = set(range(1, len(questions) + 1))
            if question_numbers != expected:
                missing = expected - question_numbers
                extra = question_numbers - expected
                if missing:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='WARNING',
                        category='QUESTION_SEQUENCE',
                        location='questions',
                        message=f"Missing question numbers in sequence: {sorted(missing)}"
                    ))
                if extra:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='WARNING',
                        category='QUESTION_SEQUENCE',
                        location='questions',
                        message=f"Extra question numbers in sequence: {sorted(extra)}"
                    ))

    def _validate_maturity_levels(self, levels: List[Dict], file_path: Path, location: str):
        """Validate maturity levels"""
        if not isinstance(levels, list):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='MATURITY_LEVELS',
                location=location,
                message="maturity_levels must be a list"
            ))
            return

        # Should have 7 levels (0-6)
        if len(levels) != 7:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='WARNING',
                category='MATURITY_LEVELS',
                location=location,
                message=f"Expected 7 maturity levels (0-6), found {len(levels)}"
            ))

        level_numbers = set()

        for idx, level in enumerate(levels):
            loc = f"{location}[{idx}]"

            # Check required fields
            missing_keys = self.REQUIRED_MATURITY_LEVEL_KEYS - set(level.keys())
            if missing_keys:
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='ERROR',
                    category='MATURITY_LEVEL',
                    location=loc,
                    message=f"Missing maturity level fields: {', '.join(missing_keys)}"
                ))

            # Validate level number
            level_num = level.get('level')
            if level_num is not None:
                if not isinstance(level_num, int):
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='MATURITY_LEVEL_NUMBER',
                        location=f"{loc}.level",
                        message=f"level must be an integer: {level_num}"
                    ))
                elif level_num < 0 or level_num > 6:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='MATURITY_LEVEL_NUMBER',
                        location=f"{loc}.level",
                        message=f"level must be between 0 and 6: {level_num}"
                    ))
                elif level_num in level_numbers:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='MATURITY_LEVEL_NUMBER',
                        location=f"{loc}.level",
                        message=f"Duplicate level number: {level_num}"
                    ))
                level_numbers.add(level_num)

            # Validate label format
            label = level.get('label', '')
            if label and level_num is not None:
                expected_label = f"Nível {level_num}"
                if label != expected_label:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='WARNING',
                        category='MATURITY_LEVEL_LABEL',
                        location=f"{loc}.label",
                        message=f"Expected label '{expected_label}', found '{label}'"
                    ))

            # Check for empty descriptions
            description = level.get('description', '')
            if not description or not description.strip():
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='WARNING',
                    category='MATURITY_LEVEL_DESCRIPTION',
                    location=f"{loc}.description",
                    message=f"Level {level_num} has empty description"
                ))

            # Validate evidence_signals
            evidence = level.get('evidence_signals', {})
            if not isinstance(evidence, dict):
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='ERROR',
                    category='EVIDENCE_SIGNALS',
                    location=f"{loc}.evidence_signals",
                    message="evidence_signals must be a dictionary"
                ))
            else:
                missing_ev_keys = self.REQUIRED_EVIDENCE_SIGNALS_KEYS - set(evidence.keys())
                if missing_ev_keys:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='EVIDENCE_SIGNALS',
                        location=f"{loc}.evidence_signals",
                        message=f"Missing evidence_signals fields: {', '.join(missing_ev_keys)}"
                    ))

                behaviors = evidence.get('observable_behaviors', [])
                if not isinstance(behaviors, list):
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='ERROR',
                        category='OBSERVABLE_BEHAVIORS',
                        location=f"{loc}.evidence_signals.observable_behaviors",
                        message="observable_behaviors must be a list"
                    ))
                elif not behaviors:
                    self.report.add_issue(ValidationIssue(
                        file_path=str(file_path),
                        severity='WARNING',
                        category='OBSERVABLE_BEHAVIORS',
                        location=f"{loc}.evidence_signals.observable_behaviors",
                        message=f"Level {level_num} has no observable behaviors defined"
                    ))

        # Check level sequence
        if level_numbers:
            expected = set(range(len(levels)))
            if level_numbers != expected:
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='ERROR',
                    category='MATURITY_LEVEL_SEQUENCE',
                    location=location,
                    message=f"Maturity levels not in sequence. Found: {sorted(level_numbers)}"
                ))

    def _validate_references(self, references: List[Dict], file_path: Path):
        """Validate references section"""
        if not isinstance(references, list):
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='ERROR',
                category='REFERENCES',
                location='references',
                message="references must be a list"
            ))
            return

        if not references:
            self.report.add_issue(ValidationIssue(
                file_path=str(file_path),
                severity='INFO',
                category='REFERENCES',
                location='references',
                message="No references provided"
            ))
            return

        for idx, ref in enumerate(references):
            loc = f"references[{idx}]"

            if not isinstance(ref, dict):
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='ERROR',
                    category='REFERENCE',
                    location=loc,
                    message="Reference must be a dictionary"
                ))
                continue

            # Check required fields
            missing_keys = self.REQUIRED_REFERENCE_KEYS - set(ref.keys())
            if missing_keys:
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='ERROR',
                    category='REFERENCE',
                    location=loc,
                    message=f"Missing reference fields: {', '.join(missing_keys)}"
                ))

            # Check if URL is provided when citation contains a URL
            citation = ref.get('citation', '')
            url = ref.get('url', '')

            if 'Disponível em:' in citation and not url:
                self.report.add_issue(ValidationIssue(
                    file_path=str(file_path),
                    severity='INFO',
                    category='REFERENCE_URL',
                    location=loc,
                    message="Citation mentions URL but 'url' field is missing"
                ))

    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """Check if version follows semantic versioning pattern"""
        parts = version.split('.')
        return len(parts) >= 2 and all(p.isdigit() for p in parts[:2])

    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        """Check if date is in YYYY-MM-DD format"""
        try:
            parts = date_str.split('-')
            if len(parts) != 3:
                return False
            year, month, day = parts
            return (len(year) == 4 and year.isdigit() and
                    len(month) == 2 and month.isdigit() and
                    len(day) == 2 and day.isdigit() and
                    1 <= int(month) <= 12 and
                    1 <= int(day) <= 31)
        except:
            return False


def print_report(report: ValidationReport):
    """Print validation report to console"""
    print("\n" + "="*80)
    print("VALIDATION REPORT")
    print("="*80)

    print(f"\nFiles processed: {report.total_files}")
    print(f"Valid files: {report.valid_files}")
    print(f"Files with errors: {report.total_files - report.valid_files}")

    errors = report.get_errors()
    warnings = report.get_warnings()
    info = report.get_info()

    print(f"\nIssues found:")
    print(f"  - Errors: {len(errors)}")
    print(f"  - Warnings: {len(warnings)}")
    print(f"  - Info: {len(info)}")

    print(f"\nAuthors: {len(report.authors)}")
    for author in sorted(report.authors):
        print(f"  - {author}")

    print(f"\nFrameworks: {len(report.frameworks)}")
    for framework in sorted(report.frameworks):
        print(f"  - {framework}")

    # Group issues by category and severity
    if report.issues:
        print("\n" + "-"*80)
        print("ISSUES DETAILS")
        print("-"*80)

        # Group by severity
        for severity in ['ERROR', 'WARNING', 'INFO']:
            issues = [i for i in report.issues if i.severity == severity]
            if not issues:
                continue

            print(f"\n{severity}S ({len(issues)}):")
            print("-"*80)

            # Group by category
            by_category = defaultdict(list)
            for issue in issues:
                by_category[issue.category].append(issue)

            for category in sorted(by_category.keys()):
                cat_issues = by_category[category]
                print(f"\n  {category} ({len(cat_issues)}):")

                # Group by file
                by_file = defaultdict(list)
                for issue in cat_issues:
                    by_file[issue.file_path].append(issue)

                for file_path in sorted(by_file.keys()):
                    file_issues = by_file[file_path]
                    print(f"\n    {file_path}:")
                    for issue in file_issues:
                        location = f" [{issue.location}]" if issue.location else ""
                        print(f"      - {issue.message}{location}")

    print("\n" + "="*80)

    # Summary
    if not errors:
        print("✓ All files passed validation!")
    else:
        print(f"✗ Validation failed with {len(errors)} error(s)")

    print("="*80 + "\n")


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python json_consistency_check.py <data_directory>")
        print("\nExample:")
        print("  python json_consistency_check.py ./question-base/JSON7_20260105_164046/data")
        sys.exit(1)

    data_dir = Path(sys.argv[1])

    if not data_dir.exists():
        print(f"Error: Directory not found: {data_dir}")
        sys.exit(1)

    if not data_dir.is_dir():
        print(f"Error: Not a directory: {data_dir}")
        sys.exit(1)

    print(f"JSON Consistency Checker")
    print(f"Data directory: {data_dir.absolute()}\n")

    checker = JSONConsistencyChecker(data_dir)
    report = checker.validate_all_files()
    print_report(report)

    # Exit with error code if there are errors
    errors = report.get_errors()
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
