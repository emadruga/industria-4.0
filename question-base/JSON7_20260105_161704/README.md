# JSON7 - Evidence Structure Restructuring

**Created**: 2026-01-05
**Version**: 7.0

## Changes from JSON6

This version implements a cleaner evidence structure that eliminates redundancy and properly separates concerns:

### Evidence Structure Changes

#### ✅ What Changed:

1. **Maturity Level Evidence** (`maturity_levels[i].evidence_signals`):
   - **REMOVED**: `artifacts`, `metrics`, `interview_questions`
   - **KEPT**: Only `observable_behaviors` (the level-specific signals N0-N6)

2. **Question-Level Evidence** (`evidence_sources`):
   - **REMOVED**: `signals_by_level` (redundant with maturity levels)
   - **KEPT**: `artifacts`, `metrics`, `sampling_guidance`

#### Before (JSON6):
```json
{
  "maturity_levels": [{
    "level": 0,
    "evidence_signals": {
      "artifacts": ["..."],           // ❌ Duplicated
      "metrics": ["..."],             // ❌ Duplicated
      "observable_behaviors": ["..."], // ✅ Level-specific
      "interview_questions": []       // ❌ Always empty
    }
  }],
  "evidence_sources": {
    "artifacts": ["..."],
    "metrics": ["..."],
    "signals_by_level": {             // ❌ Redundant
      "N0": {
        "artifacts": [],
        "metrics": [],
        "observable_behaviors": ["..."],
        "interview_questions": []
      }
    },
    "sampling_guidance": "..."
  }
}
```

#### After (JSON7):
```json
{
  "maturity_levels": [{
    "level": 0,
    "evidence_signals": {
      "observable_behaviors": ["..."] // ✅ Only level-specific signals
    }
  }],
  "evidence_sources": {
    "artifacts": ["..."],             // ✅ Question-level only
    "metrics": ["..."],               // ✅ Question-level only
    "sampling_guidance": "..."        // ✅ Question-level only
  }
}
```

## Modified Scripts

1. **extract_evidence.py**
   - `_extract_signals_by_level()`: Returns only `observable_behaviors` for each level

2. **docx_to_json_converter.py**
   - `EvidenceSources` dataclass: Removed `signals_by_level` field
   - `_map_evidence_to_maturity_levels()`: Simplified to only map observable behaviors
   - Evidence sources creation: Removed `signals_by_level` parameter

3. **generate_index_html.py**
   - `hasEvidence` check: Only checks for `observable_behaviors`
   - `renderEvidenceSection()`: Only renders observable behaviors

## Statistics

- **Total Files**: 25 DOCX files converted
- **Total Capacities**: 23
- **Total Questions**: 137
- **Average Questions/Capacity**: 5.8
- **Blocks**: 3 (Organização, Processo, Tecnologia)
- **Pilares**: 7
- **Dimensions**: 15

## Validation Results

- Files processed: 23
- Issues found: 66
- Issues auto-fixed: 65 ✅
- Remaining warnings: 4 (capacities not in catalog)

## HTML Visualization

View the interactive catalog:
```
file:///Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_161704/metadata/index.html
```

## Rationale

The JSON7 structure follows the principle that:

1. **Artifacts and Metrics** are general evidence types that apply to ALL maturity levels of a question
   - They belong at the question level, not duplicated at each level
   
2. **Observable Behaviors** are the level-specific signals (N0-N6) that distinguish one maturity level from another
   - They belong inside each maturity level definition

3. **Interview Questions** field was always empty and provided no value
   - Removed to reduce clutter

This creates a cleaner, more maintainable structure that's easier to understand and work with.
