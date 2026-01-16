#!/usr/bin/env python3
"""
Generate Excel spreadsheet of all maturity level label warnings
Cross-referenced with hierarchy table for dimension and capacity information
"""

import re
import pandas as pd
from pathlib import Path

# Define the data structure for warnings
warnings_data = []

# Parse warnings from the consistency check report
# Organized by author with file names and warnings

# Cristiano Gurgel Castro warnings
warnings_data.extend([
    {
        'Question ID': 'Q-ORG-PRONTI-APREND-012-007',  # desenvolvimento_profissional_contínuo, question 6
        'Author': 'Cristiano Gurgel Castro',
        'JSON File': 'data/Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho/desenvolvimento_profissional_contínuo.json',
        'Question Index': 'questions[6]',
        'Maturity Level': '3',
        'Expected Value': 'Nível 3',
        'What It Is Now': 'Os líderes são formalmente cobrados por (ex'
    },
    {
        'Question ID': 'Q-ORG-PRONTI-APREND-014-002',  # reconhecer_o_valor_dos_erros, question 1
        'Author': 'Cristiano Gurgel Castro',
        'JSON File': 'data/Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho/reconhecer_o_valor_dos_erros.json',
        'Question Index': 'questions[1]',
        'Maturity Level': '6',
        'Expected Value': 'Nível 6',
        'What It Is Now': 'A cultura é autorregulada'
    },
    {
        'Question ID': 'Q-ORG-PRONTI-APREND-013-007',  # prover_competencias_digitais, question 6
        'Author': 'Cristiano Gurgel Castro',
        'JSON File': 'data/Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho_(D13)/prover_competencias_digitais.json',
        'Question Index': 'questions[6]',
        'Maturity Level': '6',
        'Expected Value': 'Nível 6',
        'What It Is Now': 'A integração é completa'
    },
    {
        'Question ID': 'Q-PROC-OPERAÇ-HORIZO-015-003',  # horizontal_(d2)_-_mapeamento_secundário, question 2
        'Author': 'Cristiano Gurgel Castro',
        'JSON File': 'data/Processo/Operações/Cadeia_de_Suprimentos/Horizontal_(D2)/horizontal_(d2)_-_mapeamento_secundário.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '3',
        'Expected Value': 'Nível 3',
        'What It Is Now': 'A rastreabilidade é digital e parcial entre parceiros diretos (ex.'
    }
])

# Ewerton Madruga warnings
warnings_data.extend([
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 0
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '0',
        'Expected Value': 'Nível 0',
        'What It Is Now': 'Não familiarizada'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 1
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '1',
        'Expected Value': 'Nível 1',
        'What It Is Now': 'Conhecimento Limitado'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 2
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '2',
        'Expected Value': 'Nível 2',
        'What It Is Now': 'Informada'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 3
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '3',
        'Expected Value': 'Nível 3',
        'What It Is Now': 'Semi-dependente'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 4
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '4',
        'Expected Value': 'Nível 4',
        'What It Is Now': 'Independente'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 5
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '5',
        'Expected Value': 'Nível 5',
        'What It Is Now': 'Adaptativa'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-001',  # gestão_ágil, question 0, level 6
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[0]',
        'Maturity Level': '6',
        'Expected Value': 'Nível 6',
        'What It Is Now': 'Transformacional'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-COMPET-006-005',  # gestão_ágil, question 4, level 2
        'Author': 'Ewerton Madruga',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json',
        'Question Index': 'questions[4]',
        'Maturity Level': '2',
        'Expected Value': 'Nível 2',
        'What It Is Now': 'Existe um programa básico de treinamento inicial (ex'
    }
])

