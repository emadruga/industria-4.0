# JSON Consistency Check Report
**Date**: 2026-01-15 19:49:00
**Data Directory**: `question-base/JSON7_20260105_164046/data`

## Summary

- **Files processed**: 23
- **Valid files**: 22
- **Files with errors**: 1
- **Total issues**: 49 (1 error, 48 warnings, 0 info)

## Validation Status

✗ **Validation FAILED** - 1 error(s) found

---

## Issues by Author

### Cristiano Gurgel Castro (4 files)

**Files authored**:
- `data/Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho/desenvolvimento_profissional_contínuo.json`
- `data/Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho/reconhecer_o_valor_dos_erros.json`
- `data/Organização/Prontidão_de_Talentos/Aprendizado_e_Desenvolvimento_da_Força_de_Trabalho_(D13)/prover_competencias_digitais.json`
- `data/Processo/Operações/Cadeia_de_Suprimentos/Horizontal_(D2)/horizontal_(d2)_-_mapeamento_secundário.json`

#### Issues: 4 Warnings

**MATURITY_LEVEL_LABEL (4)**

`desenvolvimento_profissional_contínuo.json`:
- Expected label 'Nível 3', found 'Os líderes são formalmente cobrados por (ex' [questions[6].maturity_levels[3].label]

`reconhecer_o_valor_dos_erros.json`:
- Expected label 'Nível 6', found 'A cultura é autorregulada' [questions[1].maturity_levels[6].label]

`prover_competencias_digitais.json`:
- Expected label 'Nível 6', found 'A integração é completa' [questions[6].maturity_levels[6].label]

`horizontal_(d2)_-_mapeamento_secundário.json`:
- Expected label 'Nível 3', found 'A rastreabilidade é digital e parcial entre parceiros diretos (ex.' [questions[2].maturity_levels[3].label]

---

### Ewerton Madruga (6 files) ✅

**Files authored**:
- `data/Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/comunicação_aberta.json`
- `data/Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/cooperação_dentro_da_rede.json`
- `data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/abertura_à_inovação.json`
- `data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/confiança_em_processos_e_sistemas_de_informação.json`
- `data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/gestão_ágil.json`
- `data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/sistemas_de_metas_motivacionais.json`

#### Issues: 11 Warnings

**MATURITY_LEVEL_LABEL (11)**

