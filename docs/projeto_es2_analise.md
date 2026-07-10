# Planejamento do Projeto Prático — Engenharia de Software II (Paperless-ngx)

Este documento reúne a análise técnica da estrutura do repositório do **Paperless-ngx** para auxiliar no planejamento do trabalho prático da disciplina de Engenharia de Software II (UFSCar).

---

## 1. Configuração e Ambiente (Docker / Docker Compose)

Para demonstração do sistema em execução local por meio de containers, as configurações e composições encontram-se centralizadas no diretório:
* [docker/compose/](file:///d:/GitHub/ES2/paperless-ngx/docker/compose/)

### Arquivos Disponíveis
* [docker-compose.sqlite.yml](file:///d:/GitHub/ES2/paperless-ngx/docker/compose/docker-compose.sqlite.yml): Configuração padrão simplificada usando SQLite e Valkey.
* [docker-compose.postgres.yml](file:///d:/GitHub/ES2/paperless-ngx/docker/compose/docker-compose.postgres.yml): Utiliza PostgreSQL como banco de dados relacional.
* [docker-compose.postgres-tika.yml](file:///d:/GitHub/ES2/paperless-ngx/docker/compose/docker-compose.postgres-tika.yml): **[Recomendado para demonstração]** Além do PostgreSQL, inclui os serviços adicionais Apache Tika (extração de texto) e Gotenberg (conversão de documentos Office), permitindo demonstrar a funcionalidade completa de ingestão de arquivos.

### Arquivo de Configuração Principal
* [docker-compose.env](file:///d:/GitHub/ES2/paperless-ngx/docker/compose/docker-compose.env): Contém todas as variáveis de ambiente que parametrizam o sistema (fuso horário, OCR, configurações de email e a chave secreta da aplicação).

### Passo a Passo Recomendado para Execução Local
1. Crie uma pasta temporária (ou utilize a raiz do repositório) e copie os seguintes arquivos do diretório `docker/compose/` para ela:
   * O compose selecionado (ex: `docker-compose.postgres-tika.yml`, renomeando-o para `docker-compose.yml`)
   * `.env`
   * `docker-compose.env`
2. Crie os diretórios locais para persistência e consumo de arquivos:
   ```bash
   mkdir consume export
   ```
3. Edite o arquivo `docker-compose.env` e defina um segredo forte em `PAPERLESS_SECRET_KEY`.
4. Inicie os containers com Docker Compose:
   ```bash
   docker compose pull
   docker compose up -d
   ```
5. Crie um superusuário administrador para acessar a interface web:
   ```bash
   docker compose run --rm webserver createsuperuser
   ```
6. Acesse a aplicação no navegador em `http://localhost:8000`.

---

## 2. Suíte de Testes Existente (Backend em Python)

Os testes automatizados do backend Python (Django) estão organizados dentro de subpastas `tests/` nos respectivos módulos em `src/`:
* **Documentos:** [src/documents/tests/](file:///d:/GitHub/ES2/paperless-ngx/src/documents/tests/)
* **Geral:** [src/paperless/tests/](file:///d:/GitHub/ES2/paperless-ngx/src/paperless/tests/)
* **Serviço de Email:** [src/paperless_mail/tests/](file:///d:/GitHub/ES2/paperless-ngx/src/paperless_mail/tests/)
* **Inteligência Artificial:** [src/paperless_ai/tests/](file:///d:/GitHub/ES2/paperless-ngx/src/paperless_ai/tests/)

A suíte utiliza o framework `pytest` com o plugin `pytest-django`, cujas opções padrões e de cobertura estão declaradas no [pyproject.toml](file:///d:/GitHub/ES2/paperless-ngx/pyproject.toml) sob a seção `[tool.pytest]`.

### Executando a Suíte de Testes e Gerando Relatório de Cobertura
Para rodar toda a suíte de testes de forma limpa, utilize a ferramenta **`uv`** (gerenciadora de dependências oficial do projeto) executando na raiz do repositório:

```bash
# Sincroniza e garante as dependências do grupo de teste instaladas
uv sync --group testing

# Roda os testes e calcula a cobertura de código
uv run pytest
```

Como o `pyproject.toml` já possui as configurações `--cov`, `--cov-report=html` e `--cov-report=xml` especificadas no parâmetro `addopts`, o comando gerará automaticamente:
* Um diretório `htmlcov/` (abra o arquivo `htmlcov/index.html` em seu navegador para ver a cobertura de forma visual e interativa por arquivo e linha).
* Um relatório `coverage.xml` estruturado (ideal para alimentar o SonarQube/SonarCloud).
* Um arquivo de sumário `junit.xml`.

---

## 3. Sugestão de Mudanças (M1 e M2)

Três sugestões de modificações pequenas, realistas e fáceis de testar com unitários no `pytest`:

### Sugestão 1: Validação Estrita de Formato Hexadecimal de Cores em Tags
* **Onde Alterar:** [src/documents/serialisers.py](file:///d:/GitHub/ES2/paperless-ngx/src/documents/serialisers.py#L688-L693) e [src/documents/models.py](file:///d:/GitHub/ES2/paperless-ngx/src/documents/models.py#L103)
* **Contexto:** No serializer de Tags, o validador de cor (`validate_color`) usa `re.match(r"#[0-9a-fA-F]{6}", color)`. A função `re.match` do Python testa apenas se o início da string é compatível, aceitando textos inválidos maiores como `"#a6cee3extra"` que estouram o limite da coluna do banco de dados (`max_length=7`).
* **Melhoria:** Alterar o padrão regex para usar âncoras estritas `r"^#[0-9a-fA-F]{6}$"` ou `re.fullmatch`. Adicionalmente, associar um `RegexValidator` no campo `color` da Model `Tag` para assegurar integridade no Django Admin.
* **Testes unitários:** Criar cenários de testes no `pytest` alimentando cores com formato incorreto (ex: `#123`, `a6cee3`, `#a6cee3extra`) e verificando se causam um `ValidationError`.

### Sugestão 2: Impedir Expirações no Passado para Links de Compartilhamento
* **Onde Alterar:** No [ShareLinkSerializer](file:///d:/GitHub/ES2/paperless-ngx/src/documents/serialisers.py#L2720) e [ShareLinkBundleSerializer](file:///d:/GitHub/ES2/paperless-ngx/src/documents/serialisers.py#L2748) em `serialisers.py`.
* **Contexto:** Atualmente, a API permite criar um `ShareLink` ou `ShareLinkBundle` cuja propriedade `expiration` (data de validade) esteja no passado (ex: ontem), resultando na criação de links imediatamente inutilizáveis.
* **Melhoria:** Criar um validador `validate_expiration(self, value)` nos serializers:
  ```python
  def validate_expiration(self, value):
      if value is not None and value <= timezone.now():
          raise serializers.ValidationError("Expiration date cannot be in the past.")
      return value
  ```
* **Testes unitários:** Criar um teste simulando uma requisição HTTP `POST` para criar o link de compartilhamento contendo uma data expirada e verificar o retorno `400 Bad Request`.

### Sugestão 3: Validação Rigorosa de Siglas de Moedas (ISO 4217) em CustomFields Monetários
* **Onde Alterar:** No [CustomFieldSerializer.validate](file:///d:/GitHub/ES2/paperless-ngx/src/documents/serialisers.py#L806-L822) em `serialisers.py`.
* **Contexto:** Ao criar um campo customizado do tipo monetário (`MONETARY`), o validador do serializer apenas checa se a string de `default_currency` possui 3 caracteres, permitindo valores inconsistentes como `"123"` ou `"usd"` (letras minúsculas).
* **Melhoria:** Modificar a condicional para validar que a moeda é composta estritamente de 3 letras maiúsculas utilizando a regex `r"^[A-Z]{3}$"`:
  ```python
  if not isinstance(currency, str) or not re.match(r"^[A-Z]{3}$", currency):
      raise serializers.ValidationError({"error": "default_currency must be a 3-letter uppercase ISO 4217 code."})
  ```
* **Testes unitários:** Criar cenários enviando siglas com letras minúsculas ou caracteres não-alfabéticos e asseverar a correta rejeição dos payloads.

---

## 4. Arquivos de Pipeline (GitHub Actions)

Os workflows do GitHub Actions originais encontram-se na pasta:
* [.github/workflows/](file:///d:/GitHub/ES2/paperless-ngx/.github/workflows/)

### Principais Arquivos de Referência para CI
* [ci-backend.yml](file:///d:/GitHub/ES2/paperless-ngx/.github/workflows/ci-backend.yml): Pipeline completo dos testes Python. É o melhor modelo para o projeto prático, pois mostra como inicializar dependências do Ubuntu (ex: `unpaper`, `tesseract-ocr`, `ghostscript`), instalar o `uv`, subir containers secundários de apoio (Valkey/Postgres), rodar o `pytest` e exportar relatórios de cobertura para o Codecov.
* [ci-lint.yml](file:///d:/GitHub/ES2/paperless-ngx/.github/workflows/ci-lint.yml): Workflow básico responsável por validar a formatação do código (`ruff` e `prek`).
* [ci-static-analysis.yml](file:///d:/GitHub/ES2/paperless-ngx/.github/workflows/ci-static-analysis.yml): Executa validações estáticas adicionais e análise de segurança de infraestrutura.
