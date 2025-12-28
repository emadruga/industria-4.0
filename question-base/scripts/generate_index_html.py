#!/usr/bin/env python3
"""
Generate interactive HTML visualization from hierarchy markdown table.

Usage:
    python generate_index_html.py <path_to_hierarchy_table.md>

This will create an index.html file in the same directory as the markdown file.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict


def load_json_files(data_dir: Path) -> Dict[str, dict]:
    """Load all JSON files from the data directory and index by question ID."""
    json_data = {}

    # Find all JSON files in the data directory
    for json_file in data_dir.rglob('*.json'):
        # Skip metadata files
        if 'metadata' in json_file.parts:
            continue

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract capacity info
            capacity_data = data.get('capacity', {})
            metadata = capacity_data.get('metadata', {})

            capacity_info = {
                'description': capacity_data.get('description', ''),
                'author': metadata.get('author', 'Desconhecido'),
                'json_file': str(json_file)
            }

            # Index each question by its ID
            for question in data.get('questions', []):
                q_id = question.get('id', '')
                if q_id:
                    json_data[q_id] = {
                        **capacity_info,
                        'question': question
                    }
        except Exception as e:
            print(f"Warning: Could not load {json_file}: {e}", file=sys.stderr)

    return json_data


def parse_markdown_table(md_path: Path, json_data: Dict[str, dict]) -> list:
    """Parse the markdown table and extract question data, enriching with JSON metadata."""
    questions_data = []

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the table start
    table_started = False
    for line in lines:
        # Skip until we find the table header separator
        if '|-------' in line or '|----' in line:
            table_started = True
            continue

        if not table_started:
            continue

        # Skip empty lines and non-table lines
        if not line.strip() or not line.strip().startswith('|'):
            continue

        # Stop at the end of table marker
        if line.strip() == '---':
            break

        # Parse table row
        cells = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove empty first/last

        if len(cells) >= 6:
            block, pilar, dimension, capacity, question_code, question_title = cells[:6]

            # Extract question code (remove backticks)
            question_code = question_code.strip('`').strip()

            # Skip if this is a header row or separator
            if 'Block' in block or '---' in block or not question_code:
                continue

            # Base question data
            question_data = {
                'block': block.strip(),
                'pilar': pilar.strip(),
                'dimension': dimension.strip(),
                'capacity': capacity.strip(),
                'question_id': question_code,
                'question_number': len(questions_data) + 1,
                'title': question_title.replace('\\|', '|').strip(),
                'text': '',
                'maturity_levels': [],
                'author': 'Desconhecido',
                'capacity_description': ''
            }

            # Enrich with JSON data if available
            if question_code in json_data:
                json_info = json_data[question_code]
                question_data['author'] = json_info['author']
                question_data['capacity_description'] = json_info['description']

                # Get full question data from JSON
                question_json = json_info['question']
                question_data['text'] = question_json.get('text', '')
                question_data['maturity_levels'] = question_json.get('maturity_levels', [])

            questions_data.append(question_data)

    return questions_data


def generate_html(questions_data: list, total_capacities: int = None) -> str:
    """Generate the interactive HTML page."""

    # Count unique capacities
    if total_capacities is None:
        total_capacities = len(set(q['capacity'] for q in questions_data))

    questions_json = json.dumps(questions_data, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa da Maturidade da Indústria 4.0</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            height: 100vh;
            overflow: hidden;
        }}

        .container {{
            display: flex;
            flex-direction: column;
            height: 100vh;
            max-width: 100%;
            margin: 0 auto;
        }}

        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 10;
        }}

        .header h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 0.25rem;
        }}

        .header p {{
            color: #718096;
            font-size: 0.9rem;
        }}

        .main-content {{
            display: flex;
            flex-direction: column;
            flex: 1;
            overflow: hidden;
            gap: 1rem;
            padding: 1rem;
        }}

        .top-row-container {{
            margin-bottom: 1rem;
        }}

        .top-row-header {{
            padding: 1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #f7fafc;
            border-radius: 8px 8px 0 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: background 0.2s;
        }}

        .top-row-header:hover {{
            background: #edf2f7;
        }}

        .top-row-header h3 {{
            margin: 0;
            font-size: 1rem;
            font-weight: 600;
            color: #2d3748;
        }}

        .top-row-toggle-icon {{
            font-size: 1.2rem;
            color: #667eea;
            transition: transform 0.3s;
        }}

        .top-row-toggle-icon.collapsed {{
            transform: rotate(-90deg);
        }}

        .top-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            max-height: 600px;
            overflow-y: auto;
            overflow-x: hidden;
            transition: max-height 0.3s ease-out;
        }}

        .top-row.collapsed {{
            max-height: 0;
            margin: 0;
            overflow: hidden;
        }}

        .chart-section {{
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 1rem 1rem 3rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        #sunburst {{
            width: 100%;
            height: 100%;
        }}

        #sunburst svg {{
            display: block;
        }}

        .question-detail-section {{
            background: rgba(255, 255, 255, 0.98);
            padding: 2rem;
            padding-bottom: 10rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            position: relative;
        }}

        .navigation-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            gap: 1rem;
        }}

        .nav-button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background 0.2s;
        }}

        .nav-button:hover {{
            background: #5568d3;
        }}

        .nav-button:disabled {{
            background: #cbd5e0;
            cursor: not-allowed;
        }}

        .question-counter {{
            color: #718096;
            font-size: 0.9rem;
            font-weight: 500;
        }}

        .filter-section {{
            background: rgba(255, 255, 255, 0.98);
            margin-bottom: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .filter-header {{
            padding: 1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #f7fafc;
            border-radius: 8px 8px 0 0;
            transition: background 0.2s;
        }}

        .filter-header:hover {{
            background: #edf2f7;
        }}

        .filter-header h3 {{
            margin: 0;
            font-size: 1rem;
            font-weight: 600;
            color: #2d3748;
        }}

        .filter-toggle-icon {{
            font-size: 1.2rem;
            color: #667eea;
            transition: transform 0.3s;
        }}

        .filter-toggle-icon.collapsed {{
            transform: rotate(-90deg);
        }}

        .filter-content {{
            padding: 1rem;
            max-height: 500px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }}

        .filter-content.collapsed {{
            max-height: 0;
            padding: 0 1rem;
        }}

        .filter-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }}

        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .filter-label {{
            font-size: 0.75rem;
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
        }}

        .filter-select {{
            padding: 0.4rem 0.6rem;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            font-size: 0.85rem;
            background: white;
            cursor: pointer;
        }}

        .filter-select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .clear-filters {{
            padding: 0.4rem 0.8rem;
            background: #e2e8f0;
            border: none;
            border-radius: 4px;
            font-size: 0.85rem;
            cursor: pointer;
            color: #4a5568;
            font-weight: 500;
        }}

        .clear-filters:hover {{
            background: #cbd5e0;
        }}

        .maturity-section {{
            flex: 0 0 40%;
            background: rgba(255, 255, 255, 0.98);
            padding: 2rem;
            padding-bottom: 10rem;
            overflow-y: auto;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}

        .question-detail {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .breadcrumb {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            font-size: 0.85rem;
            color: #718096;
        }}

        .breadcrumb-item {{
            background: #e2e8f0;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
        }}

        .breadcrumb-separator {{
            color: #cbd5e0;
        }}

        .question-header {{
            margin-bottom: 1.5rem;
        }}

        .question-id {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }}

        .question-title {{
            font-size: 1.6rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 0.75rem;
            line-height: 1.3;
        }}

        .question-text {{
            font-size: 1.1rem;
            color: #4a5568;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }}

        .metadata-section {{
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .metadata-item {{
            margin-bottom: 0.75rem;
        }}

        .metadata-label {{
            font-weight: 600;
            color: #2d3748;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }}

        .metadata-value {{
            color: #4a5568;
            font-size: 0.95rem;
            line-height: 1.5;
        }}

        .author-badge {{
            display: inline-block;
            background: #4facfe;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 600;
        }}

        .maturity-levels {{
            margin-top: 2rem;
        }}

        .maturity-levels h3 {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 1rem;
        }}

        .level-card {{
            background: #f7fafc;
            border-left: 4px solid #667eea;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            border-radius: 4px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .level-card:hover {{
            transform: translateX(4px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        .level-header {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }}

        .level-description {{
            color: #4a5568;
            line-height: 1.6;
            font-size: 0.95rem;
        }}

        .no-question {{
            text-align: center;
            padding: 3rem;
            color: #718096;
        }}

        .no-question-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}

        .sunburst-arc {{
            cursor: pointer;
            transition: opacity 0.2s;
            stroke: white;
            stroke-width: 1px;
        }}

        .sunburst-arc:hover {{
            opacity: 0.85;
            stroke-width: 2px;
        }}


        .loading {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            font-size: 1.2rem;
            color: #718096;
        }}

        .question-detail-section::-webkit-scrollbar,
        .maturity-section::-webkit-scrollbar {{
            width: 8px;
        }}

        .question-detail-section::-webkit-scrollbar-track,
        .maturity-section::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}

        .question-detail-section::-webkit-scrollbar-thumb,
        .maturity-section::-webkit-scrollbar-thumb {{
            background: #cbd5e0;
            border-radius: 4px;
        }}

        .question-detail-section::-webkit-scrollbar-thumb:hover,
        .maturity-section::-webkit-scrollbar-thumb:hover {{
            background: #a0aec0;
        }}

        /* Evidence signals styles */
        .evidence-toggle {{
            margin-top: 1rem;
            padding: 0.75rem;
            background: #e6f2ff;
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background 0.2s;
        }}

        .evidence-toggle:hover {{
            background: #cce5ff;
        }}

        .evidence-toggle span {{
            font-size: 0.9rem;
            color: #667eea;
            font-weight: bold;
        }}

        .evidence-content {{
            margin-top: 0.75rem;
            padding-left: 1rem;
            border-left: 2px solid #667eea;
        }}

        .evidence-category {{
            margin-bottom: 1rem;
        }}

        .evidence-category-title {{
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }}

        .evidence-list {{
            list-style: none;
            padding-left: 0;
        }}

        .evidence-list li {{
            padding: 0.4rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: #4a5568;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .evidence-list li::before {{
            content: "•";
            position: absolute;
            left: 0.5rem;
            color: #667eea;
            font-weight: bold;
        }}

        .no-evidence {{
            color: #a0aec0;
            font-style: italic;
            font-size: 0.9rem;
            padding: 0.5rem 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Explorador do Modelo de Maturidade Indústria 4.0</h1>
            <p>Hierarquia interativa de questões • {len(questions_data)} questões em {total_capacities} capacidades</p>
        </div>

        <div class="main-content">
            <div class="filter-section">
                <div class="filter-header" onclick="toggleFilters()">
                    <h3>Filtros</h3>
                    <span class="filter-toggle-icon" id="filter-toggle-icon">▼</span>
                </div>
                <div class="filter-content" id="filter-content">
                    <div class="filter-row">
                        <div class="filter-group">
                            <label class="filter-label">Bloco</label>
                            <select id="filter-block" class="filter-select" onchange="applyFilters()">
                                <option value="">Todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label class="filter-label">Pilar</label>
                            <select id="filter-pilar" class="filter-select" onchange="applyFilters()">
                                <option value="">Todos</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label class="filter-label">Dimensão</label>
                            <select id="filter-dimension" class="filter-select" onchange="applyFilters()">
                                <option value="">Todas</option>
                            </select>
                        </div>
                        <div class="filter-group">
                            <label class="filter-label">Autor</label>
                            <select id="filter-author" class="filter-select" onchange="applyFilters()">
                                <option value="">Todos</option>
                            </select>
                        </div>
                    </div>
                    <button class="clear-filters" onclick="clearFilters()">Limpar Filtros</button>
                </div>
            </div>

            <div class="top-row-container">
                <div class="top-row-header" onclick="toggleTopRow()">
                    <h3>Visualização e Detalhes</h3>
                    <span class="top-row-toggle-icon" id="top-row-toggle-icon">▼</span>
                </div>
                <div class="top-row" id="top-row">
                    <div class="chart-section">
                        <div id="sunburst"></div>
                    </div>

                    <div class="question-detail-section">
                        <div id="question-detail" class="question-detail">
                            <div class="loading">Clique no gráfico para explorar as questões...</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="maturity-section">
                <div id="maturity-levels">
                    <div class="no-question">
                        <div class="no-question-icon">📊</div>
                        <p>Selecione uma questão para ver os níveis de maturidade</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const questionsData = {questions_json};
        let currentQuestionIndex = -1;
        let activeFilters = {{
            block: '',
            pilar: '',
            dimension: '',
            author: ''
        }};

        // Populate filter dropdowns
        function populateFilters() {{
            const blocks = [...new Set(questionsData.map(q => q.block))].sort();
            const pilars = [...new Set(questionsData.map(q => q.pilar))].sort();
            const dimensions = [...new Set(questionsData.map(q => q.dimension))].sort();
            const authors = [...new Set(questionsData.map(q => q.author))].sort();

            const blockSelect = document.getElementById('filter-block');
            const pilarSelect = document.getElementById('filter-pilar');
            const dimensionSelect = document.getElementById('filter-dimension');
            const authorSelect = document.getElementById('filter-author');

            blocks.forEach(block => {{
                const option = document.createElement('option');
                option.value = block;
                option.textContent = block;
                blockSelect.appendChild(option);
            }});

            pilars.forEach(pilar => {{
                const option = document.createElement('option');
                option.value = pilar;
                option.textContent = pilar;
                pilarSelect.appendChild(option);
            }});

            dimensions.forEach(dimension => {{
                const option = document.createElement('option');
                option.value = dimension;
                option.textContent = dimension;
                dimensionSelect.appendChild(option);
            }});

            authors.forEach(author => {{
                const option = document.createElement('option');
                option.value = author;
                option.textContent = author;
                authorSelect.appendChild(option);
            }});
        }}

        // Toggle filter section expand/collapse
        function toggleFilters() {{
            const content = document.getElementById('filter-content');
            const icon = document.getElementById('filter-toggle-icon');
            content.classList.toggle('collapsed');
            icon.classList.toggle('collapsed');
        }}

        // Toggle top row section expand/collapse
        function toggleTopRow() {{
            const content = document.getElementById('top-row');
            const icon = document.getElementById('top-row-toggle-icon');
            content.classList.toggle('collapsed');
            icon.classList.toggle('collapsed');
        }}

        // Apply filters
        function applyFilters() {{
            activeFilters.block = document.getElementById('filter-block').value;
            activeFilters.pilar = document.getElementById('filter-pilar').value;
            activeFilters.dimension = document.getElementById('filter-dimension').value;
            activeFilters.author = document.getElementById('filter-author').value;

            updateChartWithFilters();
        }}

        // Clear all filters
        function clearFilters() {{
            document.getElementById('filter-block').value = '';
            document.getElementById('filter-pilar').value = '';
            document.getElementById('filter-dimension').value = '';
            document.getElementById('filter-author').value = '';
            activeFilters = {{ block: '', pilar: '', dimension: '', author: '' }};
            updateChartWithFilters();
        }}

        // Check if question matches filters
        function matchesFilters(questionData) {{
            if (activeFilters.block && questionData.block !== activeFilters.block) return false;
            if (activeFilters.pilar && questionData.pilar !== activeFilters.pilar) return false;
            if (activeFilters.dimension && questionData.dimension !== activeFilters.dimension) return false;
            if (activeFilters.author && questionData.author !== activeFilters.author) return false;
            return true;
        }}

        // Update chart colors based on filters
        function updateChartWithFilters() {{
            const greenHue = '#43e97b';  // Normal green for questions
            const darkGreenHue = '#2d5f44';  // Dark green for filtered out

            d3.selectAll('.sunburst-arc')
                .attr('fill', d => {{
                    // Check if this is a question
                    if (d.data.type === 'question' && d.data.data) {{
                        const matches = matchesFilters(d.data.data);
                        return matches ? greenHue : darkGreenHue;
                    }}
                    // For non-question nodes, use standard colors
                    const color = d3.scaleOrdinal()
                        .domain(['block', 'pilar', 'dimension', 'capacity', 'question'])
                        .range(['#667eea', '#764ba2', '#f093fb', '#4facfe', greenHue]);
                    return color(d.data.type || 'root');
                }});
        }}

        // Helper function to sort children by question ID
        function sortByQuestionId(children) {{
            return children.sort((a, b) => {{
                // For questions, use the question_id from data
                if (a.type === 'question' && b.type === 'question') {{
                    const idA = a.data.question_id || '';
                    const idB = b.data.question_id || '';
                    return idA.localeCompare(idB);
                }}
                // For other types, sort by name
                return (a.name || '').localeCompare(b.name || '');
            }});
        }}

        // Build hierarchy for sunburst
        function buildHierarchy(data) {{
            const root = {{ name: "Industry 4.0", children: [] }};
            const blocks = {{}};

            data.forEach(q => {{
                if (!blocks[q.block]) {{
                    blocks[q.block] = {{ name: q.block, children: [], type: 'block' }};
                }}

                let block = blocks[q.block];
                let pilar = block.children.find(p => p.name === q.pilar);
                if (!pilar) {{
                    pilar = {{ name: q.pilar, children: [], type: 'pilar' }};
                    block.children.push(pilar);
                }}

                let dimension = pilar.children.find(d => d.name === q.dimension);
                if (!dimension) {{
                    dimension = {{ name: q.dimension, children: [], type: 'dimension' }};
                    pilar.children.push(dimension);
                }}

                let capacity = dimension.children.find(c => c.name === q.capacity);
                if (!capacity) {{
                    capacity = {{ name: q.capacity, children: [], type: 'capacity' }};
                    dimension.children.push(capacity);
                }}

                capacity.children.push({{
                    name: q.title || `Q${{q.question_number}}`,
                    type: 'question',
                    data: q
                }});
            }});

            // Sort all levels of the hierarchy
            root.children = Object.values(blocks);
            sortByQuestionId(root.children);

            root.children.forEach(block => {{
                sortByQuestionId(block.children);
                block.children.forEach(pilar => {{
                    sortByQuestionId(pilar.children);
                    pilar.children.forEach(dimension => {{
                        sortByQuestionId(dimension.children);
                        dimension.children.forEach(capacity => {{
                            sortByQuestionId(capacity.children);
                        }});
                    }});
                }});
            }});

            return root;
        }}

        // Navigate to previous/next question
        function navigateQuestion(direction) {{
            if (direction === 'prev') {{
                if (currentQuestionIndex > 0) {{
                    currentQuestionIndex--;
                }} else {{
                    // Wrap around to last question
                    currentQuestionIndex = questionsData.length - 1;
                }}
            }} else if (direction === 'next') {{
                if (currentQuestionIndex < questionsData.length - 1) {{
                    currentQuestionIndex++;
                }} else {{
                    // Wrap around to first question
                    currentQuestionIndex = 0;
                }}
            }}
            displayQuestion(questionsData[currentQuestionIndex]);
        }}

        // Display question details
        function displayQuestion(questionData) {{
            const questionContainer = document.getElementById('question-detail');
            const maturityContainer = document.getElementById('maturity-levels');

            if (!questionData) {{
                currentQuestionIndex = -1;
                questionContainer.innerHTML = `
                    <div class="no-question">
                        <div class="no-question-icon">📊</div>
                        <p>Clique em uma questão no gráfico para ver os detalhes</p>
                    </div>
                `;
                maturityContainer.innerHTML = `
                    <div class="no-question">
                        <div class="no-question-icon">📊</div>
                        <p>Selecione uma questão para ver os níveis de maturidade</p>
                    </div>
                `;
                return;
            }}

            // Update current index (always refresh when displaying a question)
            currentQuestionIndex = questionsData.findIndex(q => q.question_id === questionData.question_id);

            // Top-right panel: Question details (without maturity levels)
            questionContainer.innerHTML = `
                <div class="navigation-controls">
                    <button class="nav-button" onclick="navigateQuestion('prev')">
                        ← Anterior
                    </button>
                    <div class="question-counter">
                        ${{currentQuestionIndex + 1}} / ${{questionsData.length}}
                    </div>
                    <button class="nav-button" onclick="navigateQuestion('next')">
                        Próxima →
                    </button>
                </div>

                <div class="breadcrumb">
                    <span class="breadcrumb-item">${{questionData.block}}</span>
                    <span class="breadcrumb-separator">→</span>
                    <span class="breadcrumb-item">${{questionData.pilar}}</span>
                    <span class="breadcrumb-separator">→</span>
                    <span class="breadcrumb-item">${{questionData.dimension}}</span>
                    <span class="breadcrumb-separator">→</span>
                    <span class="breadcrumb-item">${{questionData.capacity}}</span>
                </div>

                <div class="question-header">
                    <div class="question-id">${{questionData.question_id}}</div>
                    <h2 class="question-title">${{questionData.title}}</h2>
                    ${{questionData.text ? `<p class="question-text">${{questionData.text}}</p>` : ''}}
                </div>

                <div class="metadata-section">
                    <div class="metadata-item">
                        <div class="metadata-label">Autor</div>
                        <div class="metadata-value">
                            <span class="author-badge">${{questionData.author}}</span>
                        </div>
                    </div>
                    ${{questionData.capacity_description ? `
                        <div class="metadata-item">
                            <div class="metadata-label">Descrição da Capacidade</div>
                            <div class="metadata-value">${{questionData.capacity_description}}</div>
                        </div>
                    ` : ''}}
                </div>
            `;

            // Bottom panel: Maturity levels only
            const levels = questionData.maturity_levels || [];
            if (levels.length > 0) {{
                const questionIdClean = questionData.question_id.replace(/[^a-zA-Z0-9]/g, '_');
                let maturityHTML = '<div class="maturity-levels">';

                // Add hierarchy breadcrumb (same style as metadata panel)
                maturityHTML += '<div class="breadcrumb">';
                maturityHTML += '<span class="breadcrumb-item">' + questionData.block + '</span>';
                maturityHTML += '<span class="breadcrumb-separator">→</span>';
                maturityHTML += '<span class="breadcrumb-item">' + questionData.pilar + '</span>';
                maturityHTML += '<span class="breadcrumb-separator">→</span>';
                maturityHTML += '<span class="breadcrumb-item">' + questionData.dimension + '</span>';
                maturityHTML += '<span class="breadcrumb-separator">→</span>';
                maturityHTML += '<span class="breadcrumb-item">' + questionData.capacity + '</span>';
                maturityHTML += '</div>';

                maturityHTML += '<h3 style="margin-bottom: 0.5rem;">Questão: ' + (questionData.text || questionData.title || '') + '</h3>';
                maturityHTML += '<h4 style="color: #667eea; margin-top: 0.5rem; margin-bottom: 1.5rem; font-size: 1.1rem;">Níveis de Maturidade</h4>';

                levels.forEach((level, index) => {{
                    const hasEvidence = level.evidence_signals && (
                        (level.evidence_signals.artifacts && level.evidence_signals.artifacts.length > 0) ||
                        (level.evidence_signals.metrics && level.evidence_signals.metrics.length > 0) ||
                        (level.evidence_signals.observable_behaviors && level.evidence_signals.observable_behaviors.length > 0) ||
                        (level.evidence_signals.interview_questions && level.evidence_signals.interview_questions.length > 0)
                    );

                    const evidenceId = 'evidence-' + questionIdClean + '-' + level.level;
                    const iconId = 'evidence-icon-' + questionIdClean + '-' + level.level;
                    const levelLabel = level.label || ('Nível ' + level.level);

                    maturityHTML += '<div class="level-card">';
                    maturityHTML += '<div class="level-header">' + levelLabel + '</div>';
                    maturityHTML += '<div class="level-description">' + level.description + '</div>';

                    maturityHTML += '<div class="evidence-toggle" onclick="toggleEvidence(\\\'' + questionIdClean + '\\\', ' + level.level + ')">';
                    maturityHTML += '<span id="' + iconId + '">▶</span>';
                    maturityHTML += '<strong>Sinais de Evidência</strong>';
                    maturityHTML += '</div>';

                    maturityHTML += '<div id="' + evidenceId + '" class="evidence-content" style="display: none;">';
                    if (hasEvidence) {{
                        maturityHTML += renderEvidenceSection(level.evidence_signals);
                    }} else {{
                        maturityHTML += '<p class="no-evidence">Ainda não disponível.</p>';
                    }}
                    maturityHTML += '</div>';

                    maturityHTML += '</div>';
                }});

                maturityHTML += '</div>';
                maturityContainer.innerHTML = maturityHTML;
            }} else {{
                maturityContainer.innerHTML = '<div class="no-question"><p>Nenhum nível de maturidade definido para esta questão</p></div>';
            }}

            // Highlight current question in sunburst
            highlightQuestionInChart(questionData.question_id);
        }}

        // Toggle evidence section visibility
        function toggleEvidence(questionIdClean, levelId) {{
            const contentId = `evidence-${{questionIdClean}}-${{levelId}}`;
            const iconId = `evidence-icon-${{questionIdClean}}-${{levelId}}`;
            const content = document.getElementById(contentId);
            const icon = document.getElementById(iconId);

            if (content && icon) {{
                if (content.style.display === 'none') {{
                    content.style.display = 'block';
                    icon.textContent = '▼';
                }} else {{
                    content.style.display = 'none';
                    icon.textContent = '▶';
                }}
            }}
        }}

        // Render evidence section
        function renderEvidenceSection(signals) {{
            let html = '';

            if (signals.artifacts && signals.artifacts.length > 0) {{
                html += `
                    <div class="evidence-category">
                        <div class="evidence-category-title">📄 Artefatos (${{signals.artifacts.length}})</div>
                        <ul class="evidence-list">
                            ${{signals.artifacts.map(item => `<li>${{item}}</li>`).join('')}}
                        </ul>
                    </div>
                `;
            }}

            if (signals.metrics && signals.metrics.length > 0) {{
                html += `
                    <div class="evidence-category">
                        <div class="evidence-category-title">📊 Métricas/KPIs (${{signals.metrics.length}})</div>
                        <ul class="evidence-list">
                            ${{signals.metrics.map(item => `<li>${{item}}</li>`).join('')}}
                        </ul>
                    </div>
                `;
            }}

            if (signals.observable_behaviors && signals.observable_behaviors.length > 0) {{
                html += `
                    <div class="evidence-category">
                        <div class="evidence-category-title">👁️ Comportamentos Observáveis (${{signals.observable_behaviors.length}})</div>
                        <ul class="evidence-list">
                            ${{signals.observable_behaviors.map(item => `<li>${{item}}</li>`).join('')}}
                        </ul>
                    </div>
                `;
            }}

            if (signals.interview_questions && signals.interview_questions.length > 0) {{
                html += `
                    <div class="evidence-category">
                        <div class="evidence-category-title">💬 Perguntas para Entrevista (${{signals.interview_questions.length}})</div>
                        <ul class="evidence-list">
                            ${{signals.interview_questions.map(item => `<li>${{item}}</li>`).join('')}}
                        </ul>
                    </div>
                `;
            }}

            return html || '<p class="no-evidence">Nenhuma evidência disponível.</p>';
        }}

        // Highlight the current question in the sunburst chart
        function highlightQuestionInChart(questionId) {{
            const capacityBlue = '#4facfe';
            const greenHue = '#43e97b';
            const darkGreenHue = '#2d5f44';

            d3.selectAll('.sunburst-arc')
                .attr('fill', d => {{
                    // Check if this is the current question
                    if (d.data.type === 'question' && d.data.data && d.data.data.question_id === questionId) {{
                        return capacityBlue;
                    }}
                    // For questions, apply filter-based coloring
                    if (d.data.type === 'question' && d.data.data) {{
                        const matches = matchesFilters(d.data.data);
                        return matches ? greenHue : darkGreenHue;
                    }}
                    // Otherwise use the standard color
                    const color = d3.scaleOrdinal()
                        .domain(['block', 'pilar', 'dimension', 'capacity', 'question'])
                        .range(['#667eea', '#764ba2', '#f093fb', '#4facfe', greenHue]);
                    return color(d.data.type || 'root');
                }});
        }}

        // Create sunburst chart
        function createSunburst() {{
            const width = 300;
            const height = 300;
            const radius = Math.min(width, height) / 2;

            const color = d3.scaleOrdinal()
                .domain(['block', 'pilar', 'dimension', 'capacity', 'question'])
                .range(['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']);

            const hierarchy = buildHierarchy(questionsData);
            const root = d3.hierarchy(hierarchy)
                .sum(d => d.type === 'question' ? 1 : 0);

            const partition = d3.partition()
                .size([2 * Math.PI, radius]);

            partition(root);

            const arc = d3.arc()
                .startAngle(d => d.x0)
                .endAngle(d => d.x1)
                .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
                .padRadius(radius / 2)
                .innerRadius(d => d.y0)
                .outerRadius(d => d.y1 - 1);

            const svg = d3.select('#sunburst')
                .append('svg')
                .attr('width', width)
                .attr('height', height)
                .attr('viewBox', `0 0 ${{width}} ${{height}}`)
                .style('font', '12px sans-serif');

            const g = svg.append('g')
                .attr('transform', `translate(${{radius}},${{radius}})`);

            g.selectAll('path')
                .data(root.descendants())
                .join('path')
                .attr('class', 'sunburst-arc')
                .attr('fill', d => color(d.data.type || 'root'))
                .attr('d', arc)
                .on('click', (event, d) => {{
                    if (d.data.type === 'question' && d.data.data) {{
                        displayQuestion(d.data.data);
                    }}
                }})
                .append('title')
                .text(d => `${{d.ancestors().map(a => a.data.name).reverse().join(' → ')}}\\n${{d.value}} question(s)`);

            // No text labels on the chart - tooltips only
        }}

        // Initialize
        window.addEventListener('DOMContentLoaded', () => {{
            populateFilters();
            createSunburst();

            // Show a random question on load
            if (questionsData.length > 0) {{
                const randomIndex = Math.floor(Math.random() * questionsData.length);
                displayQuestion(questionsData[randomIndex]);
            }}
        }});
    </script>
</body>
</html>"""

    return html


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Generate interactive HTML from hierarchy markdown table',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_index_html.py metadata/hierarchy_table.md
  python generate_index_html.py ../data/metadata/hierarchy_table.md
        """
    )
    parser.add_argument('markdown_file', help='Path to hierarchy_table.md file')
    parser.add_argument('-o', '--output', help='Output HTML file path (default: index.html in same directory)')

    args = parser.parse_args()

    # Validate input file
    md_path = Path(args.markdown_file)
    if not md_path.exists():
        print(f"Error: File not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = md_path.parent / 'index.html'

    print(f"Reading markdown table from: {md_path}")

    # Find data directory (sibling to metadata folder)
    data_dir = md_path.parent.parent  # Go up from metadata to data directory
    print(f"Loading JSON files from: {data_dir}")

    # Load all JSON files
    try:
        json_data = load_json_files(data_dir)
        print(f"Loaded metadata for {len(json_data)} questions from JSON files")
    except Exception as e:
        print(f"Warning: Could not load JSON files: {e}", file=sys.stderr)
        json_data = {}

    # Parse markdown table
    try:
        questions_data = parse_markdown_table(md_path, json_data)
        print(f"Extracted {len(questions_data)} questions")
    except Exception as e:
        print(f"Error parsing markdown: {e}", file=sys.stderr)
        sys.exit(1)

    if not questions_data:
        print("Warning: No questions found in markdown file", file=sys.stderr)
        sys.exit(1)

    # Generate HTML
    print("Generating interactive HTML...")
    html = generate_html(questions_data)

    # Save HTML
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Interactive HTML saved to: {output_path}")
        print(f"\nOpen the file in your browser:")
        print(f"  file://{output_path.absolute()}")
    except Exception as e:
        print(f"Error saving HTML: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