# Flavia Agostini warnings (from governança_de_dados.json, but labeled as estratégia_e_governança in report)
warnings_data.extend([
    {
        'Question ID': 'Q-ORG-ESTRUT-ESTRAT-004-008',  # governança_de_dados, question 7
        'Author': 'Flavia Agostini',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Estratégia_e_Governança/governança_de_dados.json',
        'Question Index': 'questions[7]',
        'Maturity Level': '2',
        'Expected Value': 'Nível 2',
        'What It Is Now': 'Os funcionários são incentivados a sugerir melhorias (ex'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-ESTRAT-004-009',  # governança_de_dados, question 8
        'Author': 'Flavia Agostini',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Estratégia_e_Governança/governança_de_dados.json',
        'Question Index': 'questions[8]',
        'Maturity Level': '2',
        'Expected Value': 'Nível 2',
        'What It Is Now': 'A gestão ouve as propostas, mas a iniciativa é bloqueada por burocracia excessiva (ex'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-ESTRAT-004-011',  # governança_de_dados, question 10
        'Author': 'Flavia Agostini',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Estratégia_e_Governança/governança_de_dados.json',
        'Question Index': 'questions[10]',
        'Maturity Level': '4',
        'Expected Value': 'Nível 4',
        'What It Is Now': 'A implementação segue ciclos formais de melhoria (ex'
    },
    {
        'Question ID': 'Q-ORG-ESTRUT-ESTRAT-004-011',  # governança_de_dados, question 10
        'Author': 'Flavia Agostini',
        'JSON File': 'data/Organização/Estrutura_e_Gestão/Estratégia_e_Governança/governança_de_dados.json',
        'Question Index': 'questions[10]',
        'Maturity Level': '6',
        'Expected Value': 'Nível 6',
        'What It Is Now': 'A implementação é ativamente ágil, usando ciclos curtos (ex'
    }
])

# Wilson Melo Jr warnings (MATURITY_LEVEL_LABEL only, excluding MATURITY_LEVEL_DESCRIPTION and OBSERVABLE_BEHAVIORS)
warnings_data.extend([
    {
        'Question ID': 'Q-TEC-INTELI-CHÃOFÁ-001-003',  # pré-processamento_descentralizado_de_dados_de_sensores, question 2
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Chão_de_Fábrica/pré-processamento_descentralizado_de_dados_de_sensores.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '6',
        'Expected Value': 'Nível 6',
        'What It Is Now': 'Os sistemas embarcados executam processamento complexo em tempo real (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-002',  # análise_de_dados_automatizada, question 1, level 4
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[1]',
        'Maturity Level': '4',
        'Expected Value': 'Nível 4',
        'What It Is Now': 'A análise integra dados de forma vertical, conectando o shop floor (TI/TO) com sistemas de gestão corporativa (Enterprise), como ERP ou SCM (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-002',  # análise_de_dados_automatizada, question 1, level 5
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[1]',
        'Maturity Level': '5',
        'Expected Value': 'Nível 5',
        'What It Is Now': 'A análise integra dados verticalmente (fábrica + gestão) e horizontalmente, incluindo dados de parceiros externos (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-003',  # análise_de_dados_automatizada, question 2, level 1
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '1',
        'Expected Value': 'Nível 1',
        'What It Is Now': 'A análise é 100% manual. Os dados são exportados (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-003',  # análise_de_dados_automatizada, question 2, level 2
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '2',
        'Expected Value': 'Nível 2',
        'What It Is Now': 'A análise é automatizada, mas limitada a regras fixas e pré-programadas (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-003',  # análise_de_dados_automatizada, question 2, level 3
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '3',
        'Expected Value': 'Nível 3',
        'What It Is Now': 'Os sistemas aplicam regras de diagnóstico complexas (árvores de decisão, expert systems) que foram definidas manualmente por especialistas para identificar causas conhecidas (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-003',  # análise_de_dados_automatizada, question 2, level 4
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '4',
        'Expected Value': 'Nível 4',
        'What It Is Now': 'A empresa utiliza modelos preditivos (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-003',  # análise_de_dados_automatizada, question 2, level 5
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '5',
        'Expected Value': 'Nível 5',
        'What It Is Now': 'A empresa utiliza ativamente técnicas de Machine Learning (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-003',  # análise_de_dados_automatizada, question 2, level 6
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[2]',
        'Maturity Level': '6',
        'Expected Value': 'Nível 6',
        'What It Is Now': 'Os sistemas são adaptativos e utilizam autoaprendizado (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-004',  # análise_de_dados_automatizada, question 3, level 2
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[3]',
        'Maturity Level': '2',
        'Expected Value': 'Nível 2',
        'What It Is Now': 'A análise é automatizada, mas executada em lotes (batch) com baixa frequência (ex'
    },
    {
        'Question ID': 'Q-TEC-INTELI-CORPOR-002-004',  # análise_de_dados_automatizada, question 3, level 3
        'Author': 'Wilson Melo Jr',
        'JSON File': 'data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json',
        'Question Index': 'questions[3]',
        'Maturity Level': '3',
        'Expected Value': 'Nível 3',
        'What It Is Now': 'A análise é executada em intervalos frequentes (ex'
    }
])

