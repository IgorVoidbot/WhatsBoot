## 10. Lista de Tarefas — Sprints de Desenvolvimento

> **Legenda:** `[ ]` = Pendente | `[x]` = Concluído

---

### Sprint 0 — Setup e Infraestrutura

**Objetivo:** Ambiente de desenvolvimento funcional e serviços de infraestrutura rodando.

#### Tarefa 0.1 — Configuração do Repositório e Ambiente Python
- [x] **0.1.1** Criar o diretório raiz `whatsboot/` com a estrutura de arquivos definida na arquitetura. ✅ *Todos os módulos criados: `app.py`, `chains.py`, `config.py`, `evolution_api.py`, `memory.py`, `message_buffer.py`, `prompts.py`, `vectorstore.py`*
- [X] **0.1.2** Inicializar o ambiente virtual Python (`python -m venv .venv`) e ativar.
- [x] **0.1.3** Atualizar o `requirements.txt` substituindo dependências OpenAI pelas especificadas: `fastapi`, `uvicorn[standard]`, `langchain`, `langchain-google-genai`, `langchain-chroma`, `langchain-community`, `redis`, `chromadb`, `httpx`, `pypdf`, `python-dotenv`, `tenacity`. ✅
- [x] **0.1.4** Criar o arquivo `.env.example` com as variáveis necessárias: `GEMINI_API_KEY`, `REDIS_URL`, `EVOLUTION_API_URL`, `EVOLUTION_API_KEY`, `WEBHOOK_SECRET`, `DEBOUNCE_SECONDS`, `HISTORY_TTL_SECONDS`. ✅
- [x] **0.1.5** Criar o arquivo `.gitignore` incluindo `.env`, `.venv/`, `__pycache__/`, `chroma_data/`, `rag_files/`. ✅ *`.gitignore` completo presente*

#### Tarefa 0.2 — Docker Compose e Serviços de Infraestrutura
- [x] **0.2.1** Criar o `docker-compose.yml` com o serviço `redis` (imagem `redis:latest`, porta `6379`, volume persistente). ✅
- [x] **0.2.2** Adicionar ao `docker-compose.yml` o serviço `evolution-api` (imagem `atendai/evolution-api:v2.1.1`, porta `8080`, dependência do Postgres e Redis). ✅
- [x] **0.2.3** Adicionar ao `docker-compose.yml` o serviço `postgres` (imagem `postgres:15`) como dependência da Evolution API. ✅
- [x] **0.2.4** Adicionar ao `docker-compose.yml` o serviço `bot` (build do `Dockerfile`, porta `8000`, volumes para `rag_files/` e `vectorstore_data/`). ✅
- [x] **0.2.5** Criar o `Dockerfile` para o serviço `bot`: base `python:3.13`, instalação de dependências via `requirements.txt`, entrypoint com `uvicorn app:app`. ✅
- [ ] **0.2.6** Validar que `docker-compose up` sobe todos os serviços sem erros. Testar conexão Redis com `redis-cli ping` e healthcheck do bot em `GET /health`. ⚠️ *Config YAML validado com sucesso. Requer Docker Desktop em execução para subir os serviços e testar.*

#### Tarefa 0.3 — Arquivo de Configuração de Tenants
- [x] **0.3.1** Criar o `tenants.json` com estrutura inicial contendo dois tenants de exemplo: `clinica_a` e `oficina_b`, com campos `instance_name`, `tenant_id`, `display_name`, `system_prompt`, `rag_dir`, `debounce_seconds`, `history_ttl_seconds`. ✅
- [x] **0.3.2** Criar os diretórios `rag_files/clinica_a/` e `rag_files/oficina_b/` com arquivos `.txt` de exemplo para testes. ✅

---

### Sprint 1 — Módulos Core (Config, Modelos e Utilitários)

**Objetivo:** Módulos de configuração e modelos de dados prontos, testáveis e injetáveis via FastAPI.

