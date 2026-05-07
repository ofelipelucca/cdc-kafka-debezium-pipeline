# Setup

Este documento descreve como configurar e executar o ambiente completo do projeto localmente.

---

# Pré-requisitos

Antes de iniciar, certifique-se de possuir os seguintes softwares instalados:

- Docker Desktop
- Docker Compose
- Python 3.12+
- pip
- Git

---

# Estrutura do ambiente

O projeto utiliza os seguintes componentes:

| Componente | Responsabilidade |
|---|---|
| PostgreSQL | Banco transacional (write model) |
| Debezium | Captura de mudanças (CDC) |
| Kafka | Streaming de eventos |
| Kafka Connect | Gerenciamento de connectors |
| Kafdrop | Visualização de tópicos Kafka |
| MongoDB | Banco de leitura (read model) |
| Mongo Express | Interface visual do MongoDB |
| FastAPI | API REST |
| Consumers | Processamento assíncrono dos eventos |

---

# Clonar repositório

```bash
git clone https://github.com/ofelipelucca/cdc-kafka-debezium-pipeline.git
```

```bash
cd cdc-kafka-debezium-pipeline
```

---

# Subir infraestrutura

Na raiz do projeto:

```bash
cd docker
docker compose up -d
```

---

# Verificar containers

```bash
docker ps
```

Os seguintes containers devem estar ativos:

- zookeeper
- kafka
- kafka-connect
- postgres
- kafdrop
- mongodb
- mongo-express

---

# URLs locais

| Serviço | URL |
|---|---|
| Kafdrop | http://localhost:9000 |
| Kafka Connect | http://localhost:8083 |
| Mongo Express | http://localhost:8081 |
| FastAPI Swagger | http://localhost:8000/docs |

---

# Credenciais padrão

## PostgreSQL

| Campo | Valor |
|---|---|
| Host | localhost |
| Port | 5432 |
| User | postgres |
| Password | postgres |
| Database | postgres |

---

## Mongo Express

| Campo | Valor |
|---|---|
| User | admin |
| Password | admin |

---

# Criar schema e tabelas

Executar os scripts SQL localizados em:

```text
sql/
```

Ordem recomendada:

```text
01_schema.sql
02_users.sql
03_posts.sql
04_constraints.sql
```
---

# Configurar Debezium Connector

Executar:

```bash
curl -X POST http://localhost:8083/connectors ^
-H "Content-Type: application/json" ^
-d @connectors/postgres-connector.json
```

---

# Validar connector

```bash
curl http://localhost:8083/connectors
```

Resultado esperado:

```json
["postgres-connector"]
```

---

# Rodar API

Entrar na pasta da API:

```bash
cd api
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
uvicorn app.main:app --reload --reload-dir app
```

---

# Rodar consumers

Em terminais separados:

## Users Consumer

```bash
python consumers/users_consumer.py
```

---

## Posts Consumer

```bash
python consumers/posts_consumer.py
```

---

# Gerar dados fake


Instalar dependências:

```bash
cd scripts/tests
pip install -r requirements.txt
```

Executar:

```bash
python generate_fake_data.py
```

O script irá:

- criar usuários
- criar posts
- gerar eventos CDC automaticamente

---

# Validar fluxo CDC

## 1. Inserir dado via API

```http
POST /users
```

---

## 2. Verificar tópico no Kafdrop

Acessar:

```text
http://localhost:9000
```

---

## 3. Verificar MongoDB

Acessar:

```text
http://localhost:8081
```

Coleção esperada:

```text
feed_posts
```

---

# Troubleshooting rápido

## Kafka sem mensagens

Verificar se existe publication:

```sql
SELECT * FROM pg_publication_tables;
```

---

## Connector não sobe

Verificar logs:

```bash
docker logs kafka-connect
```

---

## Mongo Express caindo

Reiniciar:

```bash
docker restart mongo-express
```

---

# Encerrando ambiente

```bash
docker compose down
```

---

# Remover volumes e resetar tudo

```bash
docker compose down -v
```