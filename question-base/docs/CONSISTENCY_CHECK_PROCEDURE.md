# JSON Consistency Check and Coverage Validation Procedures

This document explains how to validate the Industry 4.0 JSON question catalog using the available Python scripts.

## Overview

Two main validation scripts are available:

1. **`json_consistency_check.py`** - Validates JSON files against schema requirements
2. **`json_coverage_validation.py`** - Cross-references ACATECH capacities with JSON catalog

---

## Prerequisites

### Environment Setup

Both scripts require the INDUSTRIA4 conda environment:

```bash
# Activate the conda environment
source ~/.zshrc
conda activate INDUSTRIA4
```

### Required Python Packages

- `pandas` - For Excel file handling
- `openpyxl` - For Excel file reading/writing
- `json` - Standard library (no installation needed)

---

## Script 1: JSON Consistency Check

### Purpose

Validates all JSON files in the catalog against the Industry 4.0 maturity model schema. Checks for:

- **MATURITY_LEVEL_LABEL** - Ensures labels follow "Nível X" format
- **MATURITY_LEVEL_DESCRIPTION** - Validates non-empty descriptions
- **OBSERVABLE_BEHAVIORS** - Ensures evidence signals are provided
- General JSON structure and required fields

### Location

```
question-base/scripts/json_consistency_check.py
```

### Usage

#### Basic Syntax

```bash
python json_consistency_check.py <data_directory> [output_excel_file]
```

#### Parameters

- `<data_directory>` (required) - Path to the directory containing JSON files
- `[output_excel_file]` (optional) - Path to generate an Excel report with all issues

#### Example 1: Console Output Only

```bash
cd /Users/emadruga/proj/industria-4.0/question-base

python scripts/json_consistency_check.py JSON7_20260105_164046/data
```

**Expected Output:**

```
JSON Consistency Checker
Data directory: /Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/data

Found 23 JSON files to validate

Validating: data/Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/comunicação_aberta.json
Validating: data/Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/comunicação_eficiente.json
...

================================================================================
VALIDATION REPORT
================================================================================

Files processed: 23
Valid files: 23
Files with errors: 0

Issues found:
  - Errors: 0
  - Warnings: 0
  - Info: 0

Authors: 4
  - Cristiano Gurgel Castro
  - Ewerton Madruga
  - Flavia Agostini
  - Wilson Melo Jr

Frameworks: 2
  - ACATECH
  - SIRI

================================================================================
✓ All files passed validation!
================================================================================
```

#### Example 2: Save Output to Markdown File

```bash
cd /Users/emadruga/proj/industria-4.0/question-base

python scripts/json_consistency_check.py JSON7_20260105_164046/data \
  > docs/JSON_CONSISTENCY_CHECK_$(date +%Y%m%d_%H%M%S).md
```

This creates a timestamped markdown file like:
```
docs/JSON_CONSISTENCY_CHECK_20250116_102900.md
```

#### Example 3: Generate Excel Report with Issues

```bash
cd /Users/emadruga/proj/industria-4.0/question-base

python scripts/json_consistency_check.py \
  JSON7_20260105_164046/data \
  docs/validation_issues.xlsx
```

**Excel Output:** The generated Excel file will contain:
- Column A: File path
- Column B: Issue type (WARNING, ERROR, INFO)
- Column C: Issue category (MATURITY_LEVEL_LABEL, etc.)
- Column D: Detailed message
- Column E: Question ID (if applicable)

### Understanding Validation Results

#### Issue Types

- **ERROR** - Critical issues that must be fixed (malformed JSON, missing required fields)
- **WARNING** - Non-critical issues that should be addressed (empty descriptions, missing labels)
- **INFO** - Informational messages (statistics, file counts)

#### Common Warnings

1. **MATURITY_LEVEL_LABEL**
   ```
   WARNING: Label should be "Nível X" but found "Integração básica"
   Fix: Change label to "Nível 1" and move text to description
   ```

2. **MATURITY_LEVEL_DESCRIPTION**
   ```
   WARNING: Empty or missing description for maturity level 5
   Fix: Add a meaningful description explaining the maturity level
   ```