`gestão_ágil.json`:
- Expected label 'Nível 0', found 'Não familiarizado' [questions[0].maturity_levels[0].label]
- Expected label 'Nível 1', found 'Familiarizado mas sem adoção' [questions[0].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Adoção piloto' [questions[0].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Adoção parcial' [questions[0].maturity_levels[3].label]
- Expected label 'Nível 4', found 'Adoção ampla' [questions[0].maturity_levels[4].label]
- Expected label 'Nível 5', found 'Adoção completa e otimizada' [questions[0].maturity_levels[5].label]
- Expected label 'Nível 6', found 'Referência e inovação contínua' [questions[0].maturity_levels[6].label]

`sistemas_de_metas_motivacionais.json`:
- Expected label 'Nível 4', found 'Metas são específicas, digitalizadas e revisadas regularmente (ex' [questions[8].maturity_levels[4].label]
- Expected label 'Nível 2', found 'Metas genéricas são formuladas, mas sem formalização (ex' [questions[8].maturity_levels[2].label]
- Expected label 'Nível 4', found 'A implementação segue ciclos formais de melhoria (ex' [questions[10].maturity_levels[4].label]
- Expected label 'Nível 6', found 'A implementação é ativamente ágil, usando ciclos curtos (ex' [questions[10].maturity_levels[6].label]

**Note**: All artifacts and metrics successfully reformatted to line-by-line format. No structural errors.

---

### Flavia Agostini (8 files)

**Files authored**:
- `data/Organização/Estrutura_e_Gestão/Colaboração_Inter_e_Intra-Empresarial/comunicação_eficiente.json`
- `data/Organização/Estrutura_e_Gestão/Competência_de_Liderança/estilo_de_liderança_democrático.json` ❌
- `data/Organização/Estrutura_e_Gestão/Estratégia_e_Governança/governança_de_dados.json`
- `data/Tecnologia/Automação/Chão_de_Fábrica/design_de_interfaces_orientado_à_tarefa.json`
- `data/Tecnologia/Conectividade/Chão_de_Fábrica/aquisição_de_dados_por_sensores_e_atuadores.json`
- `data/Tecnologia/Conectividade/Empresa/interface_de_dados_padronizada.json`
- `data/Tecnologia/Conectividade/Instalações/infraestrutura_de_ti_resiliente.json`
- `data/Tecnologia/Inteligência/Corporativo_(D11)/enterprise_(d11).json`

#### Issues: 1 Error, 18 Warnings

**ERRORS (1)** ❌

`estilo_de_liderança_democrático.json`:
- Missing question fields: `artifacts`, `sampling_guidance`, `metrics` [questions[7]]

**WARNINGS (18)**

**MATURITY_LEVEL_DESCRIPTION (7)**

`estilo_de_liderança_democrático.json`:
- Level 0 has empty description [questions[7].maturity_levels[0].description]
- Level 1 has empty description [questions[7].maturity_levels[1].description]
- Level 2 has empty description [questions[7].maturity_levels[2].description]
- Level 3 has empty description [questions[7].maturity_levels[3].description]
- Level 4 has empty description [questions[7].maturity_levels[4].description]
- Level 5 has empty description [questions[7].maturity_levels[5].description]
- Level 6 has empty description [questions[7].maturity_levels[6].description]

**OBSERVABLE_BEHAVIORS (7)**

`estilo_de_liderança_democrático.json`:
- Level 0 has no observable behaviors defined [questions[7].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 1 has no observable behaviors defined [questions[7].maturity_levels[1].evidence_signals.observable_behaviors]
- Level 2 has no observable behaviors defined [questions[7].maturity_levels[2].evidence_signals.observable_behaviors]
- Level 3 has no observable behaviors defined [questions[7].maturity_levels[3].evidence_signals.observable_behaviors]
- Level 4 has no observable behaviors defined [questions[7].maturity_levels[4].evidence_signals.observable_behaviors]
- Level 5 has no observable behaviors defined [questions[7].maturity_levels[5].evidence_signals.observable_behaviors]
- Level 6 has no observable behaviors defined [questions[7].maturity_levels[6].evidence_signals.observable_behaviors]

**MATURITY_LEVEL_LABEL (4)**

`enterprise_(d11).json`:
- Expected label 'Nível 0', found 'Sem infraestrutura de TI/TO para dados empresariais.' [questions[0].maturity_levels[0].label]
- Expected label 'Nível 1', found 'TI/TO isoladas (ex' [questions[0].maturity_levels[1].label]
- Expected label 'Nível 2', found 'Conectividade básica entre TI/TO e Enterprise (ex' [questions[0].maturity_levels[2].label]
- Expected label 'Nível 3', found 'Integração unidirecional (ex' [questions[0].maturity_levels[3].label]

---

### Wilson Melo Jr (5 files)

**Files authored**:
- `data/Processo/Ciclo_de_Vida_do_Produto/Ciclo_de_Vida_Integrado_do_Produto/foco_em_benefícios_ao_cliente.json`
- `data/Processo/Operações/Cadeia_de_Suprimentos/Vertical_(D1)/vertical_(d1)_-_primário.json`
- `data/Tecnologia/Inteligência/Chão_de_Fábrica/pré-processamento_descentralizado_de_dados_de_sensores.json`
- `data/Tecnologia/Inteligência/Empresa/análise_de_dados_automatizada.json`
- `data/Tecnologia/Inteligência/Empresa/entrega_de_informação_contextualizada.json`

#### Issues: 15 Warnings

**MATURITY_LEVEL_DESCRIPTION (4)**

`vertical_(d1)_-_primário.json`:
- Level 5 has empty description [questions[0].maturity_levels[5].description]
- Level 6 has empty description [questions[0].maturity_levels[6].description]
- Level 5 has empty description [questions[1].maturity_levels[5].description]
- Level 6 has empty description [questions[1].maturity_levels[6].description]

**MATURITY_LEVEL_LABEL (8)**

`pré-processamento_descentralizado_de_dados_de_sensores.json`:
- Expected label 'Nível 6', found 'Os sistemas embarcados executam processamento complexo em tempo real (ex' [questions[2].maturity_levels[6].label]

`análise_de_dados_automatizada.json`:
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

**OBSERVABLE_BEHAVIORS (3)**

`análise_de_dados_automatizada.json`:
- Level 0 has no observable behaviors defined [questions[1].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[2].maturity_levels[0].evidence_signals.observable_behaviors]
- Level 0 has no observable behaviors defined [questions[3].maturity_levels[0].evidence_signals.observable_behaviors]

---

## Summary by Author

| Author | Files | Errors | Warnings | Status |
|--------|-------|--------|----------|--------|
| **Ewerton Madruga** | 6 | 0 | 11 | ✅ Valid |
| **Cristiano Gurgel Castro** | 4 | 0 | 4 | ✅ Valid |
| **Wilson Melo Jr** | 5 | 0 | 15 | ✅ Valid |
| **Flavia Agostini** | 8 | 1 | 18 | ❌ Has Errors |

---

## Critical Action Items

### 🔴 Priority 1: Flavia Agostini

**File**: `estilo_de_liderança_democrático.json`
**Question**: #8

**Must Fix**:
1. Add missing required fields:
   - `artifacts` array
   - `sampling_guidance` string
   - `metrics` array

2. Complete maturity level descriptions for all 7 levels (0-6)

3. Add observable behaviors for all 7 maturity levels

---

## Recommendations

### Label Format Consistency

The majority of warnings (27 out of 48) are about maturity level labels not following the strict "Nível X" format. Consider:

1. **Option A**: Update all files to use standard "Nível X" labels
2. **Option B**: Modify the validator to accept descriptive labels as valid

**Rationale**: Descriptive labels may provide better context for users, but standard labels ensure consistency.

### Empty Descriptions

**Wilson Melo Jr**: Complete descriptions for levels 5-6 in `vertical_(d1)_-_primário.json`

### Observable Behaviors

Add observable behaviors for Level 0 maturity where missing:
- Wilson's `análise_de_dados_automatizada.json` (3 questions)

---

## Notes

✅ **Ewerton's Reformatting**: All 6 files successfully reformatted with line-by-line artifacts and metrics. No errors introduced.

⚠️ **Label Warnings**: Mostly stylistic and do not affect functionality. All files are structurally valid except for Flavia's incomplete question.

🎯 **Next Steps**: Focus on completing Flavia's `estilo_de_liderança_democrático.json` question #8 to achieve 100% validation success.
