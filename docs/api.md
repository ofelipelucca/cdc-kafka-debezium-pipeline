# API REST

Este documento descreve a API REST do projeto, seus endpoints, contratos e comportamento geral.

---

# Objetivo

A API tem como objetivo:

- expor operações de CRUD
- servir como entrada do sistema
- alimentar a pipeline CDC
- manter simplicidade (foco em arquitetura)

---

# Base URL

```text
http://localhost:8000/api/v1
```

---

# Entidades

O sistema possui duas entidades principais:

- users
- posts

---

# Users

## Criar usuário

### Endpoint

```http
POST /users
```

### Request body

```json
{
  "nome": "João Silva",
  "email": "joao@email.com"
}
```

---

### Response

```json
{
  "id": 1,
  "guid": "uuid-gerado",
  "nome": "João Silva",
  "email": "joao@email.com"
}
```

---

### Regras

- `guid` é gerado automaticamente
- email deve ser único
- resposta retorna o `guid` público

---

## Buscar usuário por GUID

### Endpoint

```http
GET /users/{guid}
```

---

### Response

```json
{
  "guid": "uuid",
  "nome": "João Silva",
  "email": "joao@email.com"
}
```

---

# Posts

## Criar post

### Endpoint

```http
POST /posts
```

---

### Request body

```json
{
  "user_guid": "uuid-do-user",
  "content": "Meu primeiro post"
}
```

---

### Response

```json
{
  "id": 1,
  "guid": "uuid-post",
  "user_guid": "uuid-do-user",
  "content": "Meu primeiro post"
}
```

---

### Regras

- `guid` é gerado automaticamente
- post pertence a um usuário existente
- dispara evento CDC automaticamente

---

## Buscar post por GUID

### Endpoint

```http
GET /posts/{guid}
```

---

### Response

```json
{
  "guid": "uuid-post",
  "user_guid": "uuid-user",
  "content": "Meu primeiro post"
}
```

---

# Feed

## Buscar feed

### Endpoint

```http
GET /feed?n=10
```

---

### Descrição

Retorna os últimos N posts materializados no MongoDB.

---

### Response

```json
[
  {
    "guid": "post-1",
    "content": "texto",
    "user": {
      "guid": "user-1",
      "nome": "Felipe"
    }
  }
]
```

---

### Regras

- valor padrão de `n` pode ser definido (ex: 10)
- limite máximo recomendado (ex: 50)
- leitura via MongoDB (read model)

---

# Arquitetura da API

A API segue padrão simples:

```text
Router
↓
Service
↓
Repository (SQLAlchemy)
↓
PostgreSQL
```

---

# Integração com CDC

A API NÃO envia eventos diretamente ao Kafka.

Fluxo correto:

```text
API → PostgreSQL → Debezium → Kafka
```

---

# Boas práticas adotadas

- GUID como identificador público
- separação entre ID interno e externo
- API stateless
- foco em simplicidade
- ausência de frontend intencional

---

# Limitações intencionais

Este projeto não inclui:

- autenticação (JWT)
- autorização
- rate limiting
- validação avançada
- paginação complexa
- cache

---

# Evoluções futuras

- autenticação JWT
- feed personalizado
- comentários
- likes
- notificações
- busca textual

---

# Conclusão

A API foi projetada como uma camada simples de entrada para demonstrar:

- arquitetura orientada a eventos
- CDC com Debezium
- separação entre write e read model
- integração com Kafka e MongoDB

sem complexidade desnecessária de produto final.