# Configuração e Execução de Testes Unitários no Windows (ES2)

Este documento detalha o guia passo a passo para configurar o ambiente de desenvolvimento do **Paperless-ngx** no sistema operacional Windows e executar a suíte de testes de backend de forma isolada, utilizando banco de dados SQLite em memória para simplificar a infraestrutura local.

---

## 1. Ajustes de Compatibilidade do Ambiente (Windows)

Por padrão, as configurações do projeto limitam a resolução de dependências aos sistemas `linux` e `darwin`. Adicionalmente, a biblioteca `python-magic` depende de binários de sistema (`libmagic`) que não estão presentes nativamente no Windows.

Para resolver essas limitações e rodar o projeto no Windows, aplicamos as seguintes alterações:

1. **Atualização no [pyproject.toml](file:///d:/GitHub/ES2/paperless-ngx/pyproject.toml):**
   * Adicionamos a plataforma Windows (`win32`) na chave `environments` sob a tabela `[tool.uv]`:
     ```toml
     [tool.uv]
     required-version = ">=0.9.0"
     environments = [
       "sys_platform == 'darwin'",
       "sys_platform == 'linux'",
       "sys_platform == 'win32'", # Plataforma Windows adicionada
     ]
     ```
   * Adicionamos a biblioteca `python-magic-bin` condicionalmente para Windows para prover os binários do `libmagic`:
     ```toml
     dependencies = [
       ...
       "python-magic~=0.4.27",
       "python-magic-bin; sys_platform == 'win32'", # Binários da libmagic para Windows
       ...
     ]
     ```

2. **Geração do Lockfile Atualizado (`uv.lock`):**
   ```bash
   uv lock
   ```
   *Este comando atualizou o arquivo de travas adicionando as dependências de compatibilidade (como `python-magic-bin` e `pywin32`).*

3. **Sincronização do Ambiente Virtual:**
   ```bash
   uv sync --group testing
   ```
   *Instala todas as dependências de backend e bibliotecas de testes.*

---

## 2. Execução da Suíte de Testes com SQLite em Memória

Para rodar os testes unitários de maneira ágil, isolada e sem a necessidade de configurar um banco relacional externo (PostgreSQL/MariaDB), forçamos o sistema a utilizar o SQLite. O Django gerencia essa execução utilizando o banco de dados em memória `:memory:` nativamente.

Abra o terminal na pasta do projeto e use os comandos a seguir de acordo com a sua interface de linha de comando:

### A) PowerShell (Recomendado)
```powershell
# 1. Define a variável de ambiente para forçar o SQLite na sessão do PowerShell
$env:PAPERLESS_DBENGINE="sqlite"

# 2. Executa a suíte de testes via uv
uv run pytest
```

### B) Command Prompt (cmd.exe)
```cmd
# 1. Define a variável de ambiente no prompt
set PAPERLESS_DBENGINE=sqlite

# 2. Executa a suíte de testes
uv run pytest
```

### C) Bash (Git Bash / WSL / Linux)
```bash
PAPERLESS_DBENGINE=sqlite uv run pytest
```

---

## 3. Comandos Úteis para Otimização

* **Executar apenas um módulo de teste específico (ex: testes de expressões regulares):**
  ```powershell
  $env:PAPERLESS_DBENGINE="sqlite"
  uv run pytest src/documents/tests/test_regex.py
  ```

* **Executar um único teste específico em um arquivo:**
  ```powershell
  $env:PAPERLESS_DBENGINE="sqlite"
  uv run pytest src/documents/tests/test_regex.py::TestValidateRegexPattern::test_valid_pattern
  ```

* **Desabilitar execução paralela (Para fins de debug ou análise sequencial):**
  ```powershell
  $env:PAPERLESS_DBENGINE="sqlite"
  uv run pytest -p no:xdist
  ```

* **Acessar os Relatórios de Cobertura de Código:**
  Ao término de qualquer execução do pytest, os relatórios são salvos na raiz do repositório:
  * **HTML (Visual):** Abra o arquivo [htmlcov/index.html](file:///d:/GitHub/ES2/paperless-ngx/htmlcov/index.html) no navegador para auditar a cobertura linha a linha.
  * **XML (SonarQube/SonarCloud):** Localizado no arquivo [coverage.xml](file:///d:/GitHub/ES2/paperless-ngx/coverage.xml).
