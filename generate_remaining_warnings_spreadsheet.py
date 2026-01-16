#!/usr/bin/env python3
"""
Generate Excel spreadsheet of remaining warnings (MATURITY_LEVEL_DESCRIPTION and OBSERVABLE_BEHAVIORS)
"""

import pandas as pd
import json
from pathlib import Path

# Define the data structure for warnings
warnings_data = []

# Read the vertical_(d1)_-_primário.json file to get the actual state
vertical_file = Path('/Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/data/Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json')
with open(vertical_file, 'r', encoding='utf-8') as f:
    vertical_data = json.load(f)

# Read the análise_de_dados_automatizada.json file
analise_file = Path('/Users/emadruga/proj/industria-4.0/question-base/JSON7_20260105_164046/data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json')
with open(analise_file, 'r', encoding='utf-8') as f:
    analise_data = json.load(f)

# Extract author from metadata
vertical_author = vertical_data['capacity']['metadata']['author']
analise_author = analise_data['capacity']['metadata']['author']

# MATURITY_LEVEL_DESCRIPTION warnings - vertical_(d1)_-_primário.json
# Question 1 (Q-PROC-OPERAÇ-VERTIC-016-001), levels 5 and 6
q1 = vertical_data['questions'][0]
warnings_data.append({
    'Question ID': q1['id'],
    'JSON File': 'data/Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json',
    'Author': vertical_author,
    'Label Maturity Level': 'Nível 5',
    'What Description Is Now': q1['maturity_levels'][5]['description'] if q1['maturity_levels'][5]['description'] else '(empty)',
    'Suggestion for Description': 'Add a meaningful description for level 5 that explains the integration capabilities at this maturity level. Consider describing advanced predictive analytics, real-time synchronization, or autonomous optimization between shop floor and enterprise systems.'
})

warnings_data.append({
    'Question ID': q1['id'],
    'JSON File': 'data/Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json',
    'Author': vertical_author,
    'Label Maturity Level': 'Nível 6',
    'What Description Is Now': q1['maturity_levels'][6]['description'] if q1['maturity_levels'][6]['description'] else '(empty)',
    'Suggestion for Description': 'Add a meaningful description for level 6 that explains the highest level of vertical integration. Consider describing fully autonomous, self-optimizing systems with complete digital integration across all layers from field devices to enterprise planning.'
})

# Question 2 (Q-PROC-OPERAÇ-VERTIC-016-002), levels 5 and 6
q2 = vertical_data['questions'][1]
warnings_data.append({
    'Question ID': q2['id'],
    'JSON File': 'data/Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json',
    'Author': vertical_author,
    'Label Maturity Level': 'Nível 5',
    'What Description Is Now': q2['maturity_levels'][5]['description'] if q2['maturity_levels'][5]['description'] else '(empty)',
    'Suggestion for Description': 'Add a meaningful description for level 5 that explains real-time synchronization capabilities between operation and planning. Consider describing predictive planning adjustments based on real-time operational data.'
})

warnings_data.append({
    'Question ID': q2['id'],
    'JSON File': 'data/Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json',
    'Author': vertical_author,
    'Label Maturity Level': 'Nível 6',
    'What Description Is Now': q2['maturity_levels'][6]['description'] if q2['maturity_levels'][6]['description'] else '(empty)',
    'Suggestion for Description': 'Add a meaningful description for level 6 that explains autonomous synchronization. Consider describing self-optimizing systems that automatically adjust planning and execution without human intervention.'
})

# OBSERVABLE_BEHAVIORS warnings - análise_de_dados_automatizada.json
# Question 2 (Q-TEC-INTELI-CORPOR-002-002), level 0
q_analise_2 = analise_data['questions'][1]
behaviors_2_0 = q_analise_2['maturity_levels'][0]['evidence_signals']['observable_behaviors']
warnings_data.append({
    'Question ID': q_analise_2['id'],
    'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
    'Author': analise_author,
    'Label Maturity Level': 'Nível 0',
    'What Description Is Now': f'{len(behaviors_2_0)} observable behaviors' if behaviors_2_0 else '(empty list)',
    'Suggestion for Description': 'Add observable behaviors for level 0. Examples: "Gerente não consegue saber custo real do produto em produção", "Dados de produção e financeiro são completamente isolados", "Decisões são tomadas sem dados integrados"'
})

# Question 3 (Q-TEC-INTELI-CORPOR-002-003), level 0
q_analise_3 = analise_data['questions'][2]
behaviors_3_0 = q_analise_3['maturity_levels'][0]['evidence_signals']['observable_behaviors']
warnings_data.append({
    'Question ID': q_analise_3['id'],
    'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
    'Author': analise_author,
    'Label Maturity Level': 'Nível 0',
    'What Description Is Now': f'{len(behaviors_3_0)} observable behaviors' if behaviors_3_0 else '(empty list)',
    'Suggestion for Description': 'Add observable behaviors for level 0. Examples: "Não há sistema de análise de dados", "Todas as decisões são baseadas em intuição e experiência", "Não existem ferramentas de BI ou analytics"'
})

# Question 4 (Q-TEC-INTELI-CORPOR-002-004), level 0
q_analise_4 = analise_data['questions'][3]
behaviors_4_0 = q_analise_4['maturity_levels'][0]['evidence_signals']['observable_behaviors']
warnings_data.append({
    'Question ID': q_analise_4['id'],
    'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
    'Author': analise_author,
    'Label Maturity Level': 'Nível 0',
    'What Description Is Now': f'{len(behaviors_4_0)} observable behaviors' if behaviors_4_0 else '(empty list)',
    'Suggestion for Description': 'Add observable behaviors for level 0. Examples: "Relatórios são gerados manualmente quando solicitados", "Pode levar dias ou semanas para obter informações sobre problemas", "Não há análise em tempo real"'
})

# Create DataFrame
df = pd.DataFrame(warnings_data)

# Reorder columns as requested
df = df[['Question ID', 'JSON File', 'Author', 'Label Maturity Level', 'What Description Is Now', 'Suggestion for Description']]

# Sort by JSON File, then by Question ID
df = df.sort_values(['JSON File', 'Question ID'])

# Save to Excel
output_file = '/Users/emadruga/proj/industria-4.0/remaining_warnings_summary.xlsx'
df.to_excel(output_file, index=False, sheet_name='Remaining Warnings')

print(f"Excel file created: {output_file}")
print(f"Total warnings: {len(df)}")
print(f"\nWarnings by type:")
print(f"  - MATURITY_LEVEL_DESCRIPTION: 4")
print(f"  - OBSERVABLE_BEHAVIORS: 3")
