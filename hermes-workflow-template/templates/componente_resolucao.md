# COMPONENTE_RESOLUÇÃO.md

## Task: [Task Description from queue.txt]
## Workspace: [path/to/workspace]
## Timestamp: [ISO timestamp of completion]

## ✅ Itens Concluídos
[Each item should correspond to a checkbox from the development plan or a quality gate]

- [ ] Funcionalidade principal implementada conforme especificação inicial
- [ ] Nenhum erro de linting restante (score: 100/100)
- [ ] Cobertura de testes: [X]% (meta: ≥85%)
- [ ] Todos os testes unitários passando
- [ ] Todos os testes de integração passando (se aplicável)
- [ ] Testes de ponta a ponta passando (se aplicável)
- [ ] Documentação atualizada (se aplicável)
- [ ] Código revisado e aderente aos padrões do projeto
- [ ] Nenhuma vulnerabilidade de segurança óbvia introduzida
- [ ] Performance dentro dos limites aceitáveis (se métricas definidas)

## 📊 Métricas Finais
- **Tempo total estimado vs real**: [Estimado: X min / Real: Y min]
- **Arquivos modificados**: [lista de arquivos com contagem de linhas adicionadas/removidas]
- **Dependências adicionadas**: [lista de novas dependências, se houver]
- **Linhas de código adicionadas**: [number]
- **Linhas de código removidas**: [number]
- **Score de linter final**: [X]/100
- **Cobertura de testes final**: [X]%
- **Número de testes executados**: [unit: X, integration: Y, e2e: Z]

## 🔍 Histórico de Correções
[Optional: Brief summary of major iterations if there were multiple 2.0→2.3 cycles]

### Ciclo 1
- Problemas encontrados: [lista resumida]
- Correções aplicadas: [lista resumida]

### Ciclo 2 (se aplicável)
- Problemas encontrados: [lista resumida]
- Correções aplicadas: [lista resumida]

## 🎯 STATUS GERAL
[This is the critical field that determines if the task is done]

**STATUS: [CONCLUÍDO / PENDENTE]**

### Condições para CONCLUÍDO
Todos os checkboxes acima devem estar marcados [x] e o status explicitamente definido como "CONCLUÍDO".

Se algum item estiver [ ] ou o status for "PENDENTE", a tarefa retornará para a fase de desenvolvimento (2.0) para resolver as pendências específicas listadas.

## ⚠️ Pendências Específicas (se STATUS: PENDENTE)
[Only fill this section if status is PENDENTE - otherwise leave blank or remove]

1. [Specific issue from audit report that needs fixing]
2. [Specific failing test case that needs to be addressed]
3. [Any other blocker]

## 📎 Artefatos Gerados
- Context summary: `context_summary.md`
- Research output: `research_output.md` (≈[X] linhas)
- Development plan: `development_plan.md`
- Audit report: `audit_report.md`
- Test results: `test_results/` directory
- Source code: `source_code/` directory

## ✉️ Notificação
[This section can be used by the orchestrator to determine what to communicate]
- **Task completed**: [true/false]
- **Notification message**: [Optional custom message for user]