3. **OBSERVABLE_BEHAVIORS**
   ```
   WARNING: Empty observable_behaviors list for level 0
   Fix: Add 2-3 concrete, observable indicators
   ```

---

## Script 2: JSON Coverage Validation

### Purpose

Cross-references ACATECH capacity definitions from the Excel template against the JSON7 catalog to identify:

- Which capacities have been implemented as JSON files
- Which capacities are still missing
- Coverage percentage
- Authorship information

### Location

```
question-base/scripts/json_coverage_validation.py
```

### Usage

#### Basic Syntax

The script has hardcoded paths and generates output automatically:

```bash
python json_coverage_validation.py
```

#### Configured Paths (inside script)

- **Excel template:** `mdic-suframa/templates/acatech_siri_comparacao_v2.xlsx`
- **JSON catalog:** `question-base/JSON7_20260105_164046/data`
- **Output report:** `question-base/docs/json_coverage_validation.xlsx`

#### Example: Run Coverage Validation

```bash
cd /Users/emadruga/proj/industria-4.0

source ~/.zshrc && conda activate INDUSTRIA4

python question-base/scripts/json_coverage_validation.py
```

**Expected Output:**

```
JSON Coverage Validation
================================================================================
Excel template: /Users/emadruga/proj/industria-4.0/mdic-suframa/templates/acatech_siri_comparacao_v2.xlsx
JSON catalog: /Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/data

Reading ACATECH capacities from Excel...
Found 28 capacities in ACATECH sheet

Scanning JSON catalog...
Found 23 JSON capacity files

Cross-referencing capacities...
================================================================================
COVERAGE VALIDATION REPORT
================================================================================

Total ACATECH capacities: 28
Found in JSON catalog: 19 (67.9%)
Missing from JSON catalog: 9

Missing capacities:
  - Row 4: Interface de usuário específica (Dimension: Sistemas de Informação)
  - Row 8: Segurança de TI (Dimension: Sistemas de Informação)
  - Row 12: Aprendizagem e tomada de decisão baseadas em dados (Dimension: Cultura)
  - Row 13: Integração horizontal e vertical (Dimension: Sistemas de Informação)
  - Row 14: Integração horizontal e vertical (Dimension: Sistemas de Informação)
  - Row 18: Comunidades flexíveis (Dimension: Estrutura Organizacional)
  - Row 19: Gestão de direitos de decisão (Dimension: Estrutura Organizacional)
  - Row 24: Dar forma à mudança (Dimension: Cultura)
  - Row 28: Prover competências digitais (Dimension: Recursos)

Report saved to: /Users/emadruga/proj/industria-4.0/question-base/docs/json_coverage_validation.xlsx
================================================================================
```

### Understanding Coverage Results

#### Excel Report Columns

The generated `json_coverage_validation.xlsx` contains:

| Column | Description |
|--------|-------------|
| **Dimension in ACATECH Sheet** | Structural area (Recursos, Sistemas de Informação, Cultura, etc.) |
| **Capacity in ACATECH** | Portuguese name of the capacity |
| **Capacity Responsible in ACATECH** | Person assigned to create the capacity |
| **Row in ACATECH Sheet** | Excel row number for easy reference |
| **Corresponding JSON File Exists?** | "Yes" or "No" |
| **JSON File Path** | Relative path if file exists, empty if missing |
| **Author Inside JSON File** | Author metadata from JSON file |

#### Example Report Rows

**Capacity Found:**
```
Dimension: Recursos
Capacity: Design de interfaces orientado à tarefa
Responsible: Wilson
Row: 3
Exists: Yes
Path: data/Tecnologia/Automação/Chão_de_Fábrica/design_de_interfaces_orientado_à_tarefa.json
Author: Wilson Melo Jr
```

**Capacity Missing:**
```
Dimension: Sistemas de Informação
Capacity: Segurança de TI
Responsible: Wilson
Row: 8
Exists: No
Path: (empty)
Author: (empty)
```

---

## Complete Workflow Example

### Step 1: Check Current State

```bash
cd /Users/emadruga/proj/industria-4.0/question-base

# Run consistency check
python scripts/json_consistency_check.py JSON7_20260105_164046/data \
  > docs/consistency_check_$(date +%Y%m%d).md
```