#### Tarefa 1.1 — Módulo `config.py`
- [ ] **1.1.1** Implementar função `load_env() -> None` que carrega variáveis do `.env` via `python-dotenv` e valida a presença das obrigatórias, lançando `ValueError` com mensagem descritiva se alguma estiver ausente. ⚠️ *`config.py` carrega variáveis mas sem validação de presença — apenas `os.getenv()` sem checagem.*
- [ ] **1.1.2** Implementar `dataclass` ou `TypedDict` `TenantConfig` com todos os campos de um tenant: `instance_name: str`, `tenant_id: str`, `display_name: str`, `system_prompt: str`, `rag_dir: str`, `debounce_seconds: int`, `history_ttl_seconds: int`. ⚠️ *Não existe — configuração atual é single-tenant via variáveis de ambiente.*
- [ ] **1.1.3** Implementar função `load_tenants(path: str = 'tenants.json') -> dict[str, TenantConfig]` que lê o JSON, parseia cada entrada como `TenantConfig` e retorna um dicionário indexado por `instance_name`.
- [ ] **1.1.4** Implementar função de dependência FastAPI `get_tenant_config(instance_name: str, tenants: dict = Depends(get_tenants)) -> TenantConfig` que busca o tenant ou lança `HTTPException(404)`.
- [ ] **1.1.5** Escrever testes unitários básicos para `load_tenants`: tenant válido, tenant ausente, JSON malformado.

#### Tarefa 1.2 — Modelos Pydantic para Webhook
- [ ] **1.2.1** Criar arquivo `models.py` com o modelo Pydantic `WebhookPayload` mapeando os campos relevantes do payload da Evolution API: `event: str`, `instance: str`, `data.key.remoteJid: str`, `data.message.conversation: str | None`, `data.message.extendedTextMessage.text: str | None`. ⚠️ *`app.py` atual usa acesso via dicionário sem validação — sujeito a `KeyError` e `AttributeError`.*
- [ ] **1.2.2** Implementar método `get_phone_number() -> str` no modelo que extrai e normaliza o número de telefone (remove `@s.whatsapp.net`, mantém apenas dígitos).
- [ ] **1.2.3** Implementar método `get_message_text() -> str | None` que retorna o texto da mensagem independente do tipo (`conversation` ou `extendedTextMessage`).

---

### Sprint 2 — Redis: Debounce e Histórico

**Objetivo:** Módulos de buffer de debounce e histórico de conversas implementados e testados de forma assíncrona.

#### Tarefa 2.1 — Conexão Assíncrona com Redis
- [ ] **2.1.1** Em `config.py`, implementar função de dependência FastAPI `get_redis_client() -> redis.asyncio.Redis` que cria e retorna um cliente Redis assíncrono configurado via `REDIS_URL`. ⚠️ *`redis_client` existe mas é instanciado no escopo do módulo `message_buffer.py`, não como dependência injetável do FastAPI.*
- [ ] **2.1.2** Garantir que a conexão Redis é testada no startup do FastAPI (`lifespan`) com log de sucesso ou falha.

#### Tarefa 2.2 — Módulo `message_buffer.py` (Debounce)
- [x] **2.2.1** Implementar função assíncrona `append_message` que adiciona a mensagem ao final de uma lista Redis com chave `buffer:{tenant_id}:{phone}` e define TTL. ✅ *Feito via `redis_client.rpush(buffer_key, message)` + `redis_client.expire(buffer_key, BUFFER_TTL)`*
- [ ] **2.2.2** Implementar função assíncrona `set_debounce_timer` que define ou reseta uma chave de timer no Redis com `SET ... EX seconds NX`. ⚠️ *Implementação atual usa `asyncio.Task` em memória (`debounce_tasks` dict) — não sobrevive a restart e não é thread-safe em múltiplos workers. Precisa migrar para timer Redis com `NX`.*
- [x] **2.2.3** Implementar função assíncrona `flush_buffer` que lê todos os itens da lista de buffer com `LRANGE`, concatena e deleta a chave atomicamente. ✅ *Feito em `handle_debounce`: `lrange(buffer_key, 0, -1)` + `delete(buffer_key)`*
- [x] **2.2.4** Implementar a lógica principal de processamento: acumular mensagem → verificar timer → criar task de debounce com `asyncio.create_task`. ✅ *Feito em `buffer_message()`*
- [x] **2.2.5** Garantir que o callback do debounce chama `flush_buffer` antes de invocar o pipeline RAG. ✅ *`handle_debounce` lê e deleta o buffer antes de invocar a chain*
- [ ] **2.2.6** Escrever testes unitários com `fakeredis` para: acúmulo de mensagens, reset de timer, flush correto após timeout.

