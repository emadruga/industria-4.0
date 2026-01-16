#!/usr/bin/env python3
"""
JSON Coverage Validation Script
Cross-references ACATECH capacities from Excel template against JSON7 catalog
"""

import pandas as pd
import json
from pathlib import Path
import sys

def normalize_name(name):
    """Normalize capacity names for comparison"""
    if not name or pd.isna(name):
        return ""
    # Convert to lowercase, remove accents, normalize spaces
    normalized = str(name).lower().strip()
    # Remove special characters but keep spaces
    normalized = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in normalized)
    # Collapse multiple spaces
    normalized = ' '.join(normalized.split())
    return normalized

def read_excel_capacities(excel_path):
    """Read capacities from ACATECH Excel file"""
    try:
        # Read the Excel file with proper header row
        df = pd.read_excel(excel_path, sheet_name='Capacidades (acatech × SIRI)', header=1)

        capacities = []
        for idx, row in df.iterrows():
            # Skip empty rows
            dimension = row.get('Área estrutural (acatech)')
            capacity_pt = row.get('Capacidade (português)')
            responsible = row.get('Responsável')

            if pd.isna(capacity_pt) or str(capacity_pt).strip() == '':
                continue

            capacity_data = {
                'row': idx + 3,  # Excel row (1-indexed, +2 for empty first row and header)
                'dimension': str(dimension).strip() if not pd.isna(dimension) else '',
                'capacity': str(capacity_pt).strip(),
                'responsible': str(responsible).strip() if not pd.isna(responsible) else '',
                'normalized_capacity': normalize_name(capacity_pt)
            }
            capacities.append(capacity_data)

        return capacities
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def scan_json_catalog(data_dir):
    """Scan all JSON files in the catalog and extract capacity information"""
    json_files = {}
    data_path = Path(data_dir)

    for json_file in data_path.rglob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract capacity name and author
            capacity_name = data.get('capacity', {}).get('name', '')
            author = data.get('capacity', {}).get('metadata', {}).get('author', '')

            if capacity_name:
                # Store both the file path and normalized name
                relative_path = json_file.relative_to(data_path.parent)
                normalized = normalize_name(capacity_name)

                json_files[normalized] = {
                    'path': str(relative_path),
                    'author': author,
                    'original_name': capacity_name
                }
        except Exception as e:
            print(f"Warning: Could not parse {json_file}: {e}")
            continue

    return json_files

def cross_reference(excel_capacities, json_catalog):
    """Cross-reference Excel capacities against JSON catalog"""
    results = []

    for capacity in excel_capacities:
        normalized = capacity['normalized_capacity']

        # Check if capacity exists in JSON catalog
        if normalized in json_catalog:
            json_info = json_catalog[normalized]
            results.append({
                'Dimension in ACATECH Sheet': capacity['dimension'],
                'Capacity in ACATECH': capacity['capacity'],
                'Capacity Responsible in ACATECH': capacity['responsible'],
                'Row in ACATECH Sheet': capacity['row'],
                'Corresponding JSON File Exists?': 'Yes',
                'JSON File Path': json_info['path'],
                'Author Inside JSON File': json_info['author']
            })
        else:
            results.append({
                'Dimension in ACATECH Sheet': capacity['dimension'],
                'Capacity in ACATECH': capacity['capacity'],
                'Capacity Responsible in ACATECH': capacity['responsible'],
                'Row in ACATECH Sheet': capacity['row'],
                'Corresponding JSON File Exists?': 'No',
                'JSON File Path': '',
                'Author Inside JSON File': ''
            })

    return results

def main():
    # Define paths
    excel_path = Path('/Users/emadruga/proj/industria-4.0/mdic-suframa/templates/acatech_siri_comparacao_v2.xlsx')
    data_dir = Path('/Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/data')
    output_path = Path('/Users/emadruga/proj/industria-4.0/question-base/docs/json_coverage_validation.xlsx')

    print("JSON Coverage Validation")
    print("=" * 80)
    print(f"Excel template: {excel_path}")
    print(f"JSON catalog: {data_dir}")
    print()

    # Read Excel capacities
    print("Reading ACATECH capacities from Excel...")
    excel_capacities = read_excel_capacities(excel_path)
    print(f"Found {len(excel_capacities)} capacities in ACATECH sheet")
    print()

    # Scan JSON catalog
    print("Scanning JSON catalog...")
    json_catalog = scan_json_catalog(data_dir)
    print(f"Found {len(json_catalog)} JSON capacity files")
    print()

    # Cross-reference
    print("Cross-referencing capacities...")
    results = cross_reference(excel_capacities, json_catalog)

    # Create DataFrame
    df = pd.DataFrame(results)

    # Calculate statistics
    total = len(df)
    found = len(df[df['Corresponding JSON File Exists?'] == 'Yes'])
    missing = total - found
    coverage_pct = (found / total * 100) if total > 0 else 0

    # Save to Excel
    df.to_excel(output_path, index=False, sheet_name='Coverage Validation')

    # Print summary
    print("=" * 80)
    print("COVERAGE VALIDATION REPORT")
    print("=" * 80)
    print()
    print(f"Total ACATECH capacities: {total}")
    print(f"Found in JSON catalog: {found} ({coverage_pct:.1f}%)")
    print(f"Missing from JSON catalog: {missing}")
    print()

    if missing > 0:
        print("Missing capacities:")
        missing_df = df[df['Corresponding JSON File Exists?'] == 'No']
        for _, row in missing_df.iterrows():
            print(f"  - Row {row['Row in ACATECH Sheet']}: {row['Capacity in ACATECH']} (Dimension: {row['Dimension in ACATECH Sheet']})")
        print()

    print(f"Report saved to: {output_path}")
    print("=" * 80)

if __name__ == '__main__':
    main()
