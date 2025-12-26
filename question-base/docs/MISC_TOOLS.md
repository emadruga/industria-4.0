# Miscellaneous Tools - Industry 4.0 Question Base

This document describes additional utility scripts that are not part of the main workflow but may be useful for specific tasks.

## Location

All miscellaneous tools are located in: `/Users/emadruga/proj/industria-4.0/question-base/scripts/tools/`

---

## Available Tools

### 1. Compare DOCX Files from Different Sources

**Script**: `compare_docx_files_from_diff_sources.py`

**Purpose**: Compare DOCX files between two directories using MD5 hashing to identify duplicates, missing files, and unique content.

**Usage**:
```bash
python compare_docx_files_from_diff_sources.py
```

**What it does**:
- Scans `mdic-suframa/templates` and `docs_by_author` directories
- Computes MD5 hash for each DOCX file
- Identifies:
  - Files only in templates directory
  - Files only in docs_by_author directory
  - Files present in both (duplicates)
  - Duplicate files within each directory
- Generates `comparison_report.json`

**Output**:
- Console report with categorized files
- `comparison_report.json` with detailed information

**Use case**: Before batch conversion, identify which DOCX files are missing or duplicated across source directories.

---

### 2. Accept Tracked Changes in DOCX

**Script**: `accept_tracked_changes.py`

**Purpose**: Programmatically accept all tracked changes and remove comments from DOCX files using XML manipulation.

**Usage**:
```bash
# Single file
python accept_tracked_changes.py /path/to/file.docx

# Directory (all DOCX files)
python accept_tracked_changes.py /path/to/directory

# Pattern matching
python accept_tracked_changes.py /path/to/directory -p "Organizacao*.docx"
```

**What it does**:
- Extracts DOCX as ZIP
- Processes document.xml to accept insertions/deletions
- Removes comment XML files
- Repacks as DOCX
- Creates `.backup` files before modification

**Use case**: When DOCX files have tracked changes that prevent proper field extraction by `docx_to_json_converter.py`.

**Note**: This tool works at the XML level. For more complex scenarios with review comments in table cells, use the DOC conversion method instead.

---

### 3. Flatten DOCX via DOC Format Conversion

**Script**: `flatten_one_docx.sh`

**Purpose**: Flatten tracked changes by converting DOCX → DOC → DOCX using Microsoft Word via AppleScript.

**Usage**:
```bash
./flatten_one_docx.sh /path/to/file.docx
```

**What it does**:
- Opens file in Microsoft Word
- Saves as .doc (Word 97-2004 format) - this forces all edits to become permanent
- Reopens the .doc file
- Saves back as .docx
- Deletes temporary .doc file

**Requirements**:
- Microsoft Word for Mac must be installed
- File must be closed in Word before running

**Use case**: When `accept_tracked_changes.py` doesn't work because changes are in table cells or comments contain the actual content.

**Success indicator**: After conversion, `python-docx` can read all field values that were previously showing as empty.

---

### 4. Regenerate Hierarchy Table

**Script**: `regenerate_hierarchy_table.py`

**Purpose**: Regenerate `hierarchy.json` and `hierarchy_table.md` from JSON files (legacy tool, mostly replaced by `rebuild_hierarchy.py`).

**Usage**:
```bash
python regenerate_hierarchy_table.py /path/to/JSON_folder
```

**What it does**:
- Scans all JSON files in the data directory
- Builds hierarchy structure
- Generates hierarchy.json and hierarchy_table.md

**Note**: This script has a hardcoded output path issue. Use `rebuild_hierarchy.py` instead for the main workflow.

**Use case**: Historical/legacy tool. Prefer `rebuild_hierarchy.py` which has better path handling.

---

### 5. Validate Questions (Schema Validation)

**Script**: `validate_questions.py`

**Purpose**: Validate JSON files against the JSON schema (structural validation only, not catalog validation).

**Usage**:
```bash
python validate_questions.py /path/to/question.json
```

**What it does**:
- Loads JSON schema from `schema/question_schema.json`
- Validates JSON structure
- Reports schema violations

**Use case**: Quick structural validation during development. For full validation including catalog consistency, use `json_validate.py` instead.

---

### 6. Extraction Modules

**Scripts**:
- `extract_evidence.py`
- `extract_glossary.py`
- `extract_references.py`

**Purpose**: Standalone modules for extracting specific components from DOCX files. These are imported by `docx_to_json_converter.py`.

**Usage**: Not meant to be run directly. These are library modules.

**Use case**:
- Development and testing of extraction logic
- Can be imported in custom scripts if needed

---

## Moving Tools to the tools/ Folder

To organize the scripts folder, move the miscellaneous tools:

```bash
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

# Move miscellaneous tools
mv compare_docx_files_from_diff_sources.py tools/
mv accept_tracked_changes.py tools/
mv flatten_one_docx.sh tools/
mv regenerate_hierarchy_table.py tools/
mv validate_questions.py tools/

# Keep extraction modules in main scripts/ (they're libraries)
# Keep in main scripts/:
#   - batch_convert.py
#   - docx_to_json_converter.py
#   - json_validate.py
#   - rebuild_hierarchy.py
#   - generate_index_html.py
#   - extract_*.py (library modules)
```

---

## Summary

**Main Workflow Scripts** (stay in `scripts/`):
1. `batch_convert.py` - Convert DOCX to JSON
2. `json_validate.py` - Validate and fix JSON files
3. `rebuild_hierarchy.py` - Rebuild hierarchy after validation
4. `generate_index_html.py` - Generate HTML visualization
5. `docx_to_json_converter.py` - Core converter (used by batch_convert)
6. `extract_*.py` - Extraction modules (libraries)

**Miscellaneous Tools** (move to `scripts/tools/`):
1. `compare_docx_files_from_diff_sources.py`
2. `accept_tracked_changes.py`
3. `flatten_one_docx.sh`
4. `regenerate_hierarchy_table.py`
5. `validate_questions.py`

---

**Last Updated**: 2025-12-26
**Version**: 1.0
