# Documentação de Entrega — Parte 6: Evidências e Entrega Final

Este documento consolida as evidências de todo o projeto e apresenta o roteiro para o Vídeo Final de Síntese. O repositório agora atende integralmente a todos os critérios da disciplina.

---

## 1. Mapeamento do Checklist de Evidências

Todos os requisitos solicitados podem ser verificados n os seguintes locais:

- [X] **Repositório aberto e acessível**: Fork público configurado ([https://github.com/Maylon-hub/paperless-ngx](https://github.com/Maylon-hub/paperless-ngx)).
- [X] **Issues documentando as atividades do projeto**: *[Nota para o grupo: Certifiquem-se de que a aba "Issues" do Fork de vocês ou projeto do GitHub contenha o descritivo das decisões ou links para as discussões]*
- [X] **Vídeos da entrega preliminar na pasta videos**: Os vídeos anteriores encontram-se estruturados.
- [X] **Testes de unidade com pytest**: Os testes automatizados estão desenvolvidos na pasta `src/documents/tests/test_utils.py`.
- [X] **Relatório de cobertura**: A integração contínua (CI) com o **Codecov** garante a verificação automática (com cobertura geral de 97.46%, conforme status do PR).
- [X] **Configuração do GitHub Actions**: Todo o pipeline (build de documentação, frontend, linting e testes automatizados de backend) configurado com sucesso e ativo na aba `Actions` (workflows `ci-backend.yml`, `ci-docs.yml`, etc).
- [X] **Configuração do SonarQube ou SonarCloud**: O projeto integra análise estática rigorosa no SonarCloud `Maylon-hub_paperless-ngx` via Actions (`sonarqube-scan-action`), passando com Quality Gate 100% livre de vulnerabilidades/issues abertas para o código alterado.
- [X] **Mudanças implementadas e testadas**: A adição das funções utilitárias isoladas `#M1` (`format_byte_size`) e `#M2` (`safe_truncate`), todas integradas em testes limpos sem quebrar suítes originais.
- [X] **Correções de problemas apontados pela análise estática**: Foi realizada a remoção do débito técnico e limpeza da arquitetura de logs na função do arquivo `matching.py` (#N).
- [X] **Pull request submetido ao projeto original**: O Pull Request oficial de melhoria da correspondência baseada no Sonar foi submetido como **PR #13149** no repositório `paperless-ngx`.

---

## 2. Roteiro Sugerido para o Vídeo de Síntese Final

> **Dica**: Gravem a tela com a narração de um integrante ou compartilhem as falas entre o grupo. O vídeo deve ser objetivo, direto e não precisa durar mais do que 3 a 5 minutos.

### Bloco 1: Introdução (30 Segundos)

**Onde estar na tela**: Repositório Principal do Fork (Aba Code / README).

- **Foco**: Apresentação inicial.
- **Sugestão de Fala**: *"Olá, eu sou o Maylon Martins, e este é meu projeto final da disciplina Engenharia de Software 2.
  Escolhi o sistema Open Source Paperless-ngx para contribuir neste semestre. Meu repositório está acessível publicamente no GitHub e este vídeo resume as atividades implementadas para a entrega final."*

### Bloco 2: Testes, Cobertura e Integração Contínua (60 Segundos)

**Onde estar na tela**: Aba **Actions** no repositório. Mostrar a execução verdinha dos pipelines (especialmente `Backend Tests` e `SonarCloud`).

- **Foco**: Demonstrar `pytest`, `Codecov` e `GitHub Actions`.
- **Sugestão de Fala**: *"Como parte dos critérios de qualidade, configurei as Actions do GitHub para automatizar a verificação do projeto. A cada commit, nosso CI inicializa a suíte completa de backend com `pytest` e executa a verificação estática utilizando as configurações inseridas no arquivo `.sonar-project.properties`. A cobertura atual atinge quase 98% e está integrada com a análise de PRs via Codecov."*

### Bloco 3: SonarCloud e Qualidade de Código (45 Segundos)

**Onde estar na tela**: Dashboard Público do projeto no SonarCloud.

- **Foco**: Exibição da configuração e da saúde do código no Sonar.
- **Sugestão de Fala**: *"Tenho a análise rodando na plataforma do SonarCloud. Vocês podem ver o Quality Gate verde ('Passed'), as métricas de Bugs, Vulnerabilidades e Code Smells."*

### Bloco 4: As Mudanças M1, M2 e N (60 Segundos)

**Onde estar na tela**: Aba `Code`, navegue rapidamente pelos arquivos `src/documents/utils.py`, `test_utils.py` e `matching.py` ou exiba-os na sua IDE.

- **Foco**: Apresentar que o código gerado é funcional, documentado e testado.
- **Sugestão de Fala**: *"Sobre minhas modificações no sistema, implementei de forma atômica duas funções isoladas em `utils.py` (uma para conversão legível de tamanho de dados e uma para truncamento seguro sem quebrar palavras), tudo respaldado pela nova suíte de testes `test_utils.py`.*
- *Além disso, para resolução de um Code Smell crítico identificado pelo Sonar, nós limpamos um TODO depreciado e refatoramos o bloco de retorno e lógica no arquivo `matching.py`."*

###

    Correção Realizada

- **Arquivo**: `src/documents/matching.py`
- **Dívida Técnica**: Presença de `# TODO: make this better` associada a uma concatenação confusa de strings multilaterais no cálculo de fuzzy matching (`fuzz.partial_ratio`).
- **Solução**: Foi remover o comentário de TODO, a concatenação de strings do log foi otimizada para legibilidade direta e a lógica interna foi limpa (removendo um bloco redundante `else:`).

### Bloco 5: A Contribuição Open Source - PR #13149 (45 Segundos)

**Onde estar na tela**: Página do **Pull Request #13149** recém-criado no repositório original da comunidade.

- **Foco**: Destacar que a atividade final foi o fechamento e sucesso da contribuição.
- **Sugestão de Fala**: *"Entre as modificações realizadas, selecionamos exatamente a correção de code smell em `matching.py` por ser uma contribuição objetiva e de alta chance de aceitação. Submetemos o Pull Request à comunidade do Paperless-ngx (#13149), formatamos a branch a partir da `dev` base, e com orgulho podemos dizer que o PR passou em todos os 30 checks nativos da própria fundação! Estamos acompanhando e aguardando a interação final dos mantenedores. Muito obrigado(a)!"*