#### Tarefa 2.3 — Módulo `memory.py` (Histórico de Conversas)
- [x] **2.3.1** Implementar função `get_session_history` que instancia `RedisChatMessageHistory` do LangChain com URL e session_id configurados. ✅ *`get_session_history(session_id)` presente e funcional*
- [ ] **2.3.2** Garantir que a chave do histórico é prefixada por `tenant_id` para isolamento completo. ⚠️ *Chave atual usa apenas o `chat_id` sem prefixo de tenant — risco de colisão entre tenants.*
- [ ] **2.3.3** Implementar função assíncrona `clear_history(tenant_id: str, phone: str, redis_client) -> None` para eventual reset manual do histórico.
- [ ] **2.3.4** Testar que históricos de tenants diferentes não colidem mesmo com o mesmo número de telefone.

---

### Sprint 3 — Vector Store: ChromaDB e Ingestão de Documentos

**Objetivo:** Pipeline de ingestão de documentos e retrieval vetorial por tenant implementados e isolados.

#### Tarefa 3.1 — Módulo `vectorstore.py`
- [ ] **3.1.1** Implementar função `get_chroma_client(persist_directory: str = 'chroma_data') -> chromadb.Client` que retorna um cliente ChromaDB persistente com SQLite. ⚠️ *`vectorstore.py` usa `Chroma` do LangChain diretamente, sem expor o cliente nativo — necessário para gerenciar collections por tenant.*
- [ ] **3.1.2** Implementar função `get_tenant_collection_name(tenant_id: str) -> str` que retorna o nome padronizado da collection: `tenant_{tenant_id}`. ⚠️ *Não existe — sistema atual usa uma única collection compartilhada.*
- [ ] **3.1.3** Implementar função `get_embedding_function() -> GoogleGenerativeAIEmbeddings` que instancia o modelo de embeddings do Gemini configurado via `GEMINI_API_KEY`. ⚠️ *Atual usa `OpenAIEmbeddings` — precisa migrar para `GoogleGenerativeAIEmbeddings`.*
- [ ] **3.1.4** Refatorar `get_vectorstore(tenant_id: str) -> Chroma` para aceitar `tenant_id` e conectar à collection exclusiva do tenant. ⚠️ *Função existe (`get_vectorstore()`) mas sem parâmetro de tenant — usa collection única.*
- [ ] **3.1.5** Implementar função de dependência FastAPI `get_retriever(tenant_id: str) -> VectorStoreRetriever` que retorna um retriever configurado com `search_type='mmr'`, `k=4` e filtro por metadado de `tenant_id`.

#### Tarefa 3.2 — Script de Ingestão de Documentos
- [ ] **3.2.1** Criar o script `ingest.py` (executável via `python ingest.py --tenant clinica_a`) que aceita o argumento `--tenant` (ou `--all` para todos os tenants). ⚠️ *Lógica de ingestão está acoplada dentro de `get_vectorstore()` — precisa ser extraída para um script dedicado e separado do runtime.*
- [x] **3.2.2** Implementar função `load_documents(rag_dir: str) -> list[Document]` que usa `PyPDFLoader` para PDFs e `TextLoader` para TXTs. ✅ *Feito em `vectorstore.py`: `load_documents()` com suporte a `.pdf` e `.txt`*
- [x] **3.2.3** Implementar função `split_documents(documents: list[Document]) -> list[Document]` usando `RecursiveCharacterTextSplitter` com `chunk_size` e `chunk_overlap` configuráveis. ✅ *Feito dentro de `get_vectorstore()` com `chunk_size=1000`, `chunk_overlap=200`*
- [ ] **3.2.4** Implementar função `ingest_to_chroma(tenant_id: str, chunks: list[Document]) -> None` que insere os chunks na collection do tenant com metadado `tenant_id` em cada chunk, evitando duplicatas. ⚠️ *Atual não adiciona metadado de tenant aos chunks nem previne duplicatas.*
- [ ] **3.2.5** Adicionar log de progresso durante a ingestão: total de arquivos, total de chunks gerados, tempo de execução.
- [ ] **3.2.6** Testar ingestão com os arquivos de exemplo de `clinica_a` e validar que chunks aparecem na collection correta do ChromaDB.

---

### Sprint 4 — LangChain: Prompts, Chain e Orquestração RAG

**Objetivo:** Pipeline RAG completo, conversacional, assíncrono e isolado por tenant.

#### Tarefa 4.1 — Módulo `prompts.py`
- [ ] **4.1.1** Definir o template de prompt de sistema base `BASE_SYSTEM_PROMPT` em português, instruindo o LLM a: responder apenas com base no contexto fornecido, ser conciso, não inventar informações, e usar o `system_prompt` do tenant como especialização. ⚠️ *Prompts atuais são carregados do `.env` como string global — sem suporte a `system_prompt` por tenant.*
- [x] **4.1.2** Definir o `ChatPromptTemplate` principal `RAG_PROMPT` combinando: system prompt, histórico e input do usuário. ✅ *`qa_prompt` e `contextualize_prompt` implementados com `ChatPromptTemplate` e `MessagesPlaceholder`*
- [ ] **4.1.3** Definir o template de fallback `FALLBACK_PROMPT` para quando não há contexto relevante nos documentos, instruindo o bot a informar a limitação sem alucinações.

