# Fixes Applied to JSON6 HTML Generation

**Date:** 2025-12-28
**Issues Fixed:** 2

---

## Issue #1: Expand/Collapse Not Working

### Problem
The `toggleEvidence()` function was not working because the `questionIdClean` parameter was not properly quoted in the onclick handler.

### Root Cause
```javascript
// BEFORE (broken):
onclick="toggleEvidence(${{questionData.question_id.replace(/[^a-zA-Z0-9]/g, '_')}}, ${{level.level}})"
```

The replacement was happening in the template literal, generating invalid JavaScript like:
```javascript
onclick="toggleEvidence(Q_ORG_ESTRUT_COMPET_006_001, 0)"
// Missing quotes around the ID ^
```

### Fix Applied
```javascript
// AFTER (fixed):
const questionIdClean = questionData.question_id.replace(/[^a-zA-Z0-9]/g, '_');
onclick="toggleEvidence('${{questionIdClean}}', ${{level.level}})"
```

Now generates valid JavaScript:
```javascript
onclick="toggleEvidence('Q_ORG_ESTRUT_COMPET_006_001', 0)"
// Properly quoted ^                                    ^
```

**File Modified:** `/question-base/scripts/generate_index_html.py` (lines 918-920, 927)

---

## Issue #2: Nivel Labels Not Showing

### Investigation
Checked the JSON structure - labels ARE present:
```json
{
  "level": 0,
  "label": "Não familiarizada",
  "description": "..."
}
```

### Likely Cause
The HTML was generated BEFORE the fixes were applied. The JavaScript code that reads `level.label` is correct:

```javascript
<div class="level-header">${{level.label || 'Nível ' + level.level}}</div>
```

This should display either:
- The label if present: "Não familiarizada"
- Or fallback: "Nível 0"

### Status
**Should be fixed** after regenerating HTML with the updated script.

---

## Script Updates

### Updated: `generate_json6_html.sh`

**Problem:** Conda wasn't being found in PATH

**Fix:** Added conda initialization:
```bash
source ~/miniconda3/etc/profile.d/conda.sh 2>/dev/null || \
source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || true
```

This tries both miniconda3 and anaconda3 locations.

---

## How to Test

### Step 1: Regenerate HTML

```bash
cd /Users/emadruga/proj/industria-4.0/question-base/scripts
./generate_json6_html.sh
```

**Expected output:**
```
==========================================================================
GENERATING JSON6 HTML VISUALIZATION
==========================================================================

Activating Conda Environment...
--------------------------------------------------------------------------
  ✓ INDUSTRIA4 environment activated

Generating HTML...
--------------------------------------------------------------------------
Reading markdown table from: ../JSON6/metadata/hierarchy_table.md
Loading JSON files from: ../JSON6
Loaded metadata for X questions from JSON files
Extracted 2 questions
Generating interactive HTML...
✅ Interactive HTML saved to: ../JSON6/metadata/index.html
```

### Step 2: Open in Browser

```bash
open /Users/emadruga/proj/industria-4.0/question-base/JSON6/metadata/index.html
```

### Step 3: Visual Testing Checklist

#### Test Expand/Collapse:
- [ ] Click on **Question 1** (Prontidão para Aplicação de Técnicas de Gestão Ágil)
- [ ] Scroll to bottom panel (Níveis de Maturidade)
- [ ] Click "**▶ Sinais de Evidência**" on **Nível 0** (Não familiarizada)
- [ ] **Verify:** Icon changes to ▼
- [ ] **Verify:** Evidence section expands showing 4 categories:
  - 📄 Artefatos (4)
  - 📊 Métricas/KPIs (4)
  - 👁️ Comportamentos Observáveis (5)
  - 💬 Perguntas para Entrevista (5)
- [ ] Click again to collapse
- [ ] **Verify:** Icon changes back to ▶
- [ ] **Verify:** Evidence section collapses

#### Test Level Labels:
- [ ] **Verify:** Each maturity level shows proper label:
  - Level 0: "Não familiarizada"
  - Level 1: "Conhecimento Limitado"
  - Level 2: "Informada"
  - Level 3: "Semi-dependente"
  - Level 4: "Independente"
  - Level 5: "Adaptativa"

#### Test Empty Evidence (Question 2):
- [ ] Click on **Question 2** (Suporte e Comprometimento da Alta Gestão)
- [ ] Scroll to maturity levels
- [ ] Expand any level's evidence
- [ ] **Verify:** Shows "**Ainda não disponível.**" in italic gray text

#### Test Multiple Levels:
- [ ] Expand evidence on Level 0
- [ ] Expand evidence on Level 3
- [ ] **Verify:** Both stay expanded simultaneously
- [ ] **Verify:** Icons show ▼ for both
- [ ] Collapse Level 0
- [ ] **Verify:** Level 3 remains expanded

---

## What to Look For (Problems)

### If Expand/Collapse Still Doesn't Work:
1. Open browser DevTools (F12 or Cmd+Option+I)
2. Go to Console tab
3. Look for JavaScript errors
4. Share the error message

### If Level Labels Are Missing:
1. Open browser DevTools
2. Go to Elements/Inspector tab
3. Find a level card
4. Check if it shows:
   ```html
   <div class="level-header">Não familiarizada</div>
   ```
   vs.
   ```html
   <div class="level-header">Nível 0</div>
   ```

### If Evidence Doesn't Display:
1. Check browser Console for errors
2. Verify the JSON file has `evidence_signals` in each maturity level
3. Check if the data is being loaded properly

---

## Files Modified

| File | Lines Changed | Description |
|------|--------------|-------------|
| `generate_index_html.py` | 918-920, 927 | Fixed onclick handler quoting |
| `generate_json6_html.sh` | 12-14 | Added conda initialization |

---

## Next Steps

1. ✅ Regenerate HTML
2. ✅ Test expand/collapse functionality
3. ✅ Verify level labels display correctly
4. ✅ Test "Ainda não disponível" on Question 2
5. 📝 Report any remaining issues

---

**Status:** Ready for testing
**Last Updated:** 2025-12-28
