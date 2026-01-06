# JSON7 - Evidence Structure Restructuring (FINAL)

**Created**: 2026-01-05 16:40
**Version**: 7.0

## ✅ Corrected Evidence Structure

This version implements the correct evidence hierarchy where:
- **artifacts**, **metrics**, and **sampling_guidance** are at the **question level**
- **observable_behaviors** (signals N0-N6) remain at each **maturity level**

### Final Structure

```json
{
  "questions": [{
    "id": "Q-ORG-ESTRUT-COMPET-006-001",
    "question_number": 1,
    "title": "...",
    "text": "...",
    "artifacts": ["artifact1", "artifact2"],        // ✅ At question level
    "metrics": ["metric1", "metric2"],              // ✅ At question level
    "sampling_guidance": "...",                      // ✅ At question level
    "maturity_levels": [
      {
        "level": 0,
        "label": "Nível 0",
        "description": "...",
        "evidence_signals": {
          "observable_behaviors": [                  // ✅ Level-specific signals
            "signal specific to level 0"
          ]
        }
      }
    ]
  }]
}
```

## Changes from JSON6

### ❌ JSON6 Problems:
1. `artifacts` and `metrics` were duplicated at each maturity level
2. `signals_by_level` created redundancy with maturity levels
3. `interview_questions` field was always empty

### ✅ JSON7 Solution:
1. **Question Level**: `artifacts`, `metrics`, `sampling_guidance` (apply to all maturity levels)
2. **Maturity Level**: Only `observable_behaviors` (level-specific signals N0-N6)
3. **Removed**: `interview_questions`, `signals_by_level`, `evidence_sources` wrapper

## Modified Scripts

1. **extract_evidence.py**
   - Simplified `_extract_signals_by_level()` to return only observable_behaviors

2. **docx_to_json_converter.py**  
   - Removed `EvidenceSources` dataclass
   - Updated `Question` dataclass with direct fields: `artifacts`, `metrics`, `sampling_guidance`
   - Simplified evidence mapping logic

3. **generate_index_html.py**
   - Simplified evidence detection and rendering

## Statistics

- **Total Files**: 25 DOCX files
- **Total Capacities**: 23
- **Total Questions**: 137
- **Blocks**: 3
- **Pilares**: 7
- **Dimensions**: 15
- **Issues Auto-Fixed**: 65/66

## HTML Visualization

```
file:///Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/metadata/index.html
```

## Rationale

### Why artifacts/metrics at question level?
Per author specification: "All the other evidences (artifacts, etc.) must be placed at the question level in the json format for the question."

### Why observable_behaviors at maturity level?
Per author specification: "The signals of evidence, specified by authors as going from N0 to N6 in each document, shall be presented inside each different level of maturity assessment associated with a given question."

This creates the cleanest, most logical hierarchy:
- **Question level** = General evidence applicable to all maturity levels
- **Maturity level** = Specific behavioral signals that differentiate levels
