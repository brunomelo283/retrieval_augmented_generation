# Projeto RAG Completo – FastAPI, Qdrant, Elasticsearch e LLM

Este repositório apresenta uma **implementação completa de RAG (Retrieval-Augmented Generation)**, construída com foco em **arquitetura corporativa**, **modularidade**, **anti-alucinação** e **facilidade de testes locais**.

O projeto demonstra, de ponta a ponta, como ingerir documentos, indexá-los de forma vetorial e textual, recuperar informações relevantes e gerar respostas confiáveis utilizando modelos de linguagem (LLMs), mantendo total controle sobre o contexto utilizado.

---

## 🎯 Objetivo do Projeto

- Demonstrar uma arquitetura real de **RAG corporativo**
- Isolar a complexidade de IA em um **AI Gateway**
- Evitar alucinações por meio de:
  - Threshold de confiança
  - Prompt corporativo
  - Uso exclusivo de contexto recuperado
- Permitir execução **100% local**, sem dependência de serviços pagos
- Manter a solução preparada para **migração futura para produção**

---

## 🏗️ Arquitetura Geral

Fluxo simplificado da aplicação:

1. **AI Gateway (FastAPI)**
2. Ingestão e chunking de documentos
3. Geração de embeddings
4. Indexação:
   - Qdrant (busca vetorial)
   - Elasticsearch (busca textual – BM25)
5. Hybrid Search
6. Reranking com Cross-Encoder
7. Montagem de contexto
8. Prompt corporativo + anti-alucinação
9. Geração de resposta com LLaMA (Groq)

---

## 📂 Estrutura do Projeto

```text
PROJETO_RAG_COMPLETO
├── docker
│   └── docker-compose.yml
│
├── rag_api
│   ├── app
│   │   ├── embeddings
│   │   │   ├── provider.py
│   │   │   └── sentence_transformer.py
│   │   │
│   │   ├── ingestion
│   │   │   ├── chunking.py
│   │   │   ├── loaders.py
│   │   │   └── pipeline.py
│   │   │
│   │   ├── llm
│   │   │   ├── answer_pipeline.py
│   │   │   ├── context_builder.py
│   │   │   ├── llama_client.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── search
│   │   │   ├── elastic_repository.py
│   │   │   └── hybrid_search.py
│   │   │
│   │   ├── vectorstore
│   │   │   ├── qdrant_client.py
│   │   │   └── qdrant_repository.py
│   │   │
│   │   ├── reranking
│   │   │   └── reranking.py
│   │   │
│   │   ├── main.py
│   │   └── .env
│   │
│   ├── Dockerfile
│   ├── Dockerfile.base
│   └── requirements.txt
