#!/usr/bin/env python3
"""
Compare DOCX files from two directories using MD5 hashing.

This script helps identify which DOCX files are unique to each directory
and which files are duplicates (same content, possibly different names).

Usage:
    python compare_docx_files_from_diff_sources.py

The script compares:
    - Source 1: /Users/emadruga/proj/industria-4.0/mdic-suframa/templates
    - Source 2: /Users/emadruga/proj/industria-4.0/question-base/docs_by_author
"""

import hashlib
import os
from pathlib import Path
from collections import defaultdict
import json


def compute_md5(file_path):
    """
    Compute MD5 hash of a file.

    Args:
        file_path: Path to the file

    Returns:
        MD5 hash as hexadecimal string
    """
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception as e:
        print(f"Error computing MD5 for {file_path}: {e}")
        return None


def find_docx_files(root_dir):
    """
    Recursively find all DOCX files in a directory.

    Args:
        root_dir: Root directory to search

    Returns:
        Dictionary mapping file paths to their MD5 hashes
    """
    root_path = Path(root_dir)
    docx_files = {}

    if not root_path.exists():
        print(f"Warning: Directory does not exist: {root_dir}")
        return docx_files

    # Find all .docx files recursively
    for docx_file in root_path.rglob('*.docx'):
        # Skip temporary files (starting with ~$)
        if docx_file.name.startswith('~$'):
            continue

        md5_hash = compute_md5(docx_file)
        if md5_hash:
            # Store relative path from root for easier comparison
            rel_path = docx_file.relative_to(root_path)
            docx_files[str(docx_file)] = {
                'md5': md5_hash,
                'relative_path': str(rel_path),
                'filename': docx_file.name,
                'size': docx_file.stat().st_size
            }

    return docx_files


def compare_directories(dir1, dir2):
    """
    Compare DOCX files in two directories.

    Args:
        dir1: First directory path
        dir2: Second directory path

    Returns:
        Dictionary with comparison results
    """
    print(f"Scanning directory 1: {dir1}")
    files1 = find_docx_files(dir1)
    print(f"Found {len(files1)} DOCX files in directory 1\n")

    print(f"Scanning directory 2: {dir2}")
    files2 = find_docx_files(dir2)
    print(f"Found {len(files2)} DOCX files in directory 2\n")

    # Create hash to files mapping
    hash_to_files1 = defaultdict(list)
    hash_to_files2 = defaultdict(list)

    for path, info in files1.items():
        hash_to_files1[info['md5']].append({'path': path, **info})

    for path, info in files2.items():
        hash_to_files2[info['md5']].append({'path': path, **info})

    # Get all unique hashes
    all_hashes = set(hash_to_files1.keys()) | set(hash_to_files2.keys())

    # Categorize files
    only_in_dir1 = []  # Files only in directory 1
    only_in_dir2 = []  # Files only in directory 2
    in_both = []       # Files in both directories (same content)
    duplicates_dir1 = []  # Duplicate files within directory 1
    duplicates_dir2 = []  # Duplicate files within directory 2

    for hash_val in all_hashes:
        files_in_1 = hash_to_files1.get(hash_val, [])
        files_in_2 = hash_to_files2.get(hash_val, [])

        if files_in_1 and files_in_2:
            # File exists in both directories
            in_both.append({
                'md5': hash_val,
                'dir1_files': files_in_1,
                'dir2_files': files_in_2
            })
        elif files_in_1:
            # File only in directory 1
            only_in_dir1.append({
                'md5': hash_val,
                'files': files_in_1
            })
        else:
            # File only in directory 2
            only_in_dir2.append({
                'md5': hash_val,
                'files': files_in_2
            })

        # Check for duplicates within each directory
        if len(files_in_1) > 1:
            duplicates_dir1.append({
                'md5': hash_val,
                'files': files_in_1
            })

        if len(files_in_2) > 1:
            duplicates_dir2.append({
                'md5': hash_val,
                'files': files_in_2
            })

    return {
        'dir1_path': dir1,
        'dir2_path': dir2,
        'dir1_total': len(files1),
        'dir2_total': len(files2),
        'only_in_dir1': only_in_dir1,
        'only_in_dir2': only_in_dir2,
        'in_both': in_both,
        'duplicates_dir1': duplicates_dir1,
        'duplicates_dir2': duplicates_dir2
    }


