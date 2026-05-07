# Fluxo CDC

Este documento descreve detalhadamente o fluxo de CDC (Change Data Capture) implementado no projeto utilizando PostgreSQL, Debezium e Kafka.

---

# Objetivo

O objetivo do fluxo CDC é capturar alterações realizadas no banco transacional em tempo real e propagá-las para outros sistemas de forma assíncrona.

Neste projeto, os eventos capturados alimentam um read model no MongoDB utilizado pela rota de feed.

---

# O que é CDC

CDC (Change Data Capture) é uma estratégia utilizada para detectar alterações em bancos de dados e propagá-las para outros sistemas.

Eventos capturados:

- INSERT
- UPDATE
- DELETE

---

# Estratégia utilizada

O projeto utiliza:

```text
PostgreSQL Logical Replication
```

com:

```text
Debezium + Kafka Connect
```

---

# Fluxo completo

```text
FastAPI
  ↓
PostgreSQL
  ↓
WAL
  ↓
Logical Replication
  ↓
Debezium
  ↓
Kafka Connect
  ↓
Kafka Topic
  ↓
Consumer
  ↓
MongoDB
```

---

# Etapa 1 — Escrita no PostgreSQL

Quando a API recebe um request:

```http
POST /posts
```

ela persiste os dados no PostgreSQL.

Exemplo:

```sql
INSERT INTO api_social_media.posts (
    content,
    id_user,
    guid
)
VALUES (
    'Meu primeiro post',
    1,
    'post-guid'
);
```

---

# Etapa 2 — Registro no WAL

O PostgreSQL registra alterações internamente no WAL (Write Ahead Log).

O WAL é utilizado originalmente para:

- recuperação
- replicação
- durabilidade

Neste projeto, ele também serve como origem dos eventos CDC.

---

# Etapa 3 — Logical Replication

O PostgreSQL é configurado com:

```text
wal_level=logical
```

permitindo que ferramentas externas consumam alterações estruturadas.

Configuração utilizada:

```yaml
command: >
  postgres -c wal_level=logical
           -c max_wal_senders=10
           -c max_replication_slots=10
```

---

# Etapa 4 — Publication

O Debezium depende de uma publication no PostgreSQL.

Ela define quais tabelas terão CDC habilitado.

Exemplo:

```sql
CREATE PUBLICATION dbz_publication
FOR TABLE
    api_social_media.users,
    api_social_media.posts;
```

---

# Verificar publications

```sql
SELECT * FROM pg_publication_tables;
```

---

# Etapa 5 — Debezium Connector

O connector do Debezium se conecta ao PostgreSQL e captura alterações automaticamente.

Exemplo de configuração:

```json
{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "postgres",
    "database.server.name": "dbserver1",
    "topic.prefix": "dbserver1",
    "plugin.name": "pgoutput"
  }
}
```

---

# Etapa 6 — Kafka Topic

Cada tabela monitorada gera um tópico Kafka.

Exemplo:

| Tabela | Tópico |
|---|---|
| users | dbserver1.api_social_media.users |
| posts | dbserver1.api_social_media.posts |

---

# Estrutura do evento CDC

Exemplo simplificado:

```json
{
  "before": null,
  "after": {
    "id": 1,
    "content": "Meu primeiro post",
    "id_user": 1,
    "guid": "post-guid"
  },
  "op": "c"
}
```

---

# Campo "op"

| Valor | Significado |
|---|---|
| c | create |
| u | update |
| d | delete |
| r | snapshot/read |

---

# Etapa 7 — Consumer

O consumer Kafka processa o evento:

```python
for msg in consumer:
```

Responsabilidades:

- interpretar payload
- tratar operação CDC
- realizar enrichment
- persistir read model

---

# Enrichment

O posts_consumer realiza enrichment utilizando dados do usuário.

Documento final:

```json
{
  "_id": 1,
  "guid": "post-guid",
  "content": "Meu primeiro post",
  "user": {
    "guid": "user-guid",
    "nome": "Felipe"
  }
}
```

---

# Etapa 8 — MongoDB Read Model

O documento processado é persistido em:

```text
feed_posts
```

Esse modelo é otimizado para leitura rápida do feed.

---

# Feed API

A rota:

```http
GET /feed
```

consulta diretamente o MongoDB.

Isso evita:

- joins
- queries complexas
- acoplamento com write model

---

# Snapshot inicial

Ao criar o connector, o Debezium pode executar snapshot das tabelas existentes.

Isso gera eventos com:

```json
"op": "r"
```

---

# Consistência eventual

O sistema opera com consistência eventual.

Fluxo:

```text
PostgreSQL
↓
Kafka
↓
Consumer
↓
MongoDB
```

Pode existir pequeno atraso entre:

- escrita
- disponibilidade no feed

Esse comportamento é esperado.

---

# Benefícios da abordagem

## Baixo acoplamento

Consumers independentes podem ser adicionados sem alterar a API.

---

## Escalabilidade

Leituras escalam separadamente das escritas.

---

## Reprocessamento

Eventos Kafka podem ser consumidos novamente.

---

## Extensibilidade

Novos consumers podem:

- gerar analytics
- popular cache
- alimentar busca
- produzir métricas
- gerar notificações

---

# Observabilidade

O fluxo pode ser acompanhado via:

## Kafdrop

```text
http://localhost:9000
```

---

## Kafka Connect

```text
http://localhost:8083
```

---

## Mongo Express

```text
http://localhost:8081
```

---

# Problemas comuns

## Publication vazia

Sintoma:

```sql
SELECT * FROM pg_publication_tables;
```

retorna vazio.

Solução:

```sql
CREATE PUBLICATION ...
```

---

## Eventos null

O Debezium pode enviar:

```json
null
```

durante tombstones.

O consumer deve validar:

```python
if payload is None:
    continue
```

---

## Connector não sobe

Verificar logs:

```bash
docker logs kafka-connect
```

---

# Conclusão

O fluxo CDC implementado demonstra:

- captura de mudanças em tempo real
- streaming de eventos
- arquitetura orientada a eventos
- materialização de read models
- integração entre bancos relacionais e NoSQL

utilizando tecnologias amplamente adotadas em ambientes distribuídos modernos.