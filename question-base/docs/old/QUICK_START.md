# Quick Start Guide - Industry 4.0 Question Base

## ✅ Setup Complete!

Your environment is ready:
- ✅ Conda environment `INDUSTRIA4` created
- ✅ All Python dependencies installed
- ✅ JSON schemas defined
- ✅ Conversion tools ready
- ✅ Validation framework operational

## 🎯 Test Results

**First Test:** Successfully converted `20251105_checklist_gestao_agil.docx`
- ✅ Extracted 6 questions
- ✅ All maturity levels captured (6-7 levels per question)
- ⚠️ Minor issue: Dimension field extraction needs refinement

## 🚀 Next Steps

### Option 1: Improve the Parser (Recommended)

The DOCX parser works but needs refinement for dimension extraction. You have two choices:

**A. Fix the parser** - I can improve the table parsing logic to correctly extract "Competência de Liderança" from the first table.

**B. Use the Markdown files** - Since you already have converted MD files, we could create a markdown-to-JSON converter which might be more reliable.

### Option 2: Batch Convert All Files

Once you're satisfied with a single conversion, run:

```bash
conda activate INDUSTRIA4
cd /Users/emadruga/proj/industria-4.0/question-base/scripts

# Convert all DOCX files from templates
python batch_convert.py \
  "../../mdic-suframa/templates" \
  -o ".." \
  -p "**/*.docx"
```

This will:
1. Find all DOCX files in templates
2. Convert each to JSON
3. Organize by Block → Pilar → Dimension
4. Generate `hierarchy.json`
5. Print statistics

### Option 3: Start Manual Review

You can also start reviewing and editing the generated JSON files manually to:
- Correct dimension names
- Merge duplicate questions from different authors
- Improve question wording
- Validate evidence sources

## 📊 Current Status

```
✅ Created: JSON Schemas
✅ Created: DOCX to JSON Converter
✅ Created: Validation Framework
✅ Created: Batch Processing Tool
✅ Tested: Single file conversion works
⚠️  TODO: Refine dimension extraction
⏳ TODO: Process all ~60 DOCX files
⏳ TODO: Review and consolidate questions
```

## 🛠️ Commands Reference

### Activate Environment
```bash
conda activate INDUSTRIA4
```

### Convert Single File
```bash
python scripts/docx_to_json_converter.py \
  "/path/to/file.docx" \
  -o output.json \
  -a "Author Name"
```

### Validate File
```bash
python scripts/validate_questions.py output.json -v
```

### Batch Convert
```bash
python scripts/batch_convert.py input_dir -o output_dir
```

## 📁 Where Files Are

- **Source DOCX**: `/Users/emadruga/proj/industria-4.0/mdic-suframa/templates/`
- **Question Base**: `/Users/emadruga/proj/industria-4.0/question-base/`
- **Schemas**: `/Users/emadruga/proj/industria-4.0/question-base/schema/`
- **Scripts**: `/Users/emadruga/proj/industria-4.0/question-base/scripts/`
- **Test Output**: `/Users/emadruga/proj/industria-4.0/question-base/test_output.json`

## 🤔 What Would You Like To Do?

1. **Improve the parser** - Fix dimension extraction from DOCX tables
2. **Try Markdown converter** - Parse existing MD files instead
3. **Proceed with batch** - Convert all files now (will need manual cleanup)
4. **Review test output** - Check the generated JSON structure
5. **Database planning** - Revisit the MariaDB option

Let me know and I'll proceed!
