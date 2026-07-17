# Roteiro do Vídeo de Entrega Preliminar (ES2)

Este roteiro serve como guia passo a passo para a gravação dos vídeos de demonstração da **Entrega Preliminar** da disciplina de Engenharia de Software II.

O vídeo deve ser curto, objetivo, gravado em um ambiente limpo (começando preferencialmente do `git clone`) e salvo na pasta `videos/` na raiz do repositório.

---

## Estrutura Geral do Vídeo

- **Duração Recomendada:** 3 a 5 minutos.
- **Resolução:** 1080p.
- **Divisão:**
  1. Apresentação inicial do grupo e do sistema escolhido (Paperless-ngx).
  2. Demonstração de Build e Testes (#F).
  3. Demonstração do Sistema em Execução (#G).

---

## Bloco 1: Introdução (30 segundos)

- **O que falar:**
  > _"Olá, professor! Somos o grupo [Nomes dos Integrantes] da disciplina de Engenharia de Software II. O sistema de código aberto que escolhemos para analisar, testar e estender é o Paperless-ngx, um sistema robusto de gerenciamento de documentos. Neste vídeo, demonstraremos a configuração do ambiente, execução de testes unitários locais e o sistema funcionando em containers Docker."_

---

## Bloco 2: Build e Testes — #F (1.5 a 2 minutos)

Este bloco demonstra que o grupo conseguiu configurar a suíte de testes e o interpretador local no Windows.

### Passos a Demonstrar na Tela

1. **Abertura do Terminal (PowerShell):**
   Mostre o terminal na raiz do projeto clonado.
2. **Explicar a adaptação para Windows:**
   Mostre brevemente o arquivo [pyproject.toml](file:///d:/GitHub/ES2/paperless-ngx/pyproject.toml) modificado, explicando:
   - _"Para rodar o projeto no Windows, adicionamos a plataforma `win32` no gerenciador `uv` e incluímos a biblioteca `python-magic-bin` para prover a dependência nativa `libmagic` do Windows."_

3. **Restaurar Dependências (Build do ambiente):**
   Rode o comando no terminal:

   ```powershell
   uv sync --group testing
   ```

   _Mostre o `uv` confirmando que todas as dependências estão resolvidas e instaladas._

4. **Executar Testes Unitários de Forma Isolada (Banco em Memória):**
   Explique que, para rodar os testes sem a necessidade de um banco PostgreSQL rodando localmente, usamos o SQLite em memória.
   Digite e execute os comandos:

   ```powershell
   $env:PAPERLESS_DBENGINE="sqlite"
   uv run pytest src/documents/tests/test_regex.py
   ```

   _Mostre a execução do pytest coletando e passando com sucesso nos 20 testes unitários de expressão regular do sistema._

---

## Bloco 3: Execução do Sistema — #G (1.5 a 2 minutos)

Este bloco demonstra que o sistema foi configurado corretamente e está funcional com interface web e banco de dados persistente.

### Passos a Demonstrar na Tela

1. **Preparação dos Arquivos de Compose:**
   Copie os arquivos necessários da pasta de composição para a raiz (ou mostre como rodar diretamente a partir da pasta de compose):

   ```powershell
   # Copiar o compose recomendado para a raiz
   Copy-Item docker/compose/docker-compose.postgres-tika.yml docker-compose.yml
   Copy-Item docker/compose/docker-compose.env docker-compose.env
   Copy-Item docker/compose/.env .env
   ```

2. **Ajuste da Chave Secreta:**
   Abra o arquivo `docker-compose.env` no VS Code e altere a linha:

   ```env
   PAPERLESS_SECRET_KEY=change-me-para-um-segredo-qualquer
   ```

3. **Criação das pastas de volumes:**

   ```powershell
   mkdir consume, export
   ```

4. **Subir os Containers:**
   Rode o comando do docker:

   ```powershell
   docker compose up -d
   ```

   _Mostre os containers (webserver, db, broker, gotenberg, tika) subindo com sucesso no terminal ou no Docker Desktop._

5. **Criação de Usuário Administrador (Crucial para o Login):**

   ```powershell
   docker compose run --rm webserver createsuperuser
   ```

   _Digite um usuário (ex: `admin`), email e senha em tempo real na gravação._

6. **Demonstração na Interface Gráfica:**
   - Abra o navegador em `http://localhost:8000`.
   - Faça login com a conta criada.
   - **Ação Prática:** Faça upload de um arquivo PDF qualquer de teste arrastando-o para a interface. Mostre que o sistema inicia a fila de processamento (consumo) do documento e o exibe no painel principal indexado e pesquisável.

---

## Bloco 4: Encerramento (30 segundos)

- **O que falar:**
  > _"Com isso, demonstramos que o Paperless-ngx está completamente configurado localmente no Windows, com a suíte de testes unitários pronta para validar nossas futuras melhorias e o sistema operando em ambiente Docker persistente. Agradecemos a atenção!"_
