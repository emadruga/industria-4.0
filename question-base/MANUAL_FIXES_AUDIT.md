# Manual Fixes Audit - Post-Conversion Adjustments

## Overview
**CRITICAL ISSUE**: The converter produces incomplete/incorrect JSON that requires manual Python scripts to fix.

This document tracks EVERY manual fix applied after conversion.

---

## File 1: gestao_agil.json (Ewerton Madruga)

### Conversion 1 - Original (First file created)

**Converter Output**:
```json
{
  "capacity": {
    "id": "CAP-ORG-EE-UN-001",
    "name": "20251105_checklist_gestao_agil",
    "dimension": "",  // ❌ EMPTY
    ...
  }
}
```

**Manual Fixes Applied** (via inline Python script):

1. **Fix 1: Dimension field** ❌
   ```python
   data['capacity']['dimension'] = 'Competência de Liderança'  # MANUAL
   ```

2. **Fix 2: Capacity name** ❌
   ```python
   data['capacity']['name'] = 'Gestão Ágil'  # MANUAL (was filename)
   ```

3. **Fix 3: Capacity ID** ❌
   ```python
   data['capacity']['id'] = 'CAP-ORG-EG-CL-001'  # MANUAL (was wrong prefix)
   ```

4. **Fix 4: ALL Question IDs** (6 questions) ❌
   ```python
   # Had to fix all 6 question IDs manually
   q['id'] = f"Q-ORG-EG-CL-GA-{i:03d}"  # Was Q-ORG-EE-UN-001-001
   ```

5. **Fix 5: Remove co_authors field** ❌
   ```python
   # Remove co_authors: null (schema violation)
   del data['capacity']['metadata']['co_authors']
   ```

6. **Fix 6: Add Glossary** ❌
   ```python
   # Converter didn't extract glossary initially
   # Had to run separate extraction script
   data['glossary'] = extract_glossary(...)  # 19 terms
   ```

7. **Fix 7: Add References** ❌
   ```python
   # Converter didn't extract references initially
   # Had to run separate extraction script
   data['references'] = extract_references(...)  # 15 refs
   ```

**Total Manual Fixes: 7**

---

## File 2: automacao_shop_floor.json (Wilson Melo Jr)

### Conversion 1 - Original

**Converter Output**:
```json
{
  "capacity": {
    "id": "CAP-TEC-AU-UN-001",
    "name": "Shop Floor (D4)",
    "dimension": "",  // ❌ EMPTY
    "description": "Dimensão: Shop Floor (Chão de Fábrica) (D4) Resumo Descritivo Esta dimensão...",  // ❌ Messy
    ...
  }
}
```

**Manual Fixes Applied**:

1. **Fix 1: Dimension field** ❌
   ```python
   data['capacity']['dimension'] = 'Shop Floor'  # MANUAL
   ```

2. **Fix 2: Capacity name** ❌
   ```python
   data['capacity']['name'] = 'Automação de Shop Floor'  # MANUAL
   ```

3. **Fix 3: Capacity ID** ❌
   ```python
   data['capacity']['id'] = 'CAP-TEC-AU-SF-001'  # MANUAL (wrong prefix)
   ```

4. **Fix 4: Clean description** ❌
   ```python
   # Remove "Dimensão: ... Resumo Descritivo" prefix
   desc = re.sub(r'Dimensão:.*?\(D4\)\s*Resumo Descritivo\s*', '', desc)
   ```

5. **Fix 5: ALL Question IDs** (3 questions) ❌
   ```python
   # Had to fix all 3 question IDs manually
   q['id'] = f"Q-TEC-AU-SF-ASF-{i:03d}"  # Was Q-TEC-AU-UN-001-001
   ```

6. **Fix 6: Remove co_authors field** ❌
   ```python
   del data['capacity']['metadata']['co_authors']
   ```

7. **Fix 7: Add Glossary** ❌
   ```python
   # No glossary in this doc, but still had to handle it
   data['glossary'] = []
   ```

