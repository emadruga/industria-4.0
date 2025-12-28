# JSON6 Catalog - Evidence Signals Integration

**Version:** 2.0
**Created:** 2025-12-28
**Status:** Phase 1 Complete - Ready for Testing

---

## What's New in JSON6

JSON6 introduces **evidence signals at the maturity level**, enabling assessors to identify specific artifacts, metrics, observable behaviors, and interview questions that indicate a company's maturity level.

### Key Features

✅ **Evidence signals per maturity level** - Each level (0-5 or 0-6) has its own evidence
✅ **4 evidence categories** - Artifacts, Metrics, Observable Behaviors, Interview Questions
✅ **Expandable/collapsible UI** - Click to show/hide evidence in HTML view
✅ **"Ainda não disponível"** - Empty levels show placeholder message
✅ **Enhanced extraction** - Updated Python scripts to parse structured evidence

---

## Directory Structure

```
JSON6/
├── data/
│   └── Organização/
│       └── Estrutura_e_Gestão/
│           └── Competência_de_Liderança/
│               └── gestão_ágil.json          # Sample with full evidence
├── metadata/
│   ├── hierarchy_table.md                     # Question hierarchy
│   └── index.html                             # Generated HTML (after running script)
└── README.md                                  # This file
```

---

## Sample JSON Structure

```json
{
  "maturity_levels": [
    {
      "level": 0,
      "label": "Não familiarizada",
      "description": "A liderança não está familiarizada...",
      "evidence_signals": {
        "artifacts": [
          "Ausência de documentação sobre metodologias ágeis",
          "Falta de ferramentas de gestão ágil"
        ],
        "metrics": [
          "0% de projetos usando metodologias ágeis",
          "Nenhuma certificação ágil na equipe"
        ],
        "observable_behaviors": [
          "Liderança desconhece terminologia ágil básica",
          "Estrutura organizacional puramente hierárquica"
        ],
        "interview_questions": [
          "O que você entende por Scrum ou Kanban?",
          "A empresa já considerou adotar práticas ágeis?"
        ]
      }
    }
  ]
}
```

---

## How to Generate HTML

### 1. Activate Conda Environment

```bash
conda activate INDUSTRIA4
```

### 2. Generate HTML from JSON6 Catalog

```bash
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

python generate_index_html.py \
  ../JSON6/metadata/hierarchy_table.md \
  -o ../JSON6/metadata/index.html
```

### 3. Open in Browser

```bash
open ../JSON6/metadata/index.html
```

Or navigate to:
```
file:///Users/emadruga/proj/industria-4.0/question-base/JSON6/metadata/index.html
```

---

## HTML Features

### Evidence Display

Each maturity level card now includes:

1. **Evidence toggle button** - Click to expand/collapse
2. **4 evidence categories** with counts:
   - 📄 Artefatos (4)
   - 📊 Métricas/KPIs (4)
   - 👁️ Comportamentos Observáveis (5)
   - 💬 Perguntas para Entrevista (5)
3. **Placeholder for empty levels** - "Ainda não disponível."

### Visual Design

- **Collapsed by default** - Clean, uncluttered view
- **Smooth animations** - 60fps expand/collapse
- **Color-coded** - Light blue background for evidence section
- **Bullet lists** - Easy-to-read format

---

## Python Scripts Enhanced

### 1. `extract_evidence.py`

**Enhancement:** Parse structured evidence by maturity level

```python
def _extract_signals_by_level(self, text: str) -> Dict[str, Dict]:
    """
    Extract detailed signals organized by maturity level.

    Returns:
        {
            "N0": {
                "artifacts": [...],
                "metrics": [...],
                "observable_behaviors": [...],
                "interview_questions": [...]
            }
        }
    """
```

### 2. `docx_to_json_converter.py`

**Enhancement:** Map evidence to maturity levels

```python
def _map_evidence_to_maturity_levels(
    self,
    maturity_levels_list: List[Dict],
    evidence_data: Dict
) -> List[Dict]:
    """Map evidence signals to corresponding maturity levels."""
```

**Dataclass Update:**

```python
@dataclass
class MaturityLevel:
    level: int
    label: str
    description: str
    evidence_signals: Optional[Dict[str, List[str]]] = None  # NEW
```

### 3. `generate_index_html.py`

**Enhancements:**
- Added `toggleEvidence()` JavaScript function
- Added `renderEvidenceSection()` function
- Added CSS styles for evidence UI
- Updated maturity level rendering template

---

## Sample Data Included

### Question 1: Full Evidence (Levels 0-5)

**File:** `gestão_ágil.json` > Question 1
**Maturity Levels:** 0-5 (6 levels)
**Evidence:** Complete for all levels

### Question 2: Placeholder Evidence (Levels 0-6)

**File:** `gestão_ágil.json` > Question 2
**Maturity Levels:** 0-6 (7 levels)
**Evidence:** Empty (shows "Ainda não disponível")

---

## Testing Checklist

### Visual Testing

- [ ] Open HTML in browser
- [ ] Click on Question 1 (full evidence)
- [ ] Expand evidence for Level 0
- [ ] Verify 4 categories display correctly
- [ ] Collapse evidence for Level 0
- [ ] Expand evidence for Level 3
- [ ] Verify different evidence content
- [ ] Click on Question 2 (empty evidence)
- [ ] Expand evidence for any level
- [ ] Verify "Ainda não disponível" message

### Functional Testing

- [ ] Toggle works smoothly
- [ ] Icons change (▶ to ▼)
- [ ] Multiple levels can be expanded simultaneously
- [ ] Evidence content is readable
- [ ] Scrolling works properly
- [ ] No JavaScript errors in console

### Browser Testing

- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari

---

## Next Steps (Phase 2)

Once testing is complete:

1. **Batch conversion** - Convert all existing JSON5 files to JSON6 format
2. **Evidence extraction** - Extract evidence from DOCX files using enhanced scripts
3. **Validation** - Run quality checks on extracted evidence
4. **Documentation** - Update main README with JSON6 instructions

---

## Migration from JSON5 to JSON6

### Option 1: Manual Conversion

Add `evidence_signals` to each maturity level in existing JSON files:

```json
{
  "level": 0,
  "label": "Nível 0",
  "description": "...",
  "evidence_signals": {
    "artifacts": [],
    "metrics": [],
    "observable_behaviors": [],
    "interview_questions": []
  }
}
```

### Option 2: Automated Conversion (Recommended)

Create a migration script to:
1. Read JSON5 files
2. Add empty `evidence_signals` to all maturity levels
3. Save as JSON6 format
4. Preserve all existing data

---

## Troubleshooting

### HTML doesn't generate

**Error:** `Could not load JSON files`
**Solution:** Check that JSON files exist in `data/` directory

### Evidence doesn't display

**Error:** Evidence section is empty
**Solution:** Check JSON structure has `evidence_signals` object

### Toggle doesn't work

**Error:** Nothing happens when clicking
**Solution:** Check browser console for JavaScript errors

---

## File Sizes

- **JSON file with full evidence:** ~80-150KB per capacity
- **HTML with embedded data:** ~500KB-1MB (2 questions)
- **Expected full catalog:** ~2-3MB (acceptable for modern browsers)

---

## Support

For issues or questions:
1. Check `/question-base/docs/INTEGRATE_EVIDENCE_PLAN.md` for detailed implementation plan
2. Review sample JSON file: `gestão_ágil.json`
3. Check Python script documentation

---

**Last Updated:** 2025-12-28
**Author:** Ewerton Madruga (with Claude Code assistance)