### Step 2: Check Coverage

```bash
cd /Users/emadruga/proj/industria-4.0

# Run coverage validation
python question-base/scripts/json_coverage_validation.py
```

### Step 3: Review Reports

```bash
# View consistency check results
cat question-base/docs/consistency_check_20250116.md

# Open coverage report in Excel
open question-base/docs/json_coverage_validation.xlsx
```

### Step 4: Fix Issues (if any)

If warnings are found, fix them in the JSON files and re-run validation:

```bash
# After fixing issues, validate again
python question-base/scripts/json_consistency_check.py JSON7_20260105_164046/data
```

---

## Automation with Shell Script

You can create a validation script for regular checks:

```bash
#!/bin/bash
# File: question-base/scripts/run_all_validations.sh

echo "Running Industry 4.0 JSON Validations"
echo "======================================"
echo ""

# Activate conda environment
source ~/.zshrc
conda activate INDUSTRIA4

# Set timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Run consistency check
echo "1. Running consistency check..."
cd question-base
python scripts/json_consistency_check.py JSON7_20260105_164046/data \
  > docs/JSON_CONSISTENCY_CHECK_${TIMESTAMP}.md

echo "   Report saved to: docs/JSON_CONSISTENCY_CHECK_${TIMESTAMP}.md"
echo ""

# Run coverage validation
echo "2. Running coverage validation..."
cd ..
python question-base/scripts/json_coverage_validation.py

echo ""
echo "======================================"
echo "All validations complete!"
```

Make it executable:

```bash
chmod +x question-base/scripts/run_all_validations.sh
```

Run all validations:

```bash
./question-base/scripts/run_all_validations.sh
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
```bash
conda activate INDUSTRIA4
conda install pandas openpyxl
```

### Issue: "FileNotFoundError: [Errno 2] No such file or directory"

**Solution:** Ensure you're running the script from the correct directory:
```bash
cd /Users/emadruga/proj/industria-4.0
python question-base/scripts/json_coverage_validation.py
```

### Issue: "Worksheet named 'ACATECH' not found"

This means the Excel template structure has changed. The script expects a sheet named **"Capacidades (acatech × SIRI)"**.

**Solution:** Verify the Excel file exists:
```bash
ls -l mdic-suframa/templates/acatech_siri_comparacao_v2.xlsx
```

---

## Best Practices

1. **Run validations before committing changes**
   ```bash
   python question-base/scripts/json_consistency_check.py JSON7_20260105_164046/data
   ```

2. **Save validation reports with timestamps** for historical tracking
   ```bash
   > docs/JSON_CONSISTENCY_CHECK_$(date +%Y%m%d_%H%M%S).md
   ```

3. **Check coverage regularly** to track progress on missing capacities
   ```bash
   python question-base/scripts/json_coverage_validation.py
   ```

4. **Fix all ERRORs immediately**, address WARNINGs before releasing

5. **Document fixes in git commits** with references to validation reports

---

## File Locations Summary

```
question-base/
├── scripts/
│   ├── json_consistency_check.py       # Schema validation
│   ├── json_coverage_validation.py     # Coverage analysis
│   └── run_all_validations.sh          # Optional automation script
├── docs/
│   ├── JSON_CONSISTENCY_CHECK_*.md     # Validation reports (timestamped)
│   ├── json_coverage_validation.xlsx   # Coverage report
│   └── CONSISTENCY_CHECK_PROCEDURE.md  # This document
└── JSON7_20260105_164046/
    └── data/                            # JSON catalog files

mdic-suframa/
└── templates/
    └── acatech_siri_comparacao_v2.xlsx # ACATECH capacity reference
```

---

## Additional Resources

- **JSON Schema Documentation**: See `question-base/schemas/` for detailed schema definitions
- **Hierarchy Documentation**: See `question-base/JSON7_20260105_164046/metadata/hierarchy_table.md`
- **Git Commit History**: Review previous validation fixes with `git log --grep="consistency\|validation"`

---

**Last Updated:** 2025-01-16
**Maintained by:** Ewerton Madruga
