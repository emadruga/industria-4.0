#!/bin/bash
# Generate HTML from JSON6 Catalog

echo "=========================================================================="
echo "GENERATING JSON6 HTML VISUALIZATION"
echo "=========================================================================="

# Activate conda environment
echo ""
echo "Activating Conda Environment..."
echo "--------------------------------------------------------------------------"
# Source conda initialization
source ~/miniconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate INDUSTRIA4
echo "  ✓ INDUSTRIA4 environment activated"
echo ""

# Generate HTML
echo "Generating HTML..."
echo "--------------------------------------------------------------------------"
python generate_index_html.py \
  ../JSON6/metadata/hierarchy_table.md \
  -o ../JSON6/metadata/index.html

echo ""
echo "=========================================================================="
echo "GENERATION COMPLETE"
echo "=========================================================================="
echo ""
echo "To view the HTML file, run:"
echo "  open ../JSON6/metadata/index.html"
echo ""
echo "Or navigate to:"
echo "  file:///Users/emadruga/proj/industria-4.0/question-base/JSON6/metadata/index.html"
echo ""