8. **Fix 8: Add References** ❌
   ```python
   # Initial extraction got 0 refs
   # Manual extraction script got 12 refs
   data['references'] = extract_references(...)  # 12 refs
   ```

**Total Manual Fixes: 8**

---

## File 1 (data2/): gestao_agil.json - With Integrated Modules

### Conversion 2 - With extraction modules

**Converter Output** (improved):
```json
{
  "capacity": {
    "id": "CAP-ORG-EE-UN-001",  // ❌ Still wrong
    "name": "20251105_checklist_gestao_agil",  // ❌ Still filename
    "dimension": "",  // ❌ Still empty
    ...
  },
  "glossary": [...],  // ✅ Auto-extracted (19 terms)!
  "references": [...]  // ✅ Auto-extracted (15 refs)!
}
```

**Manual Fixes Applied**:

1. **Fix 1: Dimension field** ❌
   ```python
   data['capacity']['dimension'] = 'Competência de Liderança'  # STILL MANUAL
   ```

2. **Fix 2: Capacity name** ❌
   ```python
   data['capacity']['name'] = 'Gestão Ágil'  # STILL MANUAL
   ```

3. **Fix 3: Capacity ID** ❌
   ```python
   data['capacity']['id'] = 'CAP-ORG-EG-CL-001'  # STILL MANUAL
   ```

4. **Fix 4: ALL Question IDs** (6 questions) ❌
   ```python
   q['id'] = f"Q-ORG-EG-CL-GA-{i:03d}"  # STILL MANUAL
   ```

**Total Manual Fixes: 4** (improved from 7, but still significant)

---

## File 2 (data2/): automacao_shop_floor.json - With Integrated Modules

### Conversion 2 - With extraction modules

**Converter Output**:
```json
{
  "capacity": {
    "id": "CAP-TEC-AU-UN-001",  // ❌ Still wrong
    "name": "Shop Floor (D4)",  // ❌ Not cleaned
    "dimension": "",  // ❌ Still empty
    "description": "Dimensão: Shop Floor...",  // ❌ Still messy
    ...
  },
  "glossary": [],  // ✅ Correct (none in doc)
  "references": [...]  // ⚠️ Only 1 ref (should be 12)
}
```

**Manual Fixes Applied**:

1. **Fix 1: Dimension field** ❌
2. **Fix 2: Capacity name** ❌
3. **Fix 3: Capacity ID** ❌
4. **Fix 4: Clean description** ❌
5. **Fix 5: ALL Question IDs** (3) ❌
6. **Fix 6: Split references** ❌ (multi-line cell issue)

**Total Manual Fixes: 6** (improved from 8)

---

## Summary Statistics

### Manual Fixes Per File

| File | Version | Manual Fixes | Auto-Extracted | Manual Fix Rate |
|------|---------|--------------|----------------|-----------------|
| Gestão Ágil | v1 (no modules) | **7 fixes** | 0 | 100% |
| Gestão Ágil | v2 (with modules) | **4 fixes** | 2 items | 67% |
| Shop Floor | v1 (no modules) | **8 fixes** | 0 | 100% |
| Shop Floor | v2 (with modules) | **6 fixes** | 1 item | 86% |

### Issues Requiring Manual Fixes

#### Critical Issues (Affect ALL files)

1. **❌ Dimension extraction** - ALWAYS empty
   - **Impact**: 100% of files
   - **Manual work**: Must extract from description text
   - **Fix complexity**: Medium (regex parsing)

2. **❌ Capacity name extraction** - Uses filename
   - **Impact**: 100% of files
   - **Manual work**: Must infer proper name
   - **Fix complexity**: Medium (domain knowledge)

3. **❌ Capacity ID generation** - Wrong prefix
   - **Impact**: 100% of files
   - **Manual work**: Regenerate based on hierarchy
   - **Fix complexity**: Low (algorithmic)

