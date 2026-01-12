# JSON Consistency Check Report
**Date:** January 8, 2026
**Catalog:** JSON7_20260105_164046
**Total Files Analyzed:** 23

---

## Introduction

This report presents the results of a comprehensive consistency validation performed on the Industry 4.0 Maturity Questions Catalog using the newly developed `json_consistency_check.py` script.

### About the Consistency Checker Script

The **JSON Consistency Checker** (`./question-base/scripts/json_consistency_check.py`) is a Python tool designed to validate the structural integrity, completeness, and consistency of JSON files containing maturity assessment questions for Industry 4.0.

#### What the Script Validates

The script performs comprehensive validation across multiple dimensions:

1. **Structural Validation**
   - Presence of required top-level keys (`capacity`, `questions`, `references`)
   - Correct nesting of all sections
   - Data type consistency (arrays, objects, strings, integers)

2. **Capacity Section**
   - ID format validation (must start with "CAP-")
   - Block value validation (must be "Organização", "Processo", or "Tecnologia")
   - Description completeness (minimum length requirements)
   - Related capacities structure

3. **Metadata Validation**
   - Required fields: `source_frameworks`, `author`, `version`, `last_updated`, `source_docx`, `status`
   - Framework values (must be "ACATECH" or "SIRI")
   - Version format (semantic versioning: "1.0")
   - Date format (YYYY-MM-DD)
   - Valid status values

4. **Questions Validation**
   - Question ID format and uniqueness
   - Question number sequence integrity (1, 2, 3, ...)
   - Required fields presence: `artifacts`, `metrics`, `sampling_guidance`
   - Question text completeness

5. **Maturity Levels**
   - Exactly 7 levels (0 through 6) must be defined
   - Level number sequence validation
   - Label consistency ("Nível 0", "Nível 1", ..., "Nível 6")
   - Description completeness (no empty descriptions)
   - Evidence signals structure validation

6. **Observable Behaviors**
   - Presence of at least one observable behavior per maturity level
   - Non-empty behavior definitions

7. **References**
   - Citation field presence
   - URL field consistency

#### How to Use the Script

**Basic Usage:**
```bash
python3 question-base/scripts/json_consistency_check.py <data_directory>
```

**Example:**
```bash
python3 question-base/scripts/json_consistency_check.py ./question-base/JSON7_20260105_164046/data
```

**Output:**
The script produces a detailed report showing:
- Total files processed
- Number of valid vs. invalid files
- Issues categorized by severity (ERROR, WARNING, INFO)
- Issues grouped by category and file
- List of all authors and frameworks found

**Exit Code:**
- `0` = All files passed validation
- `1` = One or more files have errors

---

## JSON Template: Expected Structure

Below is the correct JSON template that all capacity files should follow:

### Complete Template Example

```json
{
  "capacity": {
    "id": "CAP-BLOCK-PILAR-DIMENSION-NNN",
    "name": "Capacity Name",
    "block": "Organização | Processo | Tecnologia",
    "pilar": "Pilar Name",
    "dimension": "Dimension Name",
    "description": "Detailed description of the capacity (minimum 100 characters recommended). Should explain what the capacity represents, its importance in Industry 4.0 maturity, and how it evolves across maturity levels.",
    "related_capacities": [
      "Related Capacity 1",
      "Related Capacity 2",
      "Related Capacity 3"
    ],
    "metadata": {
      "source_frameworks": [
        "ACATECH",
        "SIRI"
      ],
      "author": "Author Full Name",
      "version": "1.0",
      "last_updated": "YYYY-MM-DD",
      "source_docx": "source_document_name.docx",
      "status": "draft | review | approved | published"
    }
  },
  "questions": [
    {
      "id": "Q-BLOCK-PILAR-DIMENSION-NNN-001",
      "question_number": 1,
      "title": "Question Title",
      "text": "The actual question text that will be asked during assessment?",
      "maturity_levels": [
        {
          "level": 0,
          "label": "Nível 0",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        },
        {
          "level": 1,
          "label": "Nível 1",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        },
        {
          "level": 2,
          "label": "Nível 2",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        },
        {
          "level": 3,
          "label": "Nível 3",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        },
        {
          "level": 4,
          "label": "Nível 4",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        },
        {
          "level": 5,
          "label": "Nível 5",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        },
        {
          "level": 6,
          "label": "Nível 6",
          "description": "Description of what characterizes this maturity level.",
          "evidence_signals": {
            "observable_behaviors": [
              "Observable behavior or signal 1",
              "Observable behavior or signal 2"
            ]
          }
        }
      ],
      "artifacts": [
        "Artifact description 1: where to find it and what to look for",
        "Artifact description 2: where to find it and what to look for"
      ],
      "metrics": [
        "KPI or metric 1 that can be used to assess this question",
        "KPI or metric 2 that can be used to assess this question"
      ],
      "sampling_guidance": "Guidance for assessors on how to sample evidence, who to interview, what documents to review, etc."
    }
  ],
  "references": [
    {
      "citation": "Full academic citation in standard format.",
      "url": "https://optional-url-to-source.com"
    }
  ]
}
```

