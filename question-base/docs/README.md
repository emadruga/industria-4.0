# Documentation - Industry 4.0 Question Base

This folder contains all documentation for the Industry 4.0 Question Base project.

## 📚 Documentation Structure

### Main Documentation

- **[BASIC_WORKFLOW.md](BASIC_WORKFLOW.md)** - Complete workflow to build a validated JSON question base
  - Step-by-step instructions
  - All commands needed
  - Expected outputs
  - **START HERE** for production use

- **[MISC_TOOLS.md](MISC_TOOLS.md)** - Miscellaneous utility scripts
  - Tools not in the main workflow
  - Located in `scripts/tools/`
  - Use cases and examples

- **[EXAMPLE_USAGE.md](EXAMPLE_USAGE.md)** - Usage examples (to be updated)
  - Practical examples
  - Common scenarios

### Technical Documentation

- **[README_HTML_GENERATOR.md](README_HTML_GENERATOR.md)** - HTML visualization generator
  - How the HTML generator works
  - Customization options

- **[README_MODULES.md](README_MODULES.md)** - Extraction modules
  - `extract_evidence.py`
  - `extract_glossary.py`
  - `extract_references.py`
  - Standalone usage and testing

### Historical Documentation

The `old/` subfolder contains historical/deprecated documentation for reference:
- QUICK_START.md (replaced by BASIC_WORKFLOW.md)
- COMPARISON_REPORT.md
- CONVERSION_LOG.md
- FIRST_JSON_SUCCESS.md
- FIXED_COMPLETE.md
- IMPROVEMENTS_REPORT.md
- MANUAL_FIXES_AUDIT.md
- MODULE_INTEGRATION_COMPLETE.md

---

## 🚀 Quick Start

**New users**: Read [BASIC_WORKFLOW.md](BASIC_WORKFLOW.md) to get started.

**To build a new JSON question base**:

```bash
# Activate environment
conda activate INDUSTRIA4

# Navigate to scripts
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

# Create timestamped output
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="../JSON_${TIMESTAMP}"

# Run complete workflow
python batch_convert.py ../docs_by_author -o "$OUTPUT_DIR"
python json_validate.py "${OUTPUT_DIR}/data" -e ../mdic-suframa/templates/acatech_siri_comparacao.xlsx --fix
python rebuild_hierarchy.py "$OUTPUT_DIR"
python generate_index_html.py "${OUTPUT_DIR}/metadata/hierarchy_table.md"

# View results
open "${OUTPUT_DIR}/metadata/index.html"
```

---

## 📁 Project Structure

```
question-base/
├── docs/                          # Documentation (you are here)
│   ├── BASIC_WORKFLOW.md          # Main workflow guide
│   ├── MISC_TOOLS.md              # Utility tools reference
│   ├── README.md                  # This file
│   ├── README_HTML_GENERATOR.md   # HTML generator docs
│   ├── README_MODULES.md          # Extraction modules docs
│   └── old/                       # Historical documentation
│
├── scripts/                       # Main workflow scripts
│   ├── batch_convert.py           # Convert DOCX to JSON
│   ├── docx_to_json_converter.py  # Core converter
│   ├── json_validate.py           # Validate and fix JSON
│   ├── rebuild_hierarchy.py       # Rebuild hierarchy
│   ├── generate_index_html.py     # Generate HTML visualization
│   ├── extract_evidence.py        # Evidence extractor module
│   ├── extract_glossary.py        # Glossary extractor module
│   ├── extract_references.py      # References extractor module
│   └── tools/                     # Miscellaneous tools
│       ├── accept_tracked_changes.py
│       ├── compare_docx_files_from_diff_sources.py
│       ├── flatten_one_docx.sh
│       ├── regenerate_hierarchy_table.py
│       └── validate_questions.py
│
├── docs_by_author/                # Source DOCX files by author
├── JSON4/                         # Current validated question base
└── schema/                        # JSON schemas
```

---

## 🔧 Maintenance

### Adding New Documentation

Place new documentation in this `docs/` folder and update this README.

### Updating Documentation

When scripts change, update the corresponding documentation:
- Workflow changes → Update BASIC_WORKFLOW.md
- New tools → Update MISC_TOOLS.md
- Module changes → Update README_MODULES.md

### Archiving Documentation

Move outdated documentation to `docs/old/` with a note in this README.

---

**Last Updated**: 2025-12-26
**Version**: 1.0