# Create hierarchy mapping from the hierarchy table
# Map Question ID to (Block, Pilar, Dimension, Capacity)
hierarchy_map = {
    'Q-ORG-ESTRUT-COLABO-010-001': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação aberta'),
    'Q-ORG-ESTRUT-COLABO-010-002': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação aberta'),
    'Q-ORG-ESTRUT-COLABO-010-003': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação aberta'),
    'Q-ORG-ESTRUT-COLABO-010-004': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação aberta'),
    'Q-ORG-ESTRUT-COLABO-010-005': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação aberta'),
    'Q-ORG-ESTRUT-COLABO-003-001': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COLABO-003-002': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COLABO-003-003': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COLABO-003-004': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COLABO-003-005': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COLABO-003-006': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COLABO-003-007': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Comunicação eficiente'),
    'Q-ORG-ESTRUT-COOPER-009-001': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Cooperação dentro da rede'),
    'Q-ORG-ESTRUT-COOPER-009-002': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Cooperação dentro da rede'),
    'Q-ORG-ESTRUT-COOPER-009-003': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Cooperação dentro da rede'),
    'Q-ORG-ESTRUT-COOPER-009-004': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Cooperação dentro da rede'),
    'Q-ORG-ESTRUT-COOPER-009-005': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Cooperação dentro da rede'),
    'Q-ORG-ESTRUT-COOPER-009-006': ('Organização', 'Estrutura e Gestão', 'Colaboração Inter e Intra-Empresarial', 'Cooperação dentro da rede'),
    'Q-ORG-ESTRUT-COMPET-008-001': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Abertura à inovação'),
    'Q-ORG-ESTRUT-COMPET-008-002': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Abertura à inovação'),
    'Q-ORG-ESTRUT-COMPET-008-003': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Abertura à inovação'),
    'Q-ORG-ESTRUT-COMPET-008-004': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Abertura à inovação'),
    'Q-ORG-ESTRUT-COMPET-011-001': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Confiança em processos e sistemas de informação'),
    'Q-ORG-ESTRUT-COMPET-011-002': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Confiança em processos e sistemas de informação'),
    'Q-ORG-ESTRUT-COMPET-011-003': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Confiança em processos e sistemas de informação'),
    'Q-ORG-ESTRUT-COMPET-011-004': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Confiança em processos e sistemas de informação'),
    'Q-ORG-ESTRUT-COMPET-017-001': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-017-002': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-017-003': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-017-004': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-017-005': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-017-006': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-017-007': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Estilo de liderança democrático'),
    'Q-ORG-ESTRUT-COMPET-006-001': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Gestão ágil'),
    'Q-ORG-ESTRUT-COMPET-006-002': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Gestão ágil'),
    'Q-ORG-ESTRUT-COMPET-006-003': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Gestão ágil'),
    'Q-ORG-ESTRUT-COMPET-006-004': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Gestão ágil'),
    'Q-ORG-ESTRUT-COMPET-006-005': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Gestão ágil'),
    'Q-ORG-ESTRUT-COMPET-006-006': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Gestão ágil'),
    'Q-ORG-ESTRUT-COMPET-005-001': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Sistemas de metas motivacionais'),
    'Q-ORG-ESTRUT-COMPET-005-002': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Sistemas de metas motivacionais'),
    'Q-ORG-ESTRUT-COMPET-005-003': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Sistemas de metas motivacionais'),
    'Q-ORG-ESTRUT-COMPET-005-004': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Sistemas de metas motivacionais'),
    'Q-ORG-ESTRUT-COMPET-005-005': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Sistemas de metas motivacionais'),
    'Q-ORG-ESTRUT-COMPET-005-006': ('Organização', 'Estrutura e Gestão', 'Competência de Liderança', 'Sistemas de metas motivacionais'),
    'Q-ORG-ESTRUT-ESTRAT-004-001': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-002': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-003': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-004': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-005': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-006': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-007': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-008': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-009': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-010': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-ESTRUT-ESTRAT-004-011': ('Organização', 'Estrutura e Gestão', 'Estratégia e Governança', 'Governança de dados'),
    'Q-ORG-PRONTI-APREND-012-001': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-002': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-003': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-004': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-005': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-006': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-007': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-008': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-009': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-012-010': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Desenvolvimento profissional contínuo'),
    'Q-ORG-PRONTI-APREND-014-001': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-002': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-003': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-004': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-005': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-006': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-007': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-008': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-009': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-014-010': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho', 'Reconhecer o valor dos erros'),
    'Q-ORG-PRONTI-APREND-013-001': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-002': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-003': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-004': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-005': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-006': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-007': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-008': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-009': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-ORG-PRONTI-APREND-013-010': ('Organização', 'Prontidão de Talentos', 'Aprendizado e Desenvolvimento da Força de Trabalho (D13)', 'Prover competencias digitais'),
    'Q-TEC-AUTOMA-CICLOV-025-001': ('Processo', 'Ciclo de Vida do Produto', 'Ciclo de Vida Integrado do Produto', 'Foco em benefícios ao cliente'),
    'Q-TEC-AUTOMA-CICLOV-025-002': ('Processo', 'Ciclo de Vida do Produto', 'Ciclo de Vida Integrado do Produto', 'Foco em benefícios ao cliente'),
    'Q-TEC-AUTOMA-CICLOV-025-003': ('Processo', 'Ciclo de Vida do Produto', 'Ciclo de Vida Integrado do Produto', 'Foco em benefícios ao cliente'),
    'Q-TEC-AUTOMA-CICLOV-025-004': ('Processo', 'Ciclo de Vida do Produto', 'Ciclo de Vida Integrado do Produto', 'Foco em benefícios ao cliente'),
    'Q-TEC-AUTOMA-CICLOV-025-005': ('Processo', 'Ciclo de Vida do Produto', 'Ciclo de Vida Integrado do Produto', 'Foco em benefícios ao cliente'),
    'Q-PROC-OPERAÇ-HORIZO-015-001': ('Processo', 'Operações/Cadeia de Suprimentos', 'Horizontal (D2)', 'Horizontal (D2) - Mapeamento secundário'),
    'Q-PROC-OPERAÇ-HORIZO-015-002': ('Processo', 'Operações/Cadeia de Suprimentos', 'Horizontal (D2)', 'Horizontal (D2) - Mapeamento secundário'),
    'Q-PROC-OPERAÇ-HORIZO-015-003': ('Processo', 'Operações/Cadeia de Suprimentos', 'Horizontal (D2)', 'Horizontal (D2) - Mapeamento secundário'),
    'Q-PROC-OPERAÇ-HORIZO-015-004': ('Processo', 'Operações/Cadeia de Suprimentos', 'Horizontal (D2)', 'Horizontal (D2) - Mapeamento secundário'),
    'Q-PROC-OPERAÇ-HORIZO-015-005': ('Processo', 'Operações/Cadeia de Suprimentos', 'Horizontal (D2)', 'Horizontal (D2) - Mapeamento secundário'),
    'Q-PROC-OPERAÇ-HORIZO-015-006': ('Processo', 'Operações/Cadeia de Suprimentos', 'Horizontal (D2)', 'Horizontal (D2) - Mapeamento secundário'),
    'Q-PROC-OPERAÇ-VERTIC-016-001': ('Processo', 'Operações/Cadeia de Suprimentos', 'Vertical (D1)', 'Vertical (D1) - primário'),
    'Q-PROC-OPERAÇ-VERTIC-016-002': ('Processo', 'Operações/Cadeia de Suprimentos', 'Vertical (D1)', 'Vertical (D1) - primário'),
    'Q-PROC-OPERAÇ-VERTIC-016-003': ('Processo', 'Operações/Cadeia de Suprimentos', 'Vertical (D1)', 'Vertical (D1) - primário'),
    'Q-PROC-OPERAÇ-VERTIC-016-004': ('Processo', 'Operações/Cadeia de Suprimentos', 'Vertical (D1)', 'Vertical (D1) - primário'),
    'Q-PROC-OPERAÇ-VERTIC-016-005': ('Processo', 'Operações/Cadeia de Suprimentos', 'Vertical (D1)', 'Vertical (D1) - primário'),
    'Q-TEC-AUTOMA-CHÃOFÁ-020-001': ('Tecnologia', 'Automação', 'Chão de Fábrica', 'Design de interfaces orientado à tarefa'),
    'Q-TEC-AUTOMA-CHÃOFÁ-020-002': ('Tecnologia', 'Automação', 'Chão de Fábrica', 'Design de interfaces orientado à tarefa'),
    'Q-TEC-AUTOMA-CHÃOFÁ-020-003': ('Tecnologia', 'Automação', 'Chão de Fábrica', 'Design de interfaces orientado à tarefa'),
    'Q-TEC-CONECT-CHÃOFÁ-024-001': ('Tecnologia', 'Conectividade', 'Chão de Fábrica', 'Aquisição de dados por sensores e atuadores'),
    'Q-TEC-CONECT-CHÃOFÁ-024-002': ('Tecnologia', 'Conectividade', 'Chão de Fábrica', 'Aquisição de dados por sensores e atuadores'),
    'Q-TEC-CONECT-CHÃOFÁ-024-003': ('Tecnologia', 'Conectividade', 'Chão de Fábrica', 'Aquisição de dados por sensores e atuadores'),
    'Q-TEC-CONECT-CHÃOFÁ-024-004': ('Tecnologia', 'Conectividade', 'Chão de Fábrica', 'Aquisição de dados por sensores e atuadores'),
    'Q-TEC-CONECT-CORPOR-022-001': ('Tecnologia', 'Conectividade', 'Empresa', 'Interface de dados padronizada'),
    'Q-TEC-CONECT-CORPOR-022-002': ('Tecnologia', 'Conectividade', 'Empresa', 'Interface de dados padronizada'),
    'Q-TEC-CONECT-CORPOR-022-003': ('Tecnologia', 'Conectividade', 'Empresa', 'Interface de dados padronizada'),
    'Q-TEC-CONECT-INSTAL-023-001': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-CONECT-INSTAL-023-002': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-CONECT-INSTAL-023-003': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-CONECT-INSTAL-023-004': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-CONECT-INSTAL-023-005': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-CONECT-INSTAL-023-006': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-CONECT-INSTAL-023-007': ('Tecnologia', 'Conectividade', 'Instalações', 'Infraestrutura de TI resiliente'),
    'Q-TEC-INTELI-CHÃOFÁ-001-001': ('Tecnologia', 'Inteligência', 'Chão de Fábrica', 'Pré-processamento descentralizado de dados de sensores'),
    'Q-TEC-INTELI-CHÃOFÁ-001-002': ('Tecnologia', 'Inteligência', 'Chão de Fábrica', 'Pré-processamento descentralizado de dados de sensores'),
    'Q-TEC-INTELI-CHÃOFÁ-001-003': ('Tecnologia', 'Inteligência', 'Chão de Fábrica', 'Pré-processamento descentralizado de dados de sensores'),
    'Q-TEC-INTELI-CORPOR-018-001': ('Tecnologia', 'Inteligência', 'Corporativo (D11)', 'Enterprise (D11)'),
    'Q-TEC-INTELI-CORPOR-018-002': ('Tecnologia', 'Inteligência', 'Corporativo (D11)', 'Enterprise (D11)'),
    'Q-TEC-INTELI-CORPOR-018-003': ('Tecnologia', 'Inteligência', 'Corporativo (D11)', 'Enterprise (D11)'),
    'Q-TEC-INTELI-CORPOR-018-004': ('Tecnologia', 'Inteligência', 'Corporativo (D11)', 'Enterprise (D11)'),
    'Q-TEC-INTELI-CORPOR-018-005': ('Tecnologia', 'Inteligência', 'Corporativo (D11)', 'Enterprise (D11)'),
    'Q-TEC-INTELI-CORPOR-002-001': ('Tecnologia', 'Inteligência', 'Empresa', 'Análise de dados automatizada'),
    'Q-TEC-INTELI-CORPOR-002-002': ('Tecnologia', 'Inteligência', 'Empresa', 'Análise de dados automatizada'),
    'Q-TEC-INTELI-CORPOR-002-003': ('Tecnologia', 'Inteligência', 'Empresa', 'Análise de dados automatizada'),
    'Q-TEC-INTELI-CORPOR-002-004': ('Tecnologia', 'Inteligência', 'Empresa', 'Análise de dados automatizada'),
    'Q-TEC-INTELI-CORPOR-019-001': ('Tecnologia', 'Inteligência', 'Empresa', 'Entrega de informação contextualizada'),
    'Q-TEC-INTELI-CORPOR-019-002': ('Tecnologia', 'Inteligência', 'Empresa', 'Entrega de informação contextualizada'),
    'Q-TEC-INTELI-CORPOR-019-003': ('Tecnologia', 'Inteligência', 'Empresa', 'Entrega de informação contextualizada'),
    'Q-TEC-INTELI-CORPOR-019-004': ('Tecnologia', 'Inteligência', 'Empresa', 'Entrega de informação contextualizada'),
    'Q-TEC-INTELI-CORPOR-019-005': ('Tecnologia', 'Inteligência', 'Empresa', 'Entrega de informação contextualizada'),
}

# Add dimension and capacity to each warning
for warning in warnings_data:
    question_id = warning['Question ID']
    if question_id in hierarchy_map:
        block, pilar, dimension, capacity = hierarchy_map[question_id]
        warning['Block'] = block
        warning['Pilar'] = pilar
        warning['Dimension'] = dimension
        warning['Capacity'] = capacity
    else:
        warning['Block'] = 'Unknown'
        warning['Pilar'] = 'Unknown'
        warning['Dimension'] = 'Unknown'
        warning['Capacity'] = 'Unknown'

# Create DataFrame
df = pd.DataFrame(warnings_data)

# Reorder columns as requested
df = df[['Question ID', 'Author', 'Dimension', 'Capacity', 'JSON File', 'Expected Value', 'What It Is Now']]

# Sort by Author, then by Question ID
df = df.sort_values(['Author', 'Question ID'])

# Save to Excel
output_file = '/Users/emadruga/proj/industria-4.0/maturity_level_warnings_summary.xlsx'
df.to_excel(output_file, index=False, sheet_name='Label Warnings')

print(f"Excel file created: {output_file}")
print(f"Total warnings: {len(df)}")
print(f"\nWarnings by author:")
print(df.groupby('Author').size())
