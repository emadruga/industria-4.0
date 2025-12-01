# Industry 4.0 Maturity Model - Question Base

This directory contains the structured question base for the Industry 4.0 Maturity Model, based on the ACATECH and SIRI frameworks.

## 📁 Directory Structure

```
question-base/
├── schema/                          # JSON schemas for validation
│   ├── question-schema.json         # Schema for question files
│   └── hierarchy-schema.json        # Schema for hierarchy structure
├── data/                            # Question data organized by hierarchy
│   ├── Organização/                 # Block 1
│   │   ├── Estrutura_e_Gestao/      # Pilar
│   │   │   └── ...                  # Dimensions/Capacities
│   │   └── ...
│   ├── Processo/                    # Block 2
│   └── Tecnologia/                  # Block 3
├── scripts/                         # Conversion and validation tools
│   ├── docx_to_json_converter.py    # Convert DOCX to JSON
│   ├── validate_questions.py        # Validate JSON files
│   └── batch_convert.py             # Batch conversion tool
├── metadata/                        # Metadata files
│   └── hierarchy.json               # Complete hierarchy structure
└── requirements.txt                 # Python dependencies
```

## 🚀 Getting Started

### 1. Install Dependencies

```bash
cd question-base
pip install -r requirements.txt
```

### 2. Convert a Single DOCX File

```bash
python scripts/docx_to_json_converter.py \
  /path/to/document.docx \
  -o output.json \
  -a "Author Name"
```

### 3. Batch Convert All DOCX Files

```bash
python scripts/batch_convert.py \
  /path/to/mdic-suframa/templates \
  -o question-base
```

This will:
- Convert all DOCX files in the templates directory
- Organize output by Block → Pilar → Dimension
- Generate a hierarchy.json file
- Print conversion statistics

### 4. Validate JSON Files

Validate a single file:
```bash
python scripts/validate_questions.py output.json -v
```

Validate all files in a directory:
```bash
python scripts/validate_questions.py data/ -r -v
```

## 📊 JSON Structure

### Capacity File Structure

Each capacity is stored in a JSON file following this structure:

```json
{
  "capacity": {
    "id": "CAP-ORG-EG-CL-001",
    "name": "Gestão Ágil",
    "block": "Organização",
    "pilar": "Estrutura e Gestão",
    "dimension": "Competência de Liderança",
    "description": "...",
    "related_capacities": [...],
    "metadata": {
      "source_frameworks": ["ACATECH", "SIRI"],
      "author": "Ewerton",
      "version": "1.0",
      "last_updated": "2025-11-29",
      "source_docx": "20251105_checklist_gestao_agil.docx",
      "status": "draft"
    }
  },
  "questions": [
    {
      "id": "Q-ORG-EG-CL-GA-001",
      "question_number": 1,
      "title": "Prontidão para Aplicação de Técnicas de Gestão Ágil",
      "text": "Qual é a prontidão da liderança...",
      "maturity_levels": [
        {
          "level": 0,
          "label": "Não familiarizada",
          "description": "..."
        }
      ],
      "evidence_sources": {
        "artifacts": [...],
        "metrics": [...],
        "signals_by_level": {...},
        "sampling_guidance": "..."
      }
    }
  ]
}
```

## 🔍 ID Conventions

- **Capacity ID**: `CAP-{BLOCK}-{PILAR}-{DIMENSION}-{NUMBER}`
  - Example: `CAP-ORG-EG-CL-001`
- **Question ID**: `Q-{BLOCK}-{PILAR}-{DIMENSION}-{CAPACITY}-{NUMBER}`
  - Example: `Q-ORG-EG-CL-GA-001`

### Block Codes
- `ORG` - Organização
- `PROC` - Processo
- `TEC` - Tecnologia

## 🧪 Validation

The validation framework checks:

### Schema Validation
- ✅ JSON syntax validity
- ✅ Required fields presence
- ✅ Data types correctness
- ✅ Field format (IDs, dates, enums)

### Semantic Validation
- ⚠️ Sequential question numbering
- ⚠️ Maturity level completeness (0-5 or 0-6)
- ⚠️ Empty text fields
- ⚠️ Duplicate IDs
- ⚠️ ID prefix matching hierarchy

## 📈 Workflow

1. **Extract**: Convert DOCX files to JSON using `docx_to_json_converter.py`
2. **Validate**: Check JSON validity using `validate_questions.py`
3. **Review**: Manually review and edit JSON files as needed
4. **Consolidate**: Merge duplicate questions from different authors
5. **Approve**: Change status from "draft" to "approved"

## 🛠️ Advanced Usage

### Custom Schema Directory
```bash
python scripts/validate_questions.py data/ -s /custom/schema/dir
```

### Export to Database (Future)
```bash
python scripts/export_to_db.py --config db_config.json
```

## 📝 Notes

- Each DOCX file should contain one capacity with multiple questions
- Questions must have maturity levels from 0 (lowest) to 5 or 6 (highest)
- Evidence sources help assessors gather the right data
- The hierarchy.json file provides a complete map of all capacities

## 🤝 Contributing

When adding new capacities:
1. Follow the template structure
2. Use the batch converter
3. Validate the output
4. Update the hierarchy.json
5. Review for duplicates with existing capacities

## 📚 References

- ACATECH Industrie 4.0 Maturity Index (2020)
- Smart Industry Readiness Index (SIRI) - Singapore EDB
- MDIC-SUFRAMA Industry 4.0 Assessment Framework
