# HTML Visualization Updates - JSON7

**Updated**: 2026-01-05
**File**: `generate_index_html.py`

## Changes Made

### 1. Added Expandable "Evidências" Section

Added a collapsible section in the **top panel** (question metadata) that displays:
- 📄 **Artefatos** - List of artifacts for evidence collection
- 📊 **Métricas/KPIs** - List of metrics and key performance indicators  
- 🎯 **Orientações de Amostragem** - Sampling guidance

**Location**: Below "Descrição da Capacidade" in the metadata section

**Behavior**: 
- Click "▶ Evidências" to expand
- Click "▼ Evidências" to collapse
- Only appears if artifacts or metrics are present

### 2. Reduced Bottom Panel Margins

Optimized spacing in the **bottom panel** (maturity levels section) to maximize reading area:

**Changes**:
- `.maturity-levels` margin-top: `2rem` → `0.5rem`
- Question title margin: reduced to `0.25rem`
- "Níveis de Maturidade" heading margins: reduced to `0.25rem` and `0.75rem`

**Result**: More vertical space for maturity level content

### 3. Added JavaScript Toggle Function

New function `toggleQuestionEvidence(questionId)` to handle the collapsible Evidências section independently from the maturity level evidence toggles.

## Visual Layout

```
┌─────────────────────────────────────────┐
│  TOP PANEL (Question Metadata)          │
│  ─────────────────────────────────────  │
│  • Question Title                        │
│  • Autor                                 │
│  • Descrição da Capacidade              │
│  • ▶ Evidências  ← NEW SECTION          │
│    └─ (expandable)                      │
│       ├─ 📄 Artefatos                   │
│       ├─ 📊 Métricas/KPIs               │
│       └─ 🎯 Orientações de Amostragem   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  BOTTOM PANEL (Maturity Levels)         │
│  (More space now - reduced margins)     │
│  ─────────────────────────────────────  │
│  Níveis de Maturidade                   │
│  • Nível 0                              │
│    └─ ▶ Sinais de Evidência            │
│        └─ 👁️ Comportamentos Observáveis │
│  • Nível 1                              │
│  • ...                                  │
└─────────────────────────────────────────┘
```

## Code Changes Summary

**File**: `question-base/scripts/generate_index_html.py`

1. **Lines 1019-1050**: Added expandable Evidências section in metadata
2. **Lines 1131-1147**: Added `toggleQuestionEvidence()` JavaScript function  
3. **Line 510**: Reduced `.maturity-levels` top margin
4. **Lines 1071-1072**: Reduced heading margins in bottom panel

## View the Updated HTML

```
file:///Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/metadata/index.html
```
