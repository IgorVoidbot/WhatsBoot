# WhatsBoot - Chatbot Inteligente com RAG e Event Buffering

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-green)
![LangChain](https://img.shields.io/badge/AI-LangChain%20RAG-orange)
![Redis](https://img.shields.io/badge/Redis-Caching%20%26%20Buffer-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

## 🧠 Sobre o Projeto (Engenharia & IA)

O **WhatsBoot** é um assistente virtual de alta performance integrado ao WhatsApp. Diferente de bots tradicionais baseados em regras (`if/else`), ele utiliza uma arquitetura **RAG (Retrieval-Augmented Generation)** para "ler" documentos PDF/TXT e responder perguntas contextuais usando Vetores Matemáticos.

O diferencial técnico deste projeto é sua preocupação com **Concorrência e Otimização de Recursos**. Ele implementa um sistema de *Debouncing* (Buffer de Mensagens) usando Redis e Python Async, garantindo que o sistema não seja sobrecarregado por múltiplos inputs simultâneos — um conceito fundamental em sistemas de tempo real.

## 🚀 Destaques Técnicos (Skills Transferíveis)

Embora escrito em Python, este projeto aplica conceitos centrais de Ciência da Computação e desenvolvimento de sistemas complexos (como Engines de Jogos/VR):

* **Matemática Vetorial (Embeddings):** Utilização de `ChromaDB` para armazenar e consultar dados via similaridade vetorial (Cosseno/Euclidiana). A lógica de manipulação de vetores aqui é análoga à usada em **Computação Gráfica 3D**.
* **Processamento Assíncrono (`asyncio`):** O sistema não bloqueia a thread principal enquanto processa mensagens. O uso de `await` e filas no Redis simula o comportamento de sistemas de eventos não-bloqueantes.
* **Gestão de Estado (State Management):** Persistência de histórico de conversas e controle de "sessão" do usuário via Redis, similar ao gerenciamento de estado de jogadores em servidores multiplayer.
* **Arquitetura de Microsserviços:** Orquestração de múltiplos containers (App, Banco Vetorial, Redis, API WhatsApp) via Docker Compose.

## 🛠️ Arquitetura do Sistema

1.  **Input Buffer (Otimização):**
    * Recebe mensagens via Webhook.
    * Armazena em lista temporária no Redis (`RPUSH`).
    * *Debounce:* Reinicia um timer a cada nova mensagem. A IA só é acionada após X segundos de silêncio, economizando tokens e processamento.
2.  **RAG Engine (LangChain):**
    * Carrega PDFs e quebra em *chunks*.
    * Converte texto em Vetores (OpenAI Embeddings).
    * Recupera contexto relevante e gera resposta.
3.  **Interface:** Integração via Evolution API (WhatsApp Gateway).

## ⚙️ Stack Tecnológica

* **Linguagem:** Python 3.13 (Foco em tipagem e async)
* **Framework Web:** FastAPI (Alta performance)
* **Banco de Dados Vetorial:** ChromaDB (SQLite-based)
* **Cache/Fila:** Redis
* **IA/LLM:** OpenAI GPT-4o + LangChain
* **Infraestrutura:** Docker & Docker Compose

## 🔧 Como Executar

### Pré-requisitos
* Docker e Docker Compose instalados.
* Chave de API da OpenAI.

### Passos
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/whatsboot.git](https://github.com/seu-usuario/whatsboot.git)
    ```
2.  **Configure o ambiente:**
    * Crie um arquivo `.env` com suas credenciais (veja `.env.example`).
3.  **Adicione Conhecimento:**
    * Coloque seus arquivos `.pdf` na pasta `rag_files/`.
4.  **Suba os containers:**
    ```bash
    docker-compose up -d --build
    ```

## 🧪 Estrutura de Código (Destaque)

* `message_buffer.py`: Implementação manual da lógica de *Debounce* e filas assíncronas com Redis.
* `vectorstore.py`: Lógica de ingestão e matemática de busca vetorial.
* `chains.py`: Cadeias de raciocínio da IA.

---
*Desenvolvido como projeto de pesquisa em Inteligência Artificial e Sistemas Distribuídos.*