4. **❌ Question ID generation** - Wrong prefix
   - **Impact**: 100% of questions (all 6 + 3 = 9)
   - **Manual work**: Regenerate all IDs
   - **Fix complexity**: Low (loop)

5. **❌ co_authors field** - Null instead of omitted
   - **Impact**: 100% of files
   - **Manual work**: Remove field
   - **Fix complexity**: Trivial

#### Moderate Issues (Some files)

6. **❌ Description cleanup** - Contains metadata
   - **Impact**: ~50% of files
   - **Manual work**: Regex cleanup
   - **Fix complexity**: Medium

7. **⚠️ References splitting** - Multi-line cells
   - **Impact**: Some files (Wilson's format)
   - **Manual work**: Split by newlines
   - **Fix complexity**: Low

#### Resolved by Modules

8. **✅ Glossary extraction** - Now automated
9. **✅ References extraction** - Now automated (mostly)

---

## The Real Cost

### Per-File Manual Work

**Without modules**: ~15-20 minutes per file
- Extract glossary manually
- Extract references manually
- Fix all metadata fields
- Validate and test

**With modules**: ~5-10 minutes per file
- Fix metadata fields (4-6 fixes)
- Validate and test

### For 100 files (project total)

**Without modules**: 25-33 hours of manual work
**With modules**: 8-17 hours of manual work

**Savings**: ~15 hours (45% reduction)
**But still**: 8-17 hours of manual fixes needed!

---

## Root Causes

### Why So Many Manual Fixes?

1. **Dimension parsing not implemented**
   - Parser looks for "dimension" in table key
   - Actually in description text: "Dimensão: X"
   - **Should be**: Parse from description

2. **Capacity name uses filename fallback**
   - Parser can't find explicit capacity name
   - Falls back to DOCX filename
   - **Should be**: Infer from dimension or description

3. **ID generation happens too early**
   - IDs generated before dimension is known
   - Uses placeholder codes (UN = unknown)
   - **Should be**: Generate IDs after all metadata extracted

4. **Schema strictness**
   - co_authors: null fails validation
   - **Should be**: Don't add optional fields if None

5. **Table format variations**
   - Different authors use different table layouts
   - Single-cell vs multi-row references
   - **Should be**: Handle multiple formats

---

## Recommendations

### Priority 1 - Fix Core Parser (HIGH IMPACT)

1. **Improve _extract_capacity_info()** method
   - Parse dimension from description text
   - Extract proper capacity name
   - **Impact**: Eliminates 3 manual fixes per file

2. **Delay ID generation**
   - Generate IDs after all metadata known
   - Use proper codes instead of placeholders
   - **Impact**: Eliminates 2 manual fixes per file (capacity + all questions)

3. **Skip None optional fields**
   - Don't add co_authors if None
   - **Impact**: Eliminates 1 manual fix per file

**Total Impact**: **6 manual fixes eliminated** = 60% reduction

### Priority 2 - Improve Extractors (MEDIUM IMPACT)

4. **Enhance references extractor**
   - Split multi-line cells
   - Better table detection
   - **Impact**: Improves extraction quality

5. **Enhance evidence extractor**
   - Actually extract from question tables
   - Parse A), B), C), D) sections
   - **Impact**: Completes data extraction

### Priority 3 - Testing & Validation (QUALITY)

6. **Automated tests**
   - Test parser with all author formats
   - Validate against expected output
   - **Impact**: Catch issues early

---

## Conclusion

**Current State**: Converter requires **4-8 manual fixes per file**

**With Priority 1 fixes**: Could reduce to **0-2 manual fixes per file**

**Critical insight**: The extraction modules (glossary, references) are working well, but the core parser (capacity metadata) needs significant improvement.

**Bottom line**: We're treating symptoms (manual fixes) instead of the disease (parser limitations).

---

**Audit Date**: 2025-11-29
**Files Analyzed**: 4 (2 original + 2 data2)
**Total Manual Fixes Tracked**: 25 fixes across 4 files
**Average Manual Fixes Per File**: 6.25 fixes
