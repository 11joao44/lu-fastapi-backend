# 📦 Lu FastAPI – Backend Challenge

Este repositório contém a implementação da **API RESTful** da empresa **Lu Estilo**, com foco em facilitar a comunicação e automação do time comercial com clientes e operações internas.

A solução será construída com **FastAPI**, utilizando arquitetura em camadas, autenticação JWT e integração futura com WhatsApp.

---

## 🧩 Escopo do Projeto

A API deve atender aos seguintes módulos:

- [x] **Arquitetura**: 3-Layers Routers → Services → Repositories.
- [ ] **Autenticação (JWT)**: login, registro e refresh token.
- [ ] **Clientes**: CRUD completo, com filtros e validações.
- [ ] **Produtos**: CRUD com filtros (categoria, preço, disponibilidade).
- [ ] **Pedidos**: múltiplos produtos por pedido, status e filtros.
- [ ] **Integração WhatsApp**: envio automático de mensagens para eventos comerciais.
- [ ] **Camadas de permissão**: admin e usuário comum.
- [ ] **Validações robustas** e tratamento de erros com consistência.
- [ ] **Testes com pytest** (unitários e integração).
- [ ] **Deploy com Docker**.

---

## 🚀 Tecnologias Utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic (migrações)
- Pydantic 2.x
- Uvicorn
- Pytest
- Docker

---

## Commits Convencionais

| Prefixo    | Uso típico                                                                                   |
| ---------- | -------------------------------------------------------------------------------------------- |
| `Feature:` | Nova funcionalidade (ex: login, endpoint novo, integração)                                   |
| `Fix:`     | Correção de bug ou comportamento inesperado                                                  |
| `Chore:`   | Tarefas não relacionadas diretamente ao produto final (estrutura inicial, setup de ambiente) |
| `Update:`  | Melhorias genéricas (ex: refatoração leve, atualização de libs)                              |
| `Hotfix:`  | Correções urgentes/em produção (usado com deploys ou bugs críticos)                          |
