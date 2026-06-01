# Hermes Workflow Template

Este é um modelo reutilizável para o workflow estruturado de desenvolvimento autônomo do Hermes Agent.

## Como usar
1. Copie esta pasta inteira para a raiz do seu projeto (ex: `/root/seuprojeto/hermes-workflow-template/`).
2. Certifique-se de que o skill `structured-implementation-workflow` está instalado e configurado.
3. Crie um arquivo `queue.txt` na raiz do projeto com as tarefas a serem processadas (uma por linha).
4. O orchestrator cron job irá processar cada tarefa usando os templates e scripts desta pasta.

## Estrutura
- `templates/` - Arquivos modelo para cada fase do workflow
- `scripts/` - Scripts auxiliares de validação e execução
- `docs/` - Documentação detalhada do workflow
- `phases/` - (Opcional) Definições específicas de fase se necessário

## Templates
Cada template deve ser copiado e preenchido pelo workflow durante a execução de uma tarefa.

### templates/context_summary.md
Resumo do contexto do projeto para a tarefa atual.

### templates/research_output.md
Resultado da pesquisa (400-800 linhas) com documentação oficial, exemplos de código similares e análise.

### templates/development_plan.md
Plano de desenvolvimento atomizado no formato de checklist.

### templates/audit_report.md
Relatório de auditoria de qualidade (linting, padrões, etc.).

### templates/test_results/
Diretório para logs de testes (unit, lint, e2e).

### templates/componente_resolucao.md
Documento final de resolução com status da tarefa.

## Scripts
- `scripts/validate_research_depth.py` - Verifica se a pesquisa atingiu o tamanho mínimo e qualidade.
- `scripts/validate_plan_atomization.py` - Garante que o plano esteja devidamente atomizado.
- `scripts/run_audit.py` - Executa linters apropriados para o projeto.
- `scripts/run_tests.py` - Executa testes unitários, de integração e e2e.

## Integração com Hermes
O skill `structured-implementation-workflow` espera encontrar esta estrutura em `<project_root>/hermes-workflow-template/`.
Ele usa os templates como ponto de partida e os scripts para validação entre fases.