#### Tarefa 4.2 — Módulo `chains.py`
- [x] **4.2.1** Implementar função `build_rag_chain` que constrói a chain LangChain com `history_aware_retriever`, prompt RAG, LLM e output parser. ✅ *`get_rag_chain()` e `get_conversational_rag_chain()` implementados com `create_history_aware_retriever`, `create_stuff_documents_chain` e `RunnableWithMessageHistory`*
- [ ] **4.2.2** Configurar o LLM para usar `ChatGoogleGenerativeAI` com `model='gemini-1.5-flash'`, `temperature=0.3`, `max_output_tokens=512`. ⚠️ *Atual usa `ChatOpenAI` — precisa migrar para `langchain-google-genai`.*
- [ ] **4.2.3** Extrair e isolar função assíncrona `invoke_rag_chain(chain, tenant_config, user_input: str) -> str` que recebe a chain já construída e retorna apenas o texto da resposta. ⚠️ *Invocação da chain está acoplada dentro de `message_buffer.py` (`handle_debounce`) — precisa ser isolada em `chains.py`.*
- [ ] **4.2.4** Adicionar tratamento de exceção em `invoke_rag_chain`: capturar `Exception`, logar com `tenant_id` + contexto e retornar `None` para sinalizar falha ao caller.
- [ ] **4.2.5** Implementar callback do LangChain `TokenUsageCallback` para logar o consumo de tokens por invocação com `tenant_id`.

---

### Sprint 5 — Evolution API: Integração de Envio

**Objetivo:** Módulo de envio de mensagens para o WhatsApp confiável e com retry.

#### Tarefa 5.1 — Módulo `evolution_api.py`
- [ ] **5.1.1** Refatorar `send_whatsapp_message` para ser assíncrona (`async def`), aceitar `instance_name` como parâmetro e usar `httpx.AsyncClient` em vez de `requests`. ⚠️ *Função atual é síncrona com `requests.post()` e usa `EVOLUTION_INSTANCE_NAME` hardcoded do env — incompatível com multi-tenant.*
- [ ] **5.1.2** Implementar retry simples com `tenacity`: 3 tentativas, espera exponencial de 1s, 2s, 4s, capturando `httpx.HTTPError`.
- [ ] **5.1.3** Implementar função assíncrona `send_fallback_message(instance_name: str, phone: str, api_url: str, api_key: str) -> None` que envia a mensagem de fallback padrão ao usuário.
- [ ] **5.1.4** Garantir que `send_text_message` loga o status HTTP da resposta (sucesso e falha) com `tenant_id` e `phone`.
- [ ] **5.1.5** Criar dependência FastAPI `get_evolution_config() -> dict` que retorna `EVOLUTION_API_URL` e `EVOLUTION_API_KEY` das variáveis de ambiente.

---

### Sprint 6 — FastAPI: Entrypoint, Webhook e Wiring Final

**Objetivo:** Aplicação FastAPI completamente integrada, com roteamento de webhook e injeção de dependências.

