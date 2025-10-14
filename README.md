# WhatsBoot

WhatsBoot é um chatbot de WhatsApp inteligente e conversacional, construído com FastAPI e potencializado por LangChain e OpenAI. Ele utiliza uma arquitetura RAG (Retrieval-Augmented Generation) para responder a perguntas com base em uma base de conhecimento de documentos fornecida por você.

## Funcionalidades

  * **Integração com WhatsApp:** Recebe e responde mensagens diretamente no WhatsApp através da Evolution API.
  * **IA com RAG (Retrieval-Augmented Generation):** O bot usa a LangChain para consultar uma base de conhecimento de documentos (arquivos PDF e TXT) e gerar respostas contextuais e precisas com a ajuda de modelos da OpenAI.
  * **Memória Conversacional:** Mantém o histórico de conversas com cada usuário utilizando Redis, permitindo interações mais naturais e contextuais.
  * **Buffer de Mensagens (Debouncing):** Um sistema inteligente que aguarda o usuário terminar de enviar uma sequência de mensagens antes de processá-las. Isso melhora a experiência do usuário e otimiza as chamadas à IA.
  * **Containerizado com Docker:** Todo o ambiente, incluindo o bot, a API do WhatsApp, o Redis e o banco de dados, é facilmente configurado e executado com Docker Compose.

## Arquitetura

O fluxo de funcionamento é o seguinte:

1.  A **Evolution API** recebe uma mensagem do WhatsApp e a envia para o webhook do **WhatsBoot**.
2.  A aplicação **FastAPI** (`app.py`) recebe a mensagem.
3.  A mensagem é adicionada a um buffer no **Redis** (`message_buffer.py`).
4.  Após um breve período de inatividade do usuário, o buffer é processado.
5.  A **LangChain** utiliza o histórico da conversa (também do Redis) para reformular a pergunta.
6.  O sistema busca informações relevantes nos documentos da base de conhecimento (vetorizados pelo **ChromaDB**).
7.  A **OpenAI** gera uma resposta com base no contexto da conversa e nos documentos encontrados.
8.  A resposta é enviada de volta ao usuário via **Evolution API**.

## Primeiros Passos

### Pré-requisitos

  * Docker
  * Docker Compose
  * Chaves de API da OpenAI

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/igorvoidbot/whatsboot.git
    cd whatsboot
    ```

2.  **Configure as variáveis de ambiente:**

      * Renomeie o arquivo `.env.example` para `.env`.
      * Preencha todas as variáveis necessárias no arquivo `.env`, incluindo suas chaves da OpenAI e as configurações da Evolution API.

3.  **Adicione sua Base de Conhecimento:**

      * Coloque seus arquivos `.pdf` ou `.txt` dentro da pasta `rag_files`. O bot irá processar esses arquivos para criar a base de conhecimento.

4.  **Inicie os containers:**

    ```bash
    docker-compose up -d --build
    ```

5.  **Configure a Evolution API:**

      * Acesse a interface da Evolution API (normalmente em `http://localhost:8080`).
      * Crie uma instância e leia o QR Code com seu WhatsApp para conectar.
      * Configure o Webhook da sua instância para apontar para `http://bot:8000/webhook` (o nome `bot` é o nome do serviço no `docker-compose.yml`).

Agora, o chatbot está pronto para receber e responder mensagens no número de WhatsApp que você conectou.
