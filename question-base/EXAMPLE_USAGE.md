# Example Usage Scenarios

## Scenario 1: Convert All Questions from One Author

```bash
conda activate INDUSTRIA4
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

# Convert all Ewerton's files
python batch_convert.py \
  "../../mdic-suframa/templates/Organização/Estrutura e Gestão - Ewerton" \
  -o "../data_ewerton" \
  -a "Ewerton"
```

## Scenario 2: Validate All Converted Files

```bash
# Validate entire directory (schema validation)
python validate_questions.py \
  ../data/ \
  -r \
  -v
```

## Scenario 2b: Validate Hierarchy Consistency Against Catalog

After running `batch_convert.py`, validate that all JSON files have consistent Block, Pilar, and Dimension names matching the official catalog:

```bash
conda activate INDUSTRIA4
cd /Users/emadruga/proj/industria-4.0

# Validate all JSON files against the Excel catalog
python question-base/scripts/json_validate.py \
  question-base/JSON/data \
  -e mdic-suframa/templates/acatech_siri_comparacao.xlsx

# Fix issues automatically
python question-base/scripts/json_validate.py \
  question-base/JSON/data \
  -e mdic-suframa/templates/acatech_siri_comparacao.xlsx \
  --fix
```

**What it validates:**
- Block names (Organização, Processo, Tecnologia)
- Pilar names (e.g., "Estrutura e Gestão", "Automação", etc.)
- Dimension names (e.g., "Competência de Liderança", "Chão de Fábrica", etc.)

**Features:**
- Loads capacity catalog from Excel with English→Portuguese translation
- Removes dimension codes like (D4), (D10), etc.
- Reports issues organized by category (Block/Pilar/Dimension mismatches)
- `--fix` flag automatically corrects all issues

**Example output:**
```
ISSUES BY CATEGORY
============================================================

BLOCK MISMATCH (1 issues)
------------------------------------------------------------
  • foco_em_benefícios_ao_cliente.json
    Current:  'Tecnologia'
    Expected: 'Processo'

DIMENSION MISMATCH (12 issues)
------------------------------------------------------------
  • comunicação_aberta.json
    Current:  'Colaboração Inter e Intraempresarial'
    Expected: 'Colaboração Inter e Intra-Empresarial'
  ...

VALIDATION SUMMARY
============================================================
Total files validated: 19
Valid files: 4 ✅
Files with issues: 12 ⚠️
Total issues found: 14

💡 Run with --fix flag to automatically fix these issues
```

## Scenario 3: Generate Statistics Report

```python
# Python script to analyze question base
import json
from pathlib import Path

data_dir = Path("../data")
total_questions = 0
total_capacities = 0

for json_file in data_dir.rglob("*.json"):
    with open(json_file) as f:
        data = json.load(f)
        total_capacities += 1
        total_questions += len(data["questions"])

print(f"Total Capacities: {total_capacities}")
print(f"Total Questions: {total_questions}")
print(f"Average: {total_questions/total_capacities:.1f} questions/capacity")
```

## Scenario 4: Search for Questions by Keyword

```bash
# Find all questions about "agilidade"
grep -r "agilidade" ../data/ --include="*.json"
```

## Scenario 5: Export Capacity Names

```bash
# List all capacity names
find ../data -name "*.json" -exec jq -r '.capacity.name' {} \;
```

## Scenario 6: Check Maturity Level Consistency

```bash
# Validate all files have proper maturity levels
python scripts/validate_questions.py ../data/ -r | grep "maturity"
```

## Scenario 7: Compare Two Authors' Work

```bash
# Convert files from two authors
python batch_convert.py "../../mdic-suframa/templates/Organização/Estrutura e Gestão - Ewerton" -o ../data_ewerton
python batch_convert.py "../../mdic-suframa/templates/Organização" -o ../data_cgcastro -a "Carlos Castro"

# Compare question counts
echo "Ewerton:" && find ../data_ewerton -name "*.json" | wc -l
echo "Castro:" && find ../data_cgcastro -name "*.json" | wc -l
```

## Scenario 8: Generate Summary Report

```bash
# Create a markdown report
python scripts/generate_report.py ../data/ > REPORT.md
```

(Note: You'll need to create generate_report.py for this)

## Scenario 9: Export to Excel

```python
# Export all questions to Excel
import json
import pandas as pd
from pathlib import Path

data = []
for json_file in Path("../data").rglob("*.json"):
    with open(json_file) as f:
        content = json.load(f)
        capacity = content["capacity"]
        for q in content["questions"]:
            data.append({
                "Block": capacity["block"],
                "Pilar": capacity["pilar"],
                "Dimension": capacity["dimension"],
                "Capacity": capacity["name"],
                "Question #": q["question_number"],
                "Question": q["text"],
                "Maturity Levels": len(q["maturity_levels"])
            })

df = pd.DataFrame(data)
df.to_excel("questions_summary.xlsx", index=False)
print(f"Exported {len(df)} questions to Excel")
```

## Scenario 10: Find Missing Evidence Sources

```python
# Check which questions lack evidence sources
import json
from pathlib import Path

missing_evidence = []

for json_file in Path("../data").rglob("*.json"):
    with open(json_file) as f:
        data = json.load(f)
        capacity_name = data["capacity"]["name"]

        for q in data["questions"]:
            if not q.get("evidence_sources"):
                missing_evidence.append({
                    "capacity": capacity_name,
                    "question": q["question_number"]
                })

print(f"Found {len(missing_evidence)} questions without evidence sources")
for item in missing_evidence:
    print(f"  {item['capacity']} - Question {item['question']}")
```
