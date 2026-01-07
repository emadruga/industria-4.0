#!/usr/bin/env python3
"""
JSON Validation and Fix Tool for Industry 4.0 Question Base
Validates consistency between JSON files and the capacity catalog from Excel.

Author: Industry 4.0 Team
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import openpyxl
from collections import defaultdict


class CapacityCatalog:
    """Loads and manages the capacity catalog from Excel."""

    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)
        self.catalog = {}
        self.load_catalog()

    def load_catalog(self):
        """Load capacity catalog from Excel file."""
        print(f"Loading capacity catalog from: {self.excel_path}")

        wb = openpyxl.load_workbook(self.excel_path, data_only=True)
        ws = wb['Capacidades (acatech × SIRI)']

        # Skip first 2 rows (empty and header)
        for row in ws.iter_rows(min_row=3, values_only=True):
            # Columns: acatech_area, acatech_principle, capacity_en, capacity_pt,
            #          siri_block, siri_pilar, siri_dimension, siri_secondary

            if not row[3]:  # Skip if capacity_pt is empty
                continue

            capacity_pt = row[3].strip() if row[3] else None
            siri_block = row[4].strip() if row[4] else None
            siri_pilar = row[5].strip() if row[5] else None
            siri_dimension = row[6].strip() if row[6] else None

            if not (capacity_pt and siri_block and siri_pilar and siri_dimension):
                continue

            # Normalize block name
            block_normalized = self._normalize_block(siri_block)

            # Normalize pilar name
            pilar_normalized = self._normalize_pilar(siri_pilar)

            # Parse dimension to extract code and clean name, then normalize
            dimension_clean = self._clean_dimension_name(siri_dimension)
            dimension_normalized = self._normalize_dimension(dimension_clean)

            # Store in catalog using capacity name as key
            capacity_key = self._normalize_key(capacity_pt)

            if capacity_key not in self.catalog:
                self.catalog[capacity_key] = {
                    'name': capacity_pt,
                    'block': block_normalized,
                    'pilar': pilar_normalized,
                    'dimension': dimension_normalized,
                    'dimension_original': siri_dimension
                }

        print(f"✅ Loaded {len(self.catalog)} capacities from catalog")

        # Print some statistics
        blocks = set(entry['block'] for entry in self.catalog.values())
        pilares = set(entry['pilar'] for entry in self.catalog.values())
        dimensions = set(entry['dimension'] for entry in self.catalog.values())

        print(f"   - Blocks: {len(blocks)} ({', '.join(sorted(blocks))})")
        print(f"   - Pilares: {len(pilares)}")
        print(f"   - Dimensions: {len(dimensions)}")
        print()

    def _normalize_block(self, block: str) -> str:
        """Normalize block name from English to Portuguese."""
        mapping = {
            'Technology': 'Tecnologia',
            'Process': 'Processo',
            'Organization': 'Organização',
            'Tecnologia': 'Tecnologia',
            'Processo': 'Processo',
            'Organização': 'Organização',
            'Organizacao': 'Organização'
        }
        return mapping.get(block, block)

    def _normalize_pilar(self, pilar: str) -> str:
        """Normalize pilar name from English to Portuguese."""
        mapping = {
            # Technology pilares
            'Automation': 'Automação',
            'Connectivity': 'Conectividade',
            'Intelligence': 'Inteligência',
            # Process pilares
            'Operations': 'Operações',
            'Supply Chain': 'Cadeia de Suprimentos',
            'Product Lifecycle': 'Ciclo de Vida do Produto',
            # Organization pilares
            'Structure & Management': 'Estrutura e Gestão',
            'Talent Readiness': 'Prontidão de Talentos',
            # Keep Portuguese as-is
            'Automação': 'Automação',
            'Conectividade': 'Conectividade',
            'Inteligência': 'Inteligência',
            'Operações': 'Operações',
            'Cadeia de Suprimentos': 'Cadeia de Suprimentos',
            'Ciclo de Vida do Produto': 'Ciclo de Vida do Produto',
            'Estrutura e Gestão': 'Estrutura e Gestão',
            'Prontidão de Talentos': 'Prontidão de Talentos'
        }
        return mapping.get(pilar, pilar)

    def _normalize_dimension(self, dimension: str) -> str:
        """Normalize dimension name from English to Portuguese."""
        mapping = {
            # Technology dimensions
            'Shopfloor': 'Chão de Fábrica',
            'Enterprise': 'Empresa',
            'Facility': 'Instalações',
            # Process dimensions
            'Vertical': 'Vertical',
            'Horizontal': 'Horizontal',
            'Integrated Product Lifecycle': 'Ciclo de Vida Integrado do Produto',
            # Organization dimensions
            'Leadership Competency': 'Competência de Liderança',
            'Inter- and Intra-Company Collaboration': 'Colaboração Inter e Intra-Empresarial',
            'Strategy & Governance': 'Estratégia e Governança',
            'Workforce Learning & Development': 'Aprendizado e Desenvolvimento da Força de Trabalho',
            # Keep Portuguese as-is
            'Chão de Fábrica': 'Chão de Fábrica',
            'Empresa': 'Empresa',
            'Instalações': 'Instalações',
            'Vertical': 'Vertical',
            'Horizontal': 'Horizontal',
            'Ciclo de Vida Integrado do Produto': 'Ciclo de Vida Integrado do Produto',
            'Competência de Liderança': 'Competência de Liderança',
            'Colaboração Inter e Intra-Empresarial': 'Colaboração Inter e Intra-Empresarial',
            'Estratégia e Governança': 'Estratégia e Governança',
            'Aprendizado e Desenvolvimento da Força de Trabalho': 'Aprendizado e Desenvolvimento da Força de Trabalho'
        }
        return mapping.get(dimension, dimension)

    def _clean_dimension_name(self, dimension: str) -> str:
        """Clean dimension name by removing codes like (D4), (D10), etc."""
        if not dimension:
            return dimension

        import re
        # Remove patterns like (D4), (D10), etc.
        cleaned = re.sub(r'\s*\([Dd]\d+\)\s*', '', dimension)
        return cleaned.strip()

    def _normalize_key(self, name: str) -> str:
        """Normalize a name for dictionary lookup."""
        if not name:
            return ""
        # Convert to lowercase and remove extra whitespace
        return ' '.join(name.lower().split())

    def lookup_capacity(self, capacity_name: str) -> Optional[Dict]:
        """Lookup capacity in catalog by name."""
        key = self._normalize_key(capacity_name)
        return self.catalog.get(key)

    def get_all_capacities(self) -> List[Dict]:
        """Get all capacities from catalog."""
        return list(self.catalog.values())


class ValidationIssue:
    """Represents a validation issue found in a JSON file."""

    def __init__(self, file_path: str, issue_type: str, field: str,
                 current_value: str, expected_value: str, author: str = None,
                 what_to_do: str = None, severity: str = "error"):
        self.file_path = file_path
        self.issue_type = issue_type
        self.field = field
        self.current_value = current_value
        self.expected_value = expected_value
        self.author = author
        self.what_to_do = what_to_do
        self.severity = severity

    def __str__(self):
        symbol = "❌" if self.severity == "error" else "⚠️"
        author_info = f" (Author: {self.author})" if self.author else ""
        action_info = f"\n   Action: {self.what_to_do}" if self.what_to_do else ""
        return (f"{symbol} {self.issue_type} in {Path(self.file_path).name}{author_info}\n"
                f"   Field: {self.field}\n"
                f"   Current: '{self.current_value}'\n"
                f"   Expected: '{self.expected_value}'{action_info}")


class JSONValidator:
    """Validates JSON files against the capacity catalog."""

    def __init__(self, catalog: CapacityCatalog, fix_mode: bool = False):
        self.catalog = catalog
        self.fix_mode = fix_mode
        self.issues = []
        self.stats = {
            'total_files': 0,
            'valid_files': 0,
            'files_with_issues': 0,
            'total_issues': 0,
            'fixed_issues': 0
        }

    def validate_file(self, json_path: Path) -> List[ValidationIssue]:
        """Validate a single JSON file."""
        self.stats['total_files'] += 1
        file_issues = []

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            capacity = data.get('capacity', {})
            if not capacity:
                print(f"⚠️  Skipping {json_path.name}: No capacity field found")
                return file_issues

            # Get capacity info from JSON
            capacity_name = capacity.get('name', '')
            json_block = capacity.get('block', '')
            json_pilar = capacity.get('pilar', '')
            json_dimension = capacity.get('dimension', '')

            # Get author from metadata
            metadata = capacity.get('metadata', {})
            author = metadata.get('author', 'Unknown')

            # Check capacity description for formatting issues FIRST (before catalog check)
            # This ensures we validate descriptions even for capacities not in catalog
            capacity_desc = capacity.get('description', '').strip()
            if capacity_desc:
                # Check for English dimension names pattern: Capital letter + any text + (D##) within first 100 chars
                # Matches patterns like "Workforce Learning & Development (D13)" or "Leadership Competency (D14)"
                # Only check the first 100 characters to avoid false positives when (D##) appears in the description body
                import re
                desc_start = capacity_desc[:100]
                has_english_dimension = re.search(r'^[A-Z][^(]*\([Dd]\d+\)', desc_start)
                has_resumo_descritivo = 'resumo descritivo' in capacity_desc.lower()
                has_description_header = capacity_desc.lower().startswith('descrição da capacidade')

                if has_english_dimension or has_resumo_descritivo or has_description_header:
                    # Show first 100 chars of problematic description
                    preview = capacity_desc[:100] + '...' if len(capacity_desc) > 100 else capacity_desc

                    issue = ValidationIssue(
                        str(json_path),
                        "Capacity description issue",
                        "capacity.description",
                        preview,
                        "[Clean Portuguese description without headers/labels]",
                        author,
                        what_to_do=f"Remove English dimension names, 'Resumo Descritivo', and 'Descrição da Capacidade' headers"
                    )
                    file_issues.append(issue)

            # Lookup in catalog
            catalog_entry = self.catalog.lookup_capacity(capacity_name)

            if not catalog_entry:
                print(f"⚠️  Capacity '{capacity_name}' not found in catalog")
                print(f"    File:   {json_path.name}")
                print(f"    Path:   {json_path}")
                print(f"    Author: {author}")
                print()
                # Don't return early - continue to validate descriptions and question titles
                # return file_issues

            # Validate block/pilar/dimension only if capacity is in catalog
            if catalog_entry:
                block_mismatch = json_block != catalog_entry['block']
                pilar_mismatch = json_pilar != catalog_entry['pilar']
                dimension_mismatch = json_dimension != catalog_entry['dimension']

                if block_mismatch:
                    issue = ValidationIssue(
                        str(json_path),
                        "Block mismatch",
                        "capacity.block",
                        json_block,
                        catalog_entry['block'],
                        author
                    )
                    file_issues.append(issue)

                # Validate pilar
                if pilar_mismatch:
                    issue = ValidationIssue(
                        str(json_path),
                        "Pilar mismatch",
                        "capacity.pilar",
                        json_pilar,
                        catalog_entry['pilar'],
                        author
                    )
                    file_issues.append(issue)

                # Validate dimension
                if dimension_mismatch:
                    issue = ValidationIssue(
                        str(json_path),
                        "Dimension mismatch",
                        "capacity.dimension",
                        json_dimension,
                        catalog_entry['dimension'],
                        author
                    )
                    file_issues.append(issue)

            # Check for questions with "Tema" title
            questions = data.get('questions', [])
            for q in questions:
                q_title = q.get('title', '').strip()
                q_text = q.get('text', '').strip()
                q_id = q.get('id', 'N/A')
                q_number = q.get('question_number', 'N/A')

                if q_title.lower() == 'tema':
                    # Create a summary from the question text (first 60 chars)
                    suggested_title = q_text[:60] + '...' if len(q_text) > 60 else q_text

                    issue = ValidationIssue(
                        str(json_path),
                        "Question title issue",
                        f"questions[{q_number-1}].title",
                        "Tema",
                        f"[Meaningful title from question text]",
                        author,
                        what_to_do=f"Replace 'Tema' with summary of question text (Q{q_number}): \"{suggested_title}\""
                    )
                    file_issues.append(issue)

            # Determine what to do based on all issues for this file
            if file_issues:
                # Check if we have hierarchy issues that need the action
                hierarchy_issues = [i for i in file_issues if i.issue_type in
                                   ["Block mismatch", "Pilar mismatch", "Dimension mismatch"]]

                if hierarchy_issues:
                    what_to_do = self._determine_action(
                        json_path,
                        block_mismatch,
                        pilar_mismatch,
                        dimension_mismatch,
                        catalog_entry
                    )
                    # Add what_to_do to hierarchy issues only (question title issues have their own what_to_do)
                    for issue in hierarchy_issues:
                        if not issue.what_to_do:
                            issue.what_to_do = what_to_do

            # Update stats
            if file_issues:
                self.stats['files_with_issues'] += 1
                self.stats['total_issues'] += len(file_issues)

                # Fix if in fix mode
                if self.fix_mode:
                    self.fix_file(json_path, data, file_issues, catalog_entry)
            else:
                self.stats['valid_files'] += 1

            return file_issues

        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {json_path.name}: {e}")
            return file_issues
        except Exception as e:
            print(f"❌ Error processing {json_path.name}: {e}")
            return file_issues

    def _determine_action(self, json_path: Path, block_mismatch: bool,
                         pilar_mismatch: bool, dimension_mismatch: bool,
                         catalog_entry: Dict) -> str:
        """Determine what action needs to be taken to fix the issues."""
        actions = []

        # Check if file needs to be moved
        needs_move = block_mismatch or pilar_mismatch or dimension_mismatch

        if needs_move:
            # Calculate expected path
            block = catalog_entry['block'].replace(' ', '_')
            pilar = catalog_entry['pilar'].replace(' ', '_')
            dimension = catalog_entry['dimension'].replace(' ', '_')

            expected_dir = f"data/{block}/{pilar}/{dimension}"
            current_parent = json_path.parent

            actions.append(f"Rename fields in JSON")

            # Check if the current directory matches expected directory
            # We need to check if any part of the hierarchy changed
            if block_mismatch or pilar_mismatch or dimension_mismatch:
                actions.append(f"Move file to: {expected_dir}/")

        return " + ".join(actions) if actions else "Update JSON fields"

    def fix_file(self, json_path: Path, data: Dict, issues: List[ValidationIssue],
                 catalog_entry: Dict):
        """Fix issues in a JSON file and move if needed."""
        import re

        modified = False
        needs_move = False
        fixed_count = 0

        for issue in issues:
            # Fix hierarchy issues
            if issue.field == "capacity.block":
                data['capacity']['block'] = catalog_entry['block']
                modified = True
                needs_move = True
                fixed_count += 1
            elif issue.field == "capacity.pilar":
                data['capacity']['pilar'] = catalog_entry['pilar']
                modified = True
                needs_move = True
                fixed_count += 1
            elif issue.field == "capacity.dimension":
                data['capacity']['dimension'] = catalog_entry['dimension']
                modified = True
                needs_move = True
                fixed_count += 1

            # Fix capacity description issues
            elif issue.field == "capacity.description":
                desc = data['capacity']['description']
                capacity_name = data['capacity'].get('name', '')

                # Pattern: "Dimension Name Resumo Descritivo Capacity Name actual description..."
                # We want to keep only the "actual description" part

                # Step 1: Remove "Descrição da Capacidade" header if present
                if desc.lower().startswith('descrição da capacidade'):
                    desc = re.sub(r'^descrição da capacidade\s*', '', desc, flags=re.IGNORECASE)

                # Step 2: Remove English dimension names with codes like "Leadership Competency (D14)" or "Workforce Learning & Development (D13)"
                # Pattern matches: Capital letter + any text (including &) + (D##)
                desc = re.sub(r'^[A-Z][^(]*\([Dd]\d+\)\s*', '', desc)

                # Step 3: Remove dimension name at the beginning (Portuguese)
                # Pattern: dimension name followed by "Resumo Descritivo"
                desc = re.sub(r'^[^\.]+?\s+resumo descritivo\s+', '', desc, flags=re.IGNORECASE)

                # Step 4: If capacity name appears at start (after previous removals), remove it
                # This handles cases where capacity name is repeated after "Resumo Descritivo"
                if capacity_name:
                    # Escape special regex characters in capacity name
                    escaped_name = re.escape(capacity_name)
                    # Remove capacity name if it appears at the beginning
                    desc = re.sub(r'^' + escaped_name + r'\s+', '', desc, flags=re.IGNORECASE)

                # Step 5: Clean up any remaining "Resumo Descritivo" fragments
                desc = re.sub(r'resumo descritivo\s*', '', desc, flags=re.IGNORECASE)

                # Step 6: Clean up extra whitespace
                desc = ' '.join(desc.split()).strip()

                # Step 7: Capitalize first letter if needed
                if desc and desc[0].islower():
                    desc = desc[0].upper() + desc[1:]

                data['capacity']['description'] = desc
                modified = True
                fixed_count += 1

            # Fix question title issues
            elif issue.field.startswith("questions[") and issue.field.endswith("].title"):
                # Extract question index from field like "questions[0].title"
                match = re.match(r'questions\[(\d+)\]\.title', issue.field)
                if match:
                    q_idx = int(match.group(1))
                    questions = data.get('questions', [])
                    if q_idx < len(questions):
                        q_text = questions[q_idx].get('text', '').strip()
                        # Create a meaningful title from question text (first 60 chars)
                        if q_text:
                            new_title = q_text[:60].strip()
                            # Remove trailing punctuation if cut mid-sentence
                            if len(q_text) > 60:
                                new_title = new_title.rstrip('.,;:?!')

                            questions[q_idx]['title'] = new_title
                            modified = True
                            fixed_count += 1
                        else:
                            # Question has empty text - can't auto-fix, skip
                            print(f"⚠️  Cannot auto-fix question {q_idx+1} in {json_path.name}: empty question text")

        # Save the modified JSON file
        if modified:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.stats['fixed_issues'] += fixed_count

            # Move file if hierarchy changed
            if needs_move:
                self._move_file(json_path, catalog_entry)
                print(f"✅ Fixed {fixed_count} issue(s) and moved {json_path.name}")
            else:
                print(f"✅ Fixed {fixed_count} issue(s) in {json_path.name}")

    def _move_file(self, json_path: Path, catalog_entry: Dict):
        """Move file to correct directory based on hierarchy."""
        # Calculate new path
        block = catalog_entry['block'].replace(' ', '_')
        pilar = catalog_entry['pilar'].replace(' ', '_')
        dimension = catalog_entry['dimension'].replace(' ', '_')

        # Get the base data directory from current path
        # Assuming structure: .../data/Block/Pilar/Dimension/file.json
        parts = json_path.parts
        if 'data' in parts:
            data_idx = parts.index('data')
            base_dir = Path(*parts[:data_idx+1])
        else:
            # Fallback: use parent's parent's parent
            base_dir = json_path.parent.parent.parent.parent / 'data'

        new_dir = base_dir / block / pilar / dimension
        new_path = new_dir / json_path.name

        # Create directory if it doesn't exist
        new_dir.mkdir(parents=True, exist_ok=True)

        # Move the file
        import shutil
        shutil.move(str(json_path), str(new_path))

        # Try to remove empty directories (optional cleanup)
        try:
            old_dir = json_path.parent
            if old_dir.exists() and not any(old_dir.iterdir()):
                old_dir.rmdir()
                # Try parent too
                old_parent = old_dir.parent
                if old_parent.exists() and not any(old_parent.iterdir()):
                    old_parent.rmdir()
        except:
            pass  # Ignore errors in cleanup

    def validate_directory(self, base_dir: Path, pattern: str = "**/*.json") -> List[ValidationIssue]:
        """Validate all JSON files in a directory."""
        json_files = sorted(base_dir.glob(pattern))

        if not json_files:
            print(f"No JSON files found in {base_dir}")
            return []

        print(f"Found {len(json_files)} JSON files to validate")
        print("="*60)
        print()

        for json_file in json_files:
            issues = self.validate_file(json_file)
            if issues:
                self.issues.extend(issues)

        return self.issues

    def print_issues_by_category(self):
        """Print issues organized by category."""
        if not self.issues:
            return

        # Organize issues by type
        issues_by_type = defaultdict(list)
        for issue in self.issues:
            issues_by_type[issue.issue_type].append(issue)

        print("\n" + "="*60)
        print("ISSUES BY CATEGORY")
        print("="*60)

        # Print each category
        for issue_type in sorted(issues_by_type.keys()):
            issues = issues_by_type[issue_type]
            print(f"\n{issue_type.upper()} ({len(issues)} issues)")
            print("-" * 60)

            for issue in issues:
                file_name = Path(issue.file_path).name
                author_str = f" [Author: {issue.author}]" if issue.author else ""
                print(f"  • {file_name}{author_str}")
                print(f"    Path:     {issue.file_path}")
                print(f"    Current:  '{issue.current_value}'")
                print(f"    Expected: '{issue.expected_value}'")
                if issue.what_to_do:
                    print(f"    Action:   {issue.what_to_do}")
                print()

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Total files validated: {self.stats['total_files']}")
        print(f"Valid files: {self.stats['valid_files']} ✅")
        print(f"Files with issues: {self.stats['files_with_issues']} ⚠️")
        print(f"Total issues found: {self.stats['total_issues']}")

        if self.fix_mode:
            print(f"Issues fixed: {self.stats['fixed_issues']} ✅")

        if self.stats['total_issues'] > 0 and not self.fix_mode:
            print("\n💡 Run with --fix flag to automatically fix these issues")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Validate and fix Industry 4.0 JSON question files against capacity catalog'
    )
    parser.add_argument('json_dir', help='Directory containing JSON files to validate')
    parser.add_argument('-e', '--excel',
                        default='mdic-suframa/templates/acatech_siri_comparacao.xlsx',
                        help='Path to Excel catalog file')
    parser.add_argument('-p', '--pattern', default='**/*.json',
                        help='File pattern (default: **/*.json)')
    parser.add_argument('--fix', action='store_true',
                        help='Automatically fix issues found')

    args = parser.parse_args()

    # Resolve paths
    json_dir = Path(args.json_dir)
    if not json_dir.exists():
        print(f"❌ Error: Directory not found: {json_dir}")
        sys.exit(1)

    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(f"❌ Error: Excel file not found: {excel_path}")
        sys.exit(1)

    # Load catalog
    print("="*60)
    print("JSON VALIDATION TOOL")
    print("="*60)
    print()

    catalog = CapacityCatalog(str(excel_path))

    # Validate files
    validator = JSONValidator(catalog, fix_mode=args.fix)

    if args.fix:
        print("🔧 FIX MODE ENABLED - Issues will be automatically corrected")
        print()

    issues = validator.validate_directory(json_dir, pattern=args.pattern)

    # Print issues by category
    if issues and not args.fix:
        validator.print_issues_by_category()

    # Print summary
    validator.print_summary()

    # Exit with error code if issues found (and not fixed)
    if issues and not args.fix:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
