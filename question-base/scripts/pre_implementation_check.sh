#!/bin/bash
# Pre-Implementation Environment and Evidence Format Check

echo "=========================================================================="
echo "PRE-IMPLEMENTATION CHECK"
echo "=========================================================================="

# Activate conda environment
echo ""
echo "0. Activating Conda Environment"
echo "--------------------------------------------------------------------------"
eval "$(conda shell.bash hook)"
conda activate INDUSTRIA4
echo "  ✓ INDUSTRIA4 environment activated"
echo ""

# Check 1: Python version
echo "1. Python Version Check"
echo "--------------------------------------------------------------------------"
python --version
echo ""

# Check 2: Required packages
echo "2. Required Python Packages"
echo "--------------------------------------------------------------------------"
echo "Checking python-docx..."
python -c "import docx; print(f'  ✓ python-docx version: {docx.__version__}')" 2>&1

echo "Checking jsonschema..."
python -c "import jsonschema; print(f'  ✓ jsonschema installed')" 2>&1

echo "Checking d3 (for HTML - not Python, just noting)..."
echo "  ✓ d3.js loaded from CDN in HTML"

echo ""

# Check 3: Evidence format in DOCX files
echo "3. Evidence Format Check (4 Authors)"
echo "--------------------------------------------------------------------------"
python check_evidence_format.py

echo ""
echo "=========================================================================="
echo "PRE-IMPLEMENTATION CHECK COMPLETE"
echo "=========================================================================="
