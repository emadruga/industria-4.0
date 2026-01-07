# Extraction Modules - Quick Reference

## Three Specialized Modules

### 1. `extract_evidence.py` - Evidence Sources
Extracts evidence sources from question tables.

```python
from extract_evidence import EvidenceExtractor

extractor = EvidenceExtractor()
evidence = extractor.extract_from_table(table)
```

**Returns**:
```python
{
    'artifacts': ['Certificações...', 'Roadmap...'],
    'metrics': ['% da liderança...', 'Horas de treinamento...'],
    'signals_by_level': {'N0': '...', 'N1': '...'},
    'sampling_guidance': 'Entrevistar 3-5 membros...'
}
```

### 2. `extract_glossary.py` - Glossary Terms
Extracts glossary terms and definitions.

```python
from extract_glossary import GlossaryExtractor

extractor = GlossaryExtractor()
glossary = extractor.extract_from_document(doc)
```

**Returns**:
```python
[
    {'term': 'Scrum', 'definition': 'Framework ágil...'},
    {'term': 'Kanban', 'definition': 'Método visual...'}
]
```

**Command line**:
```bash
python extract_glossary.py file.docx
```

### 3. `extract_references.py` - References
Extracts academic/professional references.

```python
from extract_references import ReferencesExtractor

extractor = ReferencesExtractor()
references = extractor.extract_from_document(doc)
```

**Returns**:
```python
[
    {
        'citation': 'ACATECH. Industrie 4.0...',
        'url': 'https://en.acatech.de/...'
    }
]
```

**Command line**:
```bash
python extract_references.py file.docx
```

## Integrated Usage

All modules are automatically used by the main converter:

```bash
python docx_to_json_converter.py input.docx -o output.json -a "Author"
```

Output includes:
- ✅ Capacity metadata
- ✅ Questions with maturity levels
- ✅ Glossary terms
- ✅ References
- ⚠️ Evidence sources (partial)

## Testing Modules

Test individual modules:
```bash
# Test glossary extraction
python extract_glossary.py "../docs_by_author/EwertonMadruga/Estrutura e Gestão - Ewerton/20251105_checklist_gestao_agil.docx"

# Test references extraction
python extract_references.py "../docs_by_author/WilsonMeloJr/Automação/Shop Floor (D4).docx"
```

## Module Files

```
scripts/
├── extract_evidence.py      # Evidence sources extractor
├── extract_glossary.py      # Glossary terms extractor
├── extract_references.py    # References extractor
└── docx_to_json_converter.py # Main converter (uses all modules)
```

All modules are standalone and can be imported/used independently!
