# Basic Workflow - Industry 4.0 Question Base

This document describes the complete workflow to build a validated JSON question base from DOCX source files.

## Prerequisites

- **Conda environment**: `INDUSTRIA4` activated
- **Source files**: DOCX files in `docs_by_author/` organized by author
- **Catalog file**: `../mdic-suframa/templates/acatech_siri_comparacao.xlsx`

## Workflow Steps

### Step 1: Convert DOCX Files to JSON

Convert all DOCX files from the `docs_by_author/` directory to JSON format.

```bash
# Activate conda environment
conda activate INDUSTRIA4

# Navigate to scripts directory
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

# Create new JSON folder with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="../JSON_${TIMESTAMP}"

# Run batch conversion
python batch_convert.py ../docs_by_author -o "$OUTPUT_DIR"
```

**Output**:
- JSON files in `$OUTPUT_DIR/data/` organized by Block/Pilar/Dimension
- `$OUTPUT_DIR/metadata/hierarchy.json`
- `$OUTPUT_DIR/metadata/hierarchy_table.md`

**Expected**: All DOCX files successfully converted to JSON format.

---

### Step 2: Validate and Fix JSON Files

Validate all JSON files against the capacity catalog and automatically fix issues.

```bash
# Run validation with auto-fix
python json_validate.py "${OUTPUT_DIR}/data" \
  -e ../mdic-suframa/templates/acatech_siri_comparacao.xlsx \
  --fix
```

**What this does**:
- Validates Block/Pilar/Dimension fields against catalog
- Cleans capacity descriptions (removes "Resumo Descritivo", English dimension names, headers)
- Replaces "Tema" question titles with meaningful text from question content
- Moves files to correct directories if hierarchy changed
- Removes empty directories

**Expected**:
- Most issues auto-fixed
- Files moved to correct locations if needed
- Summary shows "Issues fixed: X"

---

### Step 3: Rebuild Hierarchy

After validation moves files, rebuild the hierarchy to reflect the new structure.

```bash
# Rebuild hierarchy.json
python rebuild_hierarchy.py "$OUTPUT_DIR"
```

**Output**:
- Updated `$OUTPUT_DIR/metadata/hierarchy.json` with correct statistics

**Expected statistics** (as of 2025-12-26):
- Total capacities: 23
- Total questions: ~137
- Total dimensions: 15
- Total pilares: 7
- Total blocks: 3

---

### Step 4: Generate HTML Visualization

Generate an interactive HTML file for viewing and analyzing the question base.

```bash
# Generate HTML from hierarchy table
python generate_index_html.py "${OUTPUT_DIR}/metadata/hierarchy_table.md"
```

**Output**:
- `$OUTPUT_DIR/metadata/index.html`

**To view**:
```bash
open "${OUTPUT_DIR}/metadata/index.html"
```

Or navigate to: `file:///Users/emadruga/proj/industria-4.0/question-base/${OUTPUT_DIR}/metadata/index.html`

---

## Complete Script

Run all steps in sequence:

```bash
#!/bin/bash
# Complete workflow to build JSON question base

# Activate environment
conda activate INDUSTRIA4

# Navigate to scripts directory
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

# Create timestamped output directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="../JSON_${TIMESTAMP}"

echo "========================================="
echo "Building JSON Question Base: ${OUTPUT_DIR}"
echo "========================================="
echo ""

# Step 1: Convert DOCX to JSON
echo "Step 1: Converting DOCX files to JSON..."
python batch_convert.py ../docs_by_author -o "$OUTPUT_DIR"
echo ""

# Step 2: Validate and fix JSON files
echo "Step 2: Validating and fixing JSON files..."
python json_validate.py "${OUTPUT_DIR}/data" \
  -e ../mdic-suframa/templates/acatech_siri_comparacao.xlsx \
  --fix
echo ""

# Step 3: Rebuild hierarchy
echo "Step 3: Rebuilding hierarchy..."
python rebuild_hierarchy.py "$OUTPUT_DIR"
echo ""

# Step 4: Generate HTML
echo "Step 4: Generating HTML visualization..."
python generate_index_html.py "${OUTPUT_DIR}/metadata/hierarchy_table.md"
echo ""

echo "========================================="
echo "✅ Complete! Question base ready at:"
echo "   ${OUTPUT_DIR}"
echo ""
echo "View HTML:"
echo "   open ${OUTPUT_DIR}/metadata/index.html"
echo "========================================="
```

---

## Troubleshooting

### Issue: Tracked changes in DOCX files prevent proper extraction

**Symptom**: Capacity fields are empty, causing multiple files to overwrite each other.

**Solution**: Flatten tracked changes using DOC format conversion:

```bash
# For each problematic DOCX file:
python scripts/tools/flatten_one_docx.sh /path/to/file.docx
```

See `docs/TROUBLESHOOTING.md` for more details.

### Issue: Files not found in catalog

**Symptom**: Warning messages like "Capacity 'X' not found in catalog"

**Solution**:
- Check if capacity name matches exactly with catalog
- Update catalog Excel file if needed
- These warnings are informational and don't prevent processing

### Issue: Empty questions

**Symptom**: Warning "Cannot auto-fix question X: empty question text"

**Solution**:
- Manually review the source DOCX file
- Fill in the missing question text
- Re-run the conversion

---

## Notes

- Always use timestamped output directories to preserve previous versions
- Keep `docs_by_author/` as the source of truth for DOCX files
- The validation step modifies JSON files in place and may move them
- Review the HTML visualization to ensure all capacities are correctly organized
- Empty or placeholder questions (like "TEMA" with no text) are left as-is for manual review

---

**Last Updated**: 2025-12-26
**Version**: 1.0
