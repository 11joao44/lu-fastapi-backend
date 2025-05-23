# 📦 Lu FastAPI – Backend Challenge

Este repositório contém a implementação da **API RESTful** da empresa **Lu Estilo**, com foco em facilitar a comunicação e automação do time comercial com clientes e operações internas.

A solução será construída com **FastAPI**, utilizando arquitetura em camadas, autenticação JWT e integração futura com WhatsApp.

---

## 🧩 Escopo do Projeto

A API deve atender aos seguintes módulos:

- [x] **Arquitetura**: 3-Layers Routers → Services → Repositories.
- [X] **Autenticação (JWT)**: login, registro e refresh token.
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

---

## 📦 Modelagem de Banco de Dados

### Tabelas principais

---

#### 1. users

| Campo           | Tipo                         | Descrição                                    |
|-----------------|------------------------------|----------------------------------------------|
| id              | SERIAL PRIMARY KEY           | Identificador único                          |
| username        | VARCHAR(64) NOT NULL UNIQUE  | Nome de usuário (login)                      |
| email           | VARCHAR(128) NOT NULL UNIQUE | E-mail único                                 |
| hashed_password | VARCHAR(256) NOT NULL        | Senha hash (bcrypt/passlib)                  |
| is_active       | BOOLEAN NOT NULL DEFAULT TRUE| Usuário ativo                                |
| is_admin        | BOOLEAN NOT NULL DEFAULT FALSE| Usuário administrador                       |
| created_at      | TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP | Data de criação              |
| updated_at      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP          | Data de atualização          |

> **Função:** Usuários autenticáveis (quem pode logar/admin).

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    hashed_password VARCHAR(256) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. clients

| Campo       | Tipo                                 | Descrição           |
| ----------- | ------------------------------------ | ------------------- |
| id          | SERIAL PRIMARY KEY                   | Identificador único |
| name        | VARCHAR(255) NOT NULL                | Nome do cliente     |
| email       | VARCHAR(255) UNIQUE NOT NULL         | E-mail único        |
| phone       | VARCHAR(20) UNIQUE                   | Telefone único      |
| cpf\_cnpj   | VARCHAR(20) UNIQUE NOT NULL          | CPF ou CNPJ único   |
| address     | TEXT UNIQUE NOT NULL               | Endereço            |
| created\_at | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Data de criação     |
| updated\_at | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Data de atualização |

> **Função:** Clientes finais do negócio.
> **Regra:** email e cpf_cnpj devem ser únicos.

```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    cpf_cnpj VARCHAR(20) UNIQUE NOT NULL,
    address TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. products

| Campo            | Tipo                                 | Descrição                   |
| ---------------- | ------------------------------------ | --------------------------- |
| id               | SERIAL PRIMARY KEY                   | Identificador único         |
| name             | VARCHAR(255) NOT NULL                | Nome do produto             |
| description      | TEXT                                 | Descrição                   |
| price            | DECIMAL(10, 2) NOT NULL              | Preço                       |
| barcode          | VARCHAR(50) UNIQUE                   | Código de barras único      |
| section          | VARCHAR(100)                         | Seção (ex: bebida, limpeza) |
| stock            | INTEGER NOT NULL DEFAULT 0           | Quantidade em estoque       |
| expiration\_date | DATE                                 | Data de validade            |
| image\_url       | TEXT                                 | URL da imagem               |
| created\_at      | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Data de criação             |
| updated\_at      | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Data de atualização         |

> **Função:** Produtos ofertados, com controle de estoque e seção.

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    barcode VARCHAR(50) UNIQUE,
    section VARCHAR(100),
    stock INTEGER NOT NULL DEFAULT 0,
    expiration_date DATE,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. orders

| Campo         | Tipo                                 | Descrição                          |
| ------------- | ------------------------------------ | ---------------------------------- |
| id            | SERIAL PRIMARY KEY                   | Identificador único                |
| client\_id    | INTEGER NOT NULL                     | Cliente (FK → clients.id)          |
| user\_id      | INTEGER NOT NULL                     | Usuário que lançou (FK → users.id) |
| status        | VARCHAR(20) NOT NULL                 | Status do pedido                   |
| total\_amount | NUMERIC(10, 2) NOT NULL              | Valor total                        |
| created\_at   | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Data de criação                    |
| updated\_at   | TIMESTAMP DEFAULT CURRENT\_TIMESTAMP | Data de atualização                |

> **Função:** Pedidos, com status, valor total, data, ligação ao cliente e usuário que criou.

```sql
CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES public.clients(id),
    FOREIGN KEY (user_id) REFERENCES public.users(id)
);
```
