# 📦 Lu FastAPI – Backend Challenge

Este repositório contém a implementação da **API RESTful** da empresa **Lu Estilo**, projetada para automatizar o fluxo do time comercial com clientes e operações internas.  

A aplicação é construída com **FastAPI**, seguindo arquitetura em camadas (Routers → Services → Repositories), autenticação JWT e pronta para integração com WhatsApp.

---

## 🧩 Escopo do Projeto

A API oferece os seguintes módulos:

- [x] **Arquitetura**: 3 camadas (Routes → Services → Repositories)  
- [x] **Autenticação (JWT)**: login, registro, refresh token  
- [x] **Models (ORM)**: mapeamento das tabelas no PostgreSQL via SQLAlchemy  
- [x] **Clientes**: CRUD completo, filtros e validações  
- [x] **Produtos**: CRUD com filtros de categoria, preço, disponibilidade  
- [x] **Pedidos**: múltiplos produtos por pedido, status e filtros  
- [x] **Itens de Pedido**: associação `order_products`, filtros por data, preço e quantidade  
- [x] **Permissões**: rotas protegidas para admin e usuário comum  
- [x] **Testes** com pytest (unitários e de integração)  
- [x] **Deploy** com Docker (local e cloud)

---

## 🚀 Tecnologias Utilizadas

- **Python 3.12**  
- **FastAPI**  
- **SQLAlchemy 2.x** + **asyncpg**  
- **PostgreSQL**  
- **Alembic** (migrações)  
- **Pydantic 2.x**  
- **Uvicorn** (ASGI server)  
- **Pytest** (testes)  
- **Docker** + **docker-compose**  

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

## 🛠️ Como Rodar Localmente com Docker

### 1. Preparar variáveis de ambiente

Na raiz do projeto, crie um arquivo .env com:

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>
SECRET_KEY=<sua_secret_key_jwt>
ALGORITHM=HS256
```

### 2. Build & Up com Docker Compose

```bash
# Builda as imagens, instalando dependências
docker compose build --no-cache

# Sobe containers em background (web + opcional db local)
docker compose up -d
```

### 3. Testar endpoints

```bash
poetry run pytest tests/

ou

poetry run pytest -v
```

>Swagger UI: [LINK LOCAL](http://localhost:8000/docs)
>Swagger UI: [LINK PRODUÇÃO](https://lu-fastapi-backend-docker.onrender.com/docs)
>Collection Postman: Em anexo e-mail.

## 📦 Modelagem de Banco de Dados

### Tabelas principais

---

#### 1. users

| Campo           | Tipo                                         | Descrição                   |
| --------------- | -------------------------------------------- | --------------------------- |
| id              | SERIAL PRIMARY KEY                           | Identificador único         |
| username        | VARCHAR(64) NOT NULL UNIQUE                  | Nome de usuário (login)     |
| email           | VARCHAR(128) NOT NULL UNIQUE                 | E-mail único                |
| hashed_password | VARCHAR(256) NOT NULL                        | Senha hash (bcrypt/passlib) |
| is_active       | BOOLEAN NOT NULL DEFAULT TRUE                | Usuário ativo               |
| is_admin        | BOOLEAN NOT NULL DEFAULT FALSE               | Usuário administrador       |
| created_at      | TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP | Data de criação             |
| updated_at      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP          | Data de atualização         |

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

| Campo      | Tipo                                | Descrição           |
| ---------- | ----------------------------------- | ------------------- |
| id         | SERIAL PRIMARY KEY                  | Identificador único |
| name       | VARCHAR(255) NOT NULL               | Nome do cliente     |
| email      | VARCHAR(255) UNIQUE NOT NULL        | E-mail único        |
| phone      | VARCHAR(20) UNIQUE                  | Telefone único      |
| cpf_cnpj   | VARCHAR(20) UNIQUE NOT NULL         | CPF ou CNPJ único   |
| address    | TEXT UNIQUE NOT NULL                | Endereço            |
| created_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de criação     |
| updated_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de atualização |

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

| Campo           | Tipo                                | Descrição                   |
| --------------- | ----------------------------------- | --------------------------- |
| id              | SERIAL PRIMARY KEY                  | Identificador único         |
| name            | VARCHAR(255) NOT NULL               | Nome do produto             |
| description     | TEXT                                | Descrição                   |
| price           | DECIMAL(10, 2) NOT NULL             | Preço                       |
| barcode         | VARCHAR(50) UNIQUE                  | Código de barras único      |
| section         | VARCHAR(100)                        | Seção (ex: bebida, limpeza) |
| stock           | INTEGER NOT NULL DEFAULT 0          | Quantidade em estoque       |
| expiration_date | DATE                                | Data de validade            |
| image_url       | TEXT                                | URL da imagem               |
| created_at      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de criação             |
| updated_at      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de atualização         |

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

| Campo        | Tipo                                | Descrição                          |
| ------------ | ----------------------------------- | ---------------------------------- |
| id           | SERIAL PRIMARY KEY                  | Identificador único                |
| client_id    | INTEGER NOT NULL                    | Cliente (FK → clients.id)          |
| user_id      | INTEGER NOT NULL                    | Usuário que lançou (FK → users.id) |
| status       | VARCHAR(20) NOT NULL                | Status do pedido                   |
| total_amount | NUMERIC(10, 2) NOT NULL             | Valor total                        |
| created_at   | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de criação                    |
| updated_at   | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de atualização                |

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

#### 5. order_products

| Campo           | Tipo                                | Descrição                             |
| --------------- | ----------------------------------- | ------------------------------------- |
| id              | SERIAL PRIMARY KEY                  | Identificador único                   |
| order_id        | INTEGER NOT NULL                    | Order (FK → orders.id)                |
| product_id      | INTEGER NOT NULL                    | Product que lançou (FK → products.id) |
| quantity        | INTEGER NOT NULL                    | quantidade de pedidos                 |
| price_at_amount | NUMERIC(10, 2) NOT NULL             | Valor total                           |
| created_at      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de criação                       |
| updated_at      | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Data de atualização                   |

> **Função:** permitir pedido com múltiplos produtos e filtro por seção.

```sql
CREATE TABLE order_products (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_moment NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```
