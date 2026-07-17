# Tarefas: Testes, Cobertura e SonarCloud

- `[/]` 1. **Setup e Cobertura Base**
  - `[x]` Iniciar os serviços locais do Docker para testes (`docker compose --file docker/compose/docker-compose.ci-test.yml up -d`).
  - `[x]` Instalar dependências necessárias (`nltk.downloader`).
  - `[/]` Executar `pytest --cov=src --cov-report=xml --cov-report=html` para gerar a baseline de cobertura.
- `[x]` 2. **Configuração do SonarCloud**
  - `[x]` Adicionar `sonar-project.properties`.
  - `[x]` Modificar `ci-backend.yml` ou `ci-static-analysis.yml` para rodar o SonarCloud Scan.
- `[ ]` 3. **Melhorar a Cobertura**
  - `[ ]` Analisar o relatório gerado.
  - `[ ]` Implementar testes para aumentar a cobertura no módulo escolhido.
  - `[ ]` Rodar `pytest` novamente e verificar se os testes passam e a cobertura aumenta.
- `[ ]` 4. **Verificação e Roteiro**
  - `[ ]` Gerar evidências do funcionamento (Walkthrough).