#### Tarefa 6.1 — Módulo `app.py`
- [ ] **6.1.1** Inicializar a aplicação FastAPI com `title='WhatsBoot'`, `version='1.0.0'` e lifespan assíncrono (`@asynccontextmanager`) para startup (conectar Redis, logar tenants carregados) e shutdown (fechar conexões). ⚠️ *`app.py` atual usa `FastAPI()` simples sem lifespan.*
- [ ] **6.1.2** Refatorar o endpoint para `POST /webhook/{instance_name}`, adicionando: validação do header `X-Webhook-Token` contra `WEBHOOK_SECRET`; parse do body como `WebhookPayload`; verificação do evento `messages.upsert`; filtro `fromMe: true`. ⚠️ *Endpoint atual é `/webhook` (sem `instance_name`), sem auth e sem filtros.*
- [ ] **6.1.3** No handler do webhook, extrair `phone_number` e `message_text` via métodos do modelo `WebhookPayload`, com log estruturado de `instance_name`, `tenant_id`, `phone`. ⚠️ *Atual usa `data.get('data').get('key').get('remoteJid')` — sem modelo, sem validação, sem log.*
- [x] **6.1.4** Chamar `buffer_message` (debounce) do `message_buffer.py` passando o callback assíncrono que executa o pipeline completo. ✅ *`buffer_message(chat_id, message)` é chamado no handler atual*
- [x] **6.1.5** Retornar `HTTP 200 OK` imediatamente após enfileirar o processamento via `asyncio.create_task`, para que a Evolution API não reenvie o webhook por timeout. ✅ *`return {'status': 'ok'}` imediato presente*
- [ ] **6.1.6** Implementar o callback do pipeline completo como função assíncrona isolada: `flush_buffer` → `get_chat_history` → `build_rag_chain(tenant_config)` → `invoke_rag_chain` → `send_text_message` (ou `send_fallback_message` em falha). ⚠️ *Pipeline atual está acoplado em `handle_debounce` no `message_buffer.py`, sem separação de responsabilidades e sem multi-tenant.*
- [ ] **6.1.7** Adicionar endpoint `GET /health` retornando status do Redis e lista de tenants carregados, para uso em healthcheck do Docker.

#### Tarefa 6.2 — Testes de Integração
- [ ] **6.2.1** Criar `tests/test_webhook.py` com `TestClient` do FastAPI simulando um payload de webhook válido e verificando que a resposta é `200 OK` imediato.
- [ ] **6.2.2** Criar `tests/test_debounce.py` verificando o agrupamento de 3 mensagens consecutivas resultando em 1 única invocação do pipeline (usando `fakeredis` e mock do pipeline).
- [ ] **6.2.3** Criar `tests/test_tenant_isolation.py` verificando que mensagens de tenants diferentes não contaminam os buffers e históricos um do outro.
- [ ] **6.2.4** Criar `tests/test_rag_chain.py` com mock do Gemini verificando que o retriever correto do tenant é usado e que a resposta de fallback é gerada quando o LLM retorna `None`.

---

### Sprint 7 — Observabilidade, Polimento e Documentação

**Objetivo:** Sistema pronto para produção com logs estruturados, documentação e configuração robusta.

#### Tarefa 7.1 — Logs Estruturados
- [ ] **7.1.1** Configurar logging Python com formato JSON usando `python-json-logger`, incluindo campos `timestamp`, `level`, `tenant_id`, `phone`, `event`, `message` em todas as entradas de log do sistema. ⚠️ *Sistema atual usa `print('[BUFFER]', ...)` — sem estrutura, sem tenant_id, não adequado para produção.*
- [ ] **7.1.2** Adicionar log de `token_usage` por invocação RAG (via `TokenUsageCallback` implementado na Sprint 4).
- [ ] **7.1.3** Garantir que nenhum dado sensível (mensagem do usuário completa, API keys) aparece nos logs de nível `INFO`. Usar `DEBUG` com flag explícita para logs detalhados.

#### Tarefa 7.2 — Documentação
- [ ] **7.2.1** Atualizar `README.md` para refletir a stack final (Gemini, multi-tenant), incluindo: pré-requisitos, setup do `.env`, como adicionar um tenant no `tenants.json`, como executar a ingestão com `ingest.py`, como rodar os testes. ⚠️ *README atual descreve a versão OpenAI single-tenant.*
- [ ] **7.2.2** Documentar cada função pública dos módulos com docstrings no padrão Google Style.
- [ ] **7.2.3** Adicionar comentários inline explicando as decisões de design não óbvias (ex: por que `NX` no timer do debounce, por que o webhook retorna 200 imediatamente).

#### Tarefa 7.3 — Polimento e Hardening
- [ ] **7.3.1** Revisar todos os módulos garantindo: sem imports não utilizados, type hints completos em todas as funções públicas, aspas simples consistentes, linhas com máximo de 88 caracteres (compatível com `black`).
- [ ] **7.3.2** Adicionar `HEALTHCHECK` no `Dockerfile` chamando `GET /health`.
- [x] **7.3.3** Configurar `docker-compose.yml` com `restart: always` para os serviços críticos. ✅ *`restart: always` já presente em todos os serviços*
- [ ] **7.3.4** Criar `Makefile` com atalhos: `make up`, `make ingest TENANT=clinica_a`, `make test`, `make logs`.
- [ ] **7.3.5** Realizar teste end-to-end manual: instância da Evolution API conectada, envio de mensagem real via WhatsApp, verificação de resposta baseada em documento ingerido, verificação de logs.