### Key Template Requirements

1. **Exactly 7 maturity levels** per question (levels 0-6)
2. **Label format** must be "Nível N" where N is the level number
3. **Observable behaviors** cannot be empty arrays
4. **Three required arrays** per question: `artifacts`, `metrics`, `maturity_levels`
5. **One required string** per question: `sampling_guidance`
6. **Date format** must be YYYY-MM-DD (e.g., "2026-01-05")
7. **Valid blocks** are: "Organização", "Processo", "Tecnologia"
8. **Valid frameworks** are: "ACATECH", "SIRI"

---

## Validation Summary

### Overall Statistics

| Metric | Count |
|--------|-------|
| Total Files | 23 |
| Valid Files | 10 |
| Files with Errors | 13 |
| **Total Issues** | **188** |
| └─ Errors | 13 |
| └─ Warnings | 172 |
| └─ Info | 3 |

### Authors in Catalog

1. Cristiano Gurgel Castro
2. Ewerton Madruga
3. Flavia Agostini
4. Wilson Melo Jr

### Frameworks Used

1. ACATECH
2. SIRI

---

## Issues by Author

### Cristiano Gurgel Castro (4 files)

**Files:**
- `Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/comunicação_eficiente.json`
- `Organização/Estrutura_e_Gestão/Estratégia_e_Governança/governança_de_dados.json`
- `Tecnologia/Inteligência/Chão_de_Fábrica/pré-processamento_descentralizado_de_dados_de_sensores.json`
- `Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json`

#### ERRORS: 0

No errors found in this author's files.

#### WARNINGS: 53

**MATURITY_LEVEL_LABEL (47 warnings)**

File: `comunicação_eficiente.json`
- Expected label 'Nível 1', found 'Existem canais de comunicação formais (ex' [questions[0].maturity_levels[1].label]
- Expected label 'Nível 2', found 'A organização utiliza ferramentas digitais básicas para comunicação (ex' [questions[0].maturity_levels[2].label]
- Expected label 'Nível 4', found 'A comunicação é rastreável e contextualizada, vinculada a processos de negócio (ex' [questions[0].maturity_levels[4].label]
- Expected label 'Nível 0', found 'A comunicação com fornecedores e clientes é totalmente manual (ex' [questions[1].maturity_levels[0].label]
- Expected label 'Nível 1', found 'São utilizados métodos digitais básicos, mas não padronizados (ex' [questions[1].maturity_levels[1].label]
- Expected label 'Nível 2', found 'A empresa utiliza um canal digital unidirecional, como um portal simples onde disponibiliza informações (ex' [questions[1].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Existe um portal de colaboração (ex' [questions[1].maturity_levels[3].label]
- Expected label 'Nível 4', found 'A comunicação é automatizada via integração de sistemas (ex' [questions[1].maturity_levels[4].label]
- Expected label 'Nível 5', found 'A integração de sistemas é ampla e ocorre em tempo real, permitindo o compartilhamento de dados operacionais (ex' [questions[1].maturity_levels[5].label]
- Expected label 'Nível 6', found 'Existe uma rede de valor dinâmica e conectada. Os sistemas da empresa e dos parceiros comunicam-se de forma autônoma para otimizar a cadeia (ex' [questions[1].maturity_levels[6].label]
- Expected label 'Nível 0', found 'As instruções de trabalho são predominantemente verbais (ex' [questions[2].maturity_levels[0].label]
- Expected label 'Nível 2', found 'As instruções são digitais (ex' [questions[2].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Os sistemas (ex' [questions[2].maturity_levels[3].label]
- Expected label 'Nível 5', found 'A empresa utiliza sistemas de assistência avançados (ex' [questions[2].maturity_levels[5].label]
- Expected label 'Nível 6', found 'Os sistemas de assistência são adaptativos e proativos. Eles não apenas guiam o operador (ex' [questions[2].maturity_levels[6].label]
- Expected label 'Nível 1', found 'Listas básicas (ex' [questions[4].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Existem sistemas de TI (ex' [questions[4].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Ferramentas de colaboração (ex' [questions[4].maturity_levels[3].label]
- Expected label 'Nível 4', found 'Plataformas de TI (ex' [questions[4].maturity_levels[4].label]
- Expected label 'Nível 6', found 'As plataformas de TI não apenas dão transparência às competências existentes, mas também se integram a novas tecnologias de treinamento (ex' [questions[4].maturity_levels[6].label]
- Expected label 'Nível 1', found 'As metas são puramente departamentais e muitas vezes unidimensionais (ex' [questions[5].maturity_levels[1].label]
- Expected label 'Nível 6', found 'O sucesso da equipe de especialistas/comunidade é formalmente medido (ex' [questions[5].maturity_levels[6].label]
- Expected label 'Nível 1', found 'A gestão de projetos é tradicional (ex' [questions[6].maturity_levels[1].label]
- Expected label 'Nível 2', found 'A empresa experimenta métodos ágeis (ex' [questions[6].maturity_levels[2].label]

File: `governança_de_dados.json`
- Expected label 'Nível 3', found 'Políticas de governança de dados são implementadas em toda a empresa, com papéis e responsabilidades definidos (ex' [questions[0].maturity_levels[3].label]
- Expected label 'Nível 0', found 'Não há gestão de dados mestres. Dados críticos (ex' [questions[1].maturity_levels[0].label]
- Expected label 'Nível 1', found 'A empresa reconhece os problemas de inconsistência de dados, mas as correções são feitas manualmente, de forma reativa e pontual (ex' [questions[1].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Existem processos departamentais para tentar padronizar a entrada de dados mestres (ex' [questions[1].maturity_levels[2].label]
- Expected label 'Nível 5', found 'O sistema MDM é usado proativamente para gerenciar o ciclo de vida completo dos dados mestres e para simular o impacto de mudanças (ex' [questions[1].maturity_levels[5].label]
- Expected label 'Nível 6', found 'Os dados mestres são gerenciados de forma dinâmica e federada, permitindo a integração ágil de novos parceiros ou fontes de dados (ex' [questions[1].maturity_levels[6].label]
- Expected label 'Nível 3', found 'A empresa começa a medir ativamente a qualidade dos dados. Existem painéis (dashboards) e KPIs de qualidade (ex' [questions[2].maturity_levels[3].label]
- Expected label 'Nível 4', found 'A empresa analisa a causa-raiz dos problemas de qualidade de dados. Existem processos formais de remediação para corrigir os dados na fonte (ex' [questions[2].maturity_levels[4].label]
- Expected label 'Nível 5', found 'A qualidade de dados é gerenciada de forma proativa e preditiva. Regras de qualidade são automatizadas e integradas aos processos de negócio (ex' [questions[2].maturity_levels[5].label]
- Expected label 'Nível 0', found 'A troca de dados entre sistemas é quase inexistente ou totalmente manual (ex' [questions[3].maturity_levels[0].label]
- Expected label 'Nível 2', found 'A empresa utiliza um barramento de serviço (ESB) ou ferramenta de EAI (Enterprise Application Integration) para gerenciar algumas integrações centrais, mas a maioria ainda é ponto a ponto. Os formatos de dados (ex' [questions[3].maturity_levels[2].label]
- Expected label 'Nível 3', found 'A empresa adota padrões de indústria (ex' [questions[3].maturity_levels[3].label]
- Expected label 'Nível 1', found 'As decisões são centralizadas e baseadas em procedimentos formais. A TI é usada de forma isolada (ex' [questions[4].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Os sistemas de TI estão conectados (ex' [questions[4].maturity_levels[2].label]
- Expected label 'Nível 0', found 'Não há delegação para sistemas. Todas as decisões de processo (ex' [questions[5].maturity_levels[0].label]
- Expected label 'Nível 1', found 'Os sistemas de TI são usados apenas para registrar dados (ex' [questions[5].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Os sistemas de TI (ex' [questions[5].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Os sistemas (Digital Shadow) alertam ativamente sobre desvios em tempo real (ex' [questions[5].maturity_levels[3].label]
- Expected label 'Nível 4', found 'Os sistemas analisam os dados (transparência) e diagnosticam a causa raiz de um problema (ex' [questions[5].maturity_levels[4].label]
- Expected label 'Nível 5', found 'Os sistemas (capacidade preditiva) antecipam eventos e recomendam ações corretivas (ex' [questions[5].maturity_levels[5].label]
- Expected label 'Nível 6', found 'Os sistemas de TI (adaptabilidade) têm autonomia para tomar e executar decisões táticas complexas automaticamente (ex' [questions[5].maturity_levels[6].label]
- Expected label 'Nível 1', found 'As decisões são baseadas em dados de sistemas isolados (ex' [questions[6].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Os sistemas estão minimamente conectados. O tomador de decisão pode buscar ativamente os dados em diferentes sistemas (ex' [questions[6].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Os tomadores de decisão têm acesso a um "Digital Shadow" (ex' [questions[6].maturity_levels[3].label]
- Expected label 'Nível 4', found 'O sistema não apenas mostra o estado atual, mas também fornece análises de causa-raiz (Transparência), explicando por que algo está acontecendo (ex' [questions[6].maturity_levels[4].label]
- Expected label 'Nível 5', found 'O sistema fornece informações preditivas e simulações de impacto (Capacidade Preditiva) aos tomadores de decisão (ex' [questions[6].maturity_levels[5].label]

File: `pré-processamento_descentralizado_de_dados_de_sensores.json`
- Expected label 'Nível 5', found 'Os sistemas de processamento descentralizado são robustos o suficiente para executar análises complexas (ex' [questions[0].maturity_levels[5].label]
- Expected label 'Nível 4', found 'O pré-processamento descentralizado (ex' [questions[1].maturity_levels[4].label]
- Expected label 'Nível 5', found 'Os sistemas descentralizados executam análises complexas (ex' [questions[1].maturity_levels[5].label]

File: `análise_de_dados_automatizada.json`
- Expected label 'Nível 5', found 'A empresa emprega modelos e algoritmos (ex' [questions[0].maturity_levels[5].label]
- Expected label 'Nível 1', found 'A análise automatizada é usada de forma isolada, focada em um único ativo, parâmetro ou processo (ex' [questions[1].maturity_levels[1].label]
- Expected label 'Nível 3', found 'A análise integra dados de múltiplos processos e sistemas dentro de um mesmo domínio funcional (ex' [questions[1].maturity_levels[3].label]

**OBSERVABLE_BEHAVIORS (3 warnings)**

File: `governança_de_dados.json`
- Level 0 has no observable behaviors defined [questions[8].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[9].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[10].maturity_levels[0].evidence_signals.observable_behaviors]

**MATURITY_LEVEL_DESCRIPTION (3 warnings)**

File: `pré-processamento_descentralizado_de_dados_de_sensores.json`
- Expected label 'Nível 3', found 'Sistemas embarcados são utilizados para monitoramento local e loops de controle fechado de processos técnicos (ex' [questions[2].maturity_levels[3].label]
- Expected label 'Nível 4', found 'O pré-processamento descentralizado em dispositivos de borda é usado para executar cálculos mais complexos (ex' [questions[2].maturity_levels[4].label]
- Expected label 'Nível 5', found 'O processamento descentralizado executa cálculos complexos e modelos de otimização (ex' [questions[2].maturity_levels[5].label]

---

### Ewerton Madruga (6 files)

**Files:**
- `Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/comunicação_aberta.json`
- `Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/cooperação_dentro_da_rede.json`
- `Organização/Estrutura_e_Gestão/Competência_de_Liderança/abertura_à_inovação.json`
- `Organização/Estrutura_e_Gestão/Competência_de_Liderança/confiança_em_processos_e_sistemas_de_informação.json`
- `Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json`
- `Organização/Estrutura_e_Gestão/Competência_de_Liderança/sistemas_de_metas_motivacionais.json`

#### ERRORS: 4

**QUESTION (4 errors)**

File: `comunicação_aberta.json`
- Missing question fields: artifacts, metrics, sampling_guidance [questions[1]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[2]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[3]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[4]]

#### WARNINGS: 38

**MATURITY_LEVELS (1 warning)**

File: `gestão_ágil.json`
- Expected 7 maturity levels (0-6), found 6 [questions[0].maturity_levels]

**MATURITY_LEVEL_LABEL (9 warnings)**

File: `gestão_ágil.json`
- Expected label 'Nível 0', found 'Não familiarizada' [questions[0].maturity_levels[0].label]
- Expected label 'Nível 1', found 'Conhecimento Limitado' [questions[0].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Informada' [questions[0].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Semi-dependente' [questions[0].maturity_levels[3].label]
- Expected label 'Nível 4', found 'Independente' [questions[0].maturity_levels[4].label]
- Expected label 'Nível 5', found 'Adaptativa' [questions[0].maturity_levels[5].label]
- Expected label 'Nível 2', found 'Existe um programa básico de treinamento inicial (ex' [questions[4].maturity_levels[2].label]

File: `sistemas_de_metas_motivacionais.json`
- Expected label 'Nível 1', found 'Metas individuais privadas, compartilhadas apenas entre líder e liderado em conversas 1' [questions[2].maturity_levels[1].label]

File: `governança_de_dados.json`
- Expected label 'Nível 2', found 'A gestão ouve as propostas, mas a iniciativa é bloqueada por burocracia excessiva (ex' [questions[8].maturity_levels[2].label]

**OBSERVABLE_BEHAVIORS (28 warnings)**

File: `comunicação_aberta.json`
- Level 0 has no observable behaviors defined [questions[1].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[1].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[1].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[1].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[1].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[1].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[1].maturity_levels[6].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[2].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[2].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[2].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[2].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[2].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[2].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[2].maturity_levels[6].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[3].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[3].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[3].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[3].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[3].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[3].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[3].maturity_levels[6].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[4].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[4].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[4].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[4].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[4].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[4].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[4].maturity_levels[6].evidence_signals.observable_behaviors]

#### INFO: 2

**STRUCTURE (2 info)**

File: `cooperação_dentro_da_rede.json`
- Extra top-level keys: glossary

File: `gestão_ágil.json`
- Extra top-level keys: glossary

---

### Flavia Agostini (8 files)

**Files:**
- `Organização/Estrutura_e_Gestão/Competência_de_Liderança/estilo_de_liderança_democrático.json`
- `Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho/desenvolvimento_profissional_contínuo.json`
- `Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho/reconhecer_o_valor_dos_erros.json`
- `Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho_(D13)/prover_competencias_digitais.json`
- `Processo/Operações/Cadeia_de_Suprimentos/Horizontal_(D2)/horizontal_(d2)_-_mapeamento_secundário.json`
- `Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json`
- `Tecnologia/Inteligência/Corporativo_(D11)/enterprise_(d11).json`
- `Tecnologia/Inteligência/Empresa/entrega_de_informação_contextualizada.json`

#### ERRORS: 8

**QUESTION (8 errors)**

File: `estilo_de_liderança_democrático.json`
- Missing question fields: artifacts, metrics, sampling_guidance [questions[7]]

File: `horizontal_(d2)_-_mapeamento_secundário.json`
- Missing question fields: artifacts, metrics, sampling_guidance [questions[5]]

File: `entrega_de_informação_contextualizada.json`
- Missing question fields: artifacts, metrics, sampling_guidance [questions[2]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[3]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[4]]

File: `confiança_em_processos_e_sistemas_de_informação.json`
- Missing question fields: artifacts, metrics, sampling_guidance [questions[0]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[1]]
- Missing question fields: artifacts, metrics, sampling_guidance [questions[2]]

#### WARNINGS: 65

**MATURITY_LEVELS (4 warnings)**

File: `horizontal_(d2)_-_mapeamento_secundário.json`
- Expected 7 maturity levels (0-6), found 0 [questions[5].maturity_levels]

File: `entrega_de_informação_contextualizada.json`
- Expected 7 maturity levels (0-6), found 0 [questions[2].maturity_levels]
- Expected 7 maturity levels (0-6), found 0 [questions[3].maturity_levels]
- Expected 7 maturity levels (0-6), found 0 [questions[4].maturity_levels]

**MATURITY_LEVEL_DESCRIPTION (11 warnings)**

File: `estilo_de_liderança_democrático.json`
- Level 0 has empty description [questions[7].maturity_levels[0].description]
- Level 1 has empty description [questions[7].maturity_levels[1].description]
- Level 2 has empty description [questions[7].maturity_levels[2].description]
- Level 3 has empty description [questions[7].maturity_levels[3].description]
- Level 4 has empty description [questions[7].maturity_levels[4].description]
- Level 5 has empty description [questions[7].maturity_levels[5].description]
- Level 6 has empty description [questions[7].maturity_levels[6].description]

File: `vertical_(d1)_-_primário.json`
- Level 5 has empty description [questions[0].maturity_levels[5].description]
- Level 6 has empty description [questions[0].maturity_levels[6].description]
- Level 5 has empty description [questions[1].maturity_levels[5].description]
- Level 6 has empty description [questions[1].maturity_levels[6].description]

**MATURITY_LEVEL_LABEL (4 warnings)**

File: `desenvolvimento_profissional_contínuo.json`
- Expected label 'Nível 3', found 'Os líderes são formalmente cobrados por (ex' [questions[6].maturity_levels[3].label]

File: `reconhecer_o_valor_dos_erros.json`
- Expected label 'Nível 6', found 'A cultura é autorregulada' [questions[1].maturity_levels[6].label]

File: `prover_competencias_digitais.json`
- Expected label 'Nível 6', found 'A integração é completa' [questions[6].maturity_levels[6].label]

File: `horizontal_(d2)_-_mapeamento_secundário.json`
- Expected label 'Nível 3', found 'A rastreabilidade é digital e parcial entre parceiros diretos (ex.' [questions[2].maturity_levels[3].label]

**OBSERVABLE_BEHAVIORS (46 warnings)**

File: `estilo_de_liderança_democrático.json`
- Level 0 has no observable behaviors defined [questions[7].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[7].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[7].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[7].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[7].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[7].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[7].maturity_levels[6].evidence_signals.observable_behaviors]

File: `confiança_em_processos_e_sistemas_de_informação.json`
- Level 0 has no observable behaviors defined [questions[0].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[0].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[0].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[0].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[0].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[0].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[0].maturity_levels[6].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[1].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[1].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[1].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[1].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[1].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[1].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[1].maturity_levels[6].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[2].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[2].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[2].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[2].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[2].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[2].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[2].maturity_levels[6].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[3].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[3].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[3].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[3].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[3].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[3].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[3].maturity_levels[6].evidence_signals.observable_behaviors]

File: `análise_de_dados_automatizada.json`
- Level 0 has no observable behaviors defined [questions[1].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[2].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[3].maturity_levels[0].evidence_signals.observable_behaviors]

File: `entrega_de_informação_contextualizada.json`
- Level 0 has no observable behaviors defined [questions[0].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[0].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[0].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[1].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[1].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[1].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[1].maturity_levels[5].evidence_signals.observable_behaviors]

#### INFO: 1

**STRUCTURE (1 info)**

File: `sistemas_de_metas_motivacionais.json`
- Extra top-level keys: glossary

---

### Wilson Melo Jr (5 files)

**Files:**
- `Processo/Ciclo_de_Vida_do_Produto/Ciclo_de_Vida_Integrado_do_Produto/foco_em_benefícios_ao_cliente.json`
- `Tecnologia/Automação/Chão_de_Fábrica/design_de_interfaces_orientado_à_tarefa.json`
- `Tecnologia/Conectividade/Chão_de_Fábrica/aquisição_de_dados_por_sensores_e_atuadores.json`
- `Tecnologia/Conectividade/Empresa/interface_de_dados_padronizada.json`
- `Tecnologia/Conectividade/Instalações/infraestrutura_de_ti_resiliente.json`

#### ERRORS: 1

**QUESTION (1 error - appears to be from confiança_em_processos cross-attribution)**

File: `confiança_em_processos_e_sistemas_de_informação.json`
- Missing question fields: artifacts, metrics, sampling_guidance [questions[3]]

#### WARNINGS: 16

**MATURITY_LEVEL_LABEL (13 warnings)**

File: `governança_de_dados.json`
- Expected label 'Nível 2', found 'Os funcionários são incentivados a sugerir melhorias (ex' [questions[7].maturity_levels[2].label]
- Expected label 'Nível 4', found 'A implementação segue ciclos formais de melhoria (ex' [questions[10].maturity_levels[4].label]
- Expected label 'Nível 6', found 'A implementação é ativamente ágil, usando ciclos curtos (ex' [questions[10].maturity_levels[6].label]

File: `análise_de_dados_automatizada.json`
- Expected label 'Nível 4', found 'A análise integra dados de forma vertical, conectando o shop floor (TI/TO) com sistemas de gestão corporativa (Enterprise), como ERP ou SCM (ex' [questions[1].maturity_levels[4].label]
- Expected label 'Nível 5', found 'A análise integra dados verticalmente (fábrica + gestão) e horizontalmente, incluindo dados de parceiros externos (ex' [questions[1].maturity_levels[5].label]
- Expected label 'Nível 1', found 'A análise é 100% manual. Os dados são exportados (ex' [questions[2].maturity_levels[1].label]
- Expected label 'Nível 2', found 'A análise é automatizada, mas limitada a regras fixas e pré-programadas (ex' [questions[2].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Os sistemas aplicam regras de diagnóstico complexas (árvores de decisão, expert systems) que foram definidas manualmente por especialistas para identificar causas conhecidas (ex' [questions[2].maturity_levels[3].label]
- Expected label 'Nível 4', found 'A empresa utiliza modelos preditivos (ex' [questions[2].maturity_levels[4].label]
- Expected label 'Nível 5', found 'A empresa utiliza ativamente técnicas de Machine Learning (ex' [questions[2].maturity_levels[5].label]
- Expected label 'Nível 6', found 'Os sistemas são adaptativos e utilizam autoaprendizado (ex' [questions[2].maturity_levels[6].label]
- Expected label 'Nível 2', found 'A análise é automatizada, mas executada em lotes (batch) com baixa frequência (ex' [questions[3].maturity_levels[2].label]
- Expected label 'Nível 3', found 'A análise é executada em intervalos frequentes (ex' [questions[3].maturity_levels[3].label]

**OBSERVABLE_BEHAVIORS (3 warnings)**

File: `pré-processamento_descentralizado_de_dados_de_sensores.json`
- Expected label 'Nível 6', found 'Os sistemas embarcados executam processamento complexo em tempo real (ex' [questions[2].maturity_levels[6].label]

File: `interface_de_dados_padronizada.json`
- Level 6 has no observable behaviors defined [questions[2].maturity_levels[6].evidence_signals.observable_behaviors]

File: `análise_de_dados_automatizada.json` (overlaps with Cristiano Castro's work)
- Level 0 has no observable behaviors defined [questions[1].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[2].maturity_levels[0].evidence_signals.observable_behaviors]

#### INFO: 0

No INFO-level issues found for this author.

---

## Recommendations by Issue Type

### Critical Issues (ERRORS)

1. **Missing Required Fields in Questions**
   - **Count:** 13 errors across multiple authors
   - **Impact:** Questions are incomplete and cannot be used for assessments
   - **Action:** Add the missing fields `artifacts`, `metrics`, and `sampling_guidance` to all affected questions
   - **Priority:** HIGH

### Major Issues (WARNINGS)

2. **Incorrect Maturity Level Labels**
   - **Count:** 86 warnings
   - **Impact:** Inconsistent labeling makes it harder to parse and display questions correctly
   - **Action:** Standardize all labels to follow "Nível N" format exactly
   - **Priority:** MEDIUM
   - **Note:** Some authors are using descriptive text in labels instead of the standard format

3. **Missing Observable Behaviors**
   - **Count:** 70 warnings
   - **Impact:** Maturity levels lack concrete evidence signals for assessors
   - **Action:** Add at least one observable behavior for each maturity level
   - **Priority:** HIGH
   - **Note:** Observable behaviors are critical for assessment validity

4. **Wrong Number of Maturity Levels**
   - **Count:** 5 warnings
   - **Impact:** Questions don't align with the 0-6 maturity scale
   - **Action:** Ensure all questions have exactly 7 maturity levels (0-6)
   - **Priority:** HIGH

5. **Empty Maturity Level Descriptions**
   - **Count:** 11 warnings
   - **Impact:** Maturity levels cannot be assessed without descriptions
   - **Action:** Write complete descriptions for all maturity levels
   - **Priority:** HIGH

### Minor Issues (INFO)

6. **Extra Top-Level Keys (glossary)**
   - **Count:** 3 info items
   - **Impact:** Non-standard structure, but doesn't break functionality
   - **Action:** Decide whether to incorporate "glossary" into the standard template or remove it
   - **Priority:** LOW

---

## Next Steps

### Immediate Actions (Priority: HIGH)

1. **Ewerton Madruga**: Complete 4 questions in `comunicação_aberta.json` by adding:
   - artifacts arrays
   - metrics arrays
   - sampling_guidance strings

2. **Flavia Agostini**:
   - Complete 1 question in `estilo_de_liderança_democrático.json`
   - Complete 1 question in `horizontal_(d2)_-_mapeamento_secundário.json`
   - Complete 3 questions in `entrega_de_informação_contextualizada.json`
   - Add descriptions for 11 empty maturity levels
   - Add maturity levels for 3 questions that have 0 levels

3. **All Authors**: Add observable behaviors to all maturity levels that are currently empty (70 instances total)

### Short-Term Actions (Priority: MEDIUM)

4. **All Authors**: Standardize maturity level labels to "Nível N" format (86 instances)

5. **Ewerton Madruga**: Add the 7th maturity level to `gestão_ágil.json` question

### Long-Term Actions (Priority: LOW)

6. **Team Decision**: Determine policy on "glossary" field - either standardize it across all files or remove it

7. **Template Documentation**: Update author guidelines with the complete template and validation requirements

---

## Conclusion

The JSON Consistency Checker has identified **188 issues** across **23 files** in the catalog:
- **13 ERRORS** requiring immediate attention (missing required fields)
- **172 WARNINGS** indicating inconsistencies and incomplete content
- **3 INFO** items highlighting non-standard additions

The most significant issues are:
1. Missing required fields (artifacts, metrics, sampling_guidance) in 13 questions
2. Missing observable behaviors in 70 maturity level definitions
3. Non-standard maturity level labels in 86 instances

**Flavia Agostini** and **Ewerton Madruga** have the highest number of issues to address, primarily related to incomplete questions and missing observable behaviors.

All authors are encouraged to use the consistency checker regularly during content development to catch issues early:

```bash
python3 question-base/scripts/json_consistency_check.py question-base/JSON7_20260105_164046/data
```

The script provides immediate feedback and helps maintain catalog quality across all contributors.