def print_results(results):
    """Print comparison results in a readable format."""

    print("=" * 80)
    print("DOCX FILES COMPARISON REPORT")
    print("=" * 80)
    print()

    print(f"Directory 1: {results['dir1_path']}")
    print(f"  Total DOCX files: {results['dir1_total']}")
    print()

    print(f"Directory 2: {results['dir2_path']}")
    print(f"  Total DOCX files: {results['dir2_total']}")
    print()

    print("=" * 80)
    print(f"SUMMARY")
    print("=" * 80)
    print(f"Files only in Directory 1: {len(results['only_in_dir1'])}")
    print(f"Files only in Directory 2: {len(results['only_in_dir2'])}")
    print(f"Files in both directories: {len(results['in_both'])}")
    print(f"Duplicates within Directory 1: {len(results['duplicates_dir1'])}")
    print(f"Duplicates within Directory 2: {len(results['duplicates_dir2'])}")
    print()

    # Files only in Directory 1 (templates)
    if results['only_in_dir1']:
        print("=" * 80)
        print(f"FILES ONLY IN DIRECTORY 1 ({len(results['only_in_dir1'])} unique files)")
        print("=" * 80)
        for i, item in enumerate(results['only_in_dir1'], 1):
            print(f"\n{i}. MD5: {item['md5']}")
            for file_info in item['files']:
                print(f"   - {file_info['relative_path']}")
                print(f"     Size: {file_info['size']:,} bytes")

    # Files only in Directory 2 (docs_by_author)
    if results['only_in_dir2']:
        print()
        print("=" * 80)
        print(f"FILES ONLY IN DIRECTORY 2 ({len(results['only_in_dir2'])} unique files)")
        print("=" * 80)
        for i, item in enumerate(results['only_in_dir2'], 1):
            print(f"\n{i}. MD5: {item['md5']}")
            for file_info in item['files']:
                print(f"   - {file_info['relative_path']}")
                print(f"     Size: {file_info['size']:,} bytes")

    # Files in both directories
    if results['in_both']:
        print()
        print("=" * 80)
        print(f"FILES IN BOTH DIRECTORIES ({len(results['in_both'])} unique files)")
        print("=" * 80)
        for i, item in enumerate(results['in_both'], 1):
            print(f"\n{i}. MD5: {item['md5']}")
            print(f"   Directory 1:")
            for file_info in item['dir1_files']:
                print(f"     - {file_info['relative_path']}")
            print(f"   Directory 2:")
            for file_info in item['dir2_files']:
                print(f"     - {file_info['relative_path']}")

    # Duplicates within Directory 1
    if results['duplicates_dir1']:
        print()
        print("=" * 80)
        print(f"DUPLICATES WITHIN DIRECTORY 1 ({len(results['duplicates_dir1'])} sets)")
        print("=" * 80)
        for i, item in enumerate(results['duplicates_dir1'], 1):
            print(f"\n{i}. MD5: {item['md5']}")
            for file_info in item['files']:
                print(f"   - {file_info['relative_path']}")

    # Duplicates within Directory 2
    if results['duplicates_dir2']:
        print()
        print("=" * 80)
        print(f"DUPLICATES WITHIN DIRECTORY 2 ({len(results['duplicates_dir2'])} sets)")
        print("=" * 80)
        for i, item in enumerate(results['duplicates_dir2'], 1):
            print(f"\n{i}. MD5: {item['md5']}")
            for file_info in item['files']:
                print(f"   - {file_info['relative_path']}")

    print()
    print("=" * 80)
    print("ACTIONABLE INSIGHTS")
    print("=" * 80)

    missing_count = len(results['only_in_dir1'])
    if missing_count > 0:
        print(f"\n⚠️  {missing_count} files from Directory 1 are missing in Directory 2")
        print(f"   These files should be converted to JSON to get all {missing_count + len(results['in_both'])} capacities")
    else:
        print("\n✅ All files from Directory 1 exist in Directory 2")

    if results['duplicates_dir1']:
        print(f"\n⚠️  {len(results['duplicates_dir1'])} duplicate file sets found in Directory 1")
        print("   Consider removing duplicates to avoid confusion")

    if results['duplicates_dir2']:
        print(f"\n⚠️  {len(results['duplicates_dir2'])} duplicate file sets found in Directory 2")
        print("   Consider removing duplicates to avoid confusion")

    print()


def save_json_report(results, output_file='comparison_report.json'):
    """Save comparison results to a JSON file."""
    output_path = Path(__file__).parent / output_file

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Detailed JSON report saved to: {output_path}")


def main():
    """Main function."""
    # Define directories
    dir1 = "/Users/emadruga/proj/industria-4.0/mdic-suframa/templates"
    dir2 = "/Users/emadruga/proj/industria-4.0/question-base/docs_by_author"

    # Compare directories
    results = compare_directories(dir1, dir2)

    # Print results
    print_results(results)

    # Save JSON report
    save_json_report(results)


if __name__ == "__main__":
    main()
