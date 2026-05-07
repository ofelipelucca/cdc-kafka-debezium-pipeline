# Arquitetura

Este documento descreve a arquitetura geral do projeto, os componentes envolvidos e o fluxo completo de dados da pipeline CDC.

---

# Objetivo do projeto

O projeto simula uma rede social 100% baseada em API utilizando:

- PostgreSQL como banco transacional
- Debezium para CDC (Change Data Capture)
- Kafka para streaming de eventos
- Consumers para processamento assíncrono
- MongoDB como read model otimizado para feed

O principal objetivo é demonstrar uma arquitetura orientada a eventos utilizando CDC em um cenário próximo de produção.

---

# Visão geral da arquitetura

```text
Client
  ↓
FastAPI
  ↓
PostgreSQL
  ↓
WAL (Logical Replication)
  ↓
Debezium
  ↓
Kafka
  ↓
Consumers
  ↓
MongoDB
  ↓
Feed API
```

---

# Componentes

## FastAPI

Responsável por:

- expor endpoints REST
- persistir dados transacionais
- iniciar o fluxo CDC

Principais endpoints:

| Método | Endpoint | Descrição |
|---|---|---|
| POST | /users | Criação de usuários |
| GET | /users/{guid} | Consulta de usuário |
| POST | /posts | Criação de posts |
| GET | /posts/{guid} | Consulta de post |
| GET | /feed | Consulta do feed |

---

## PostgreSQL

Banco relacional responsável pelo write model da aplicação.

Responsabilidades:

- persistência transacional
- integridade relacional
- origem oficial dos dados

Tabelas principais:

| Tabela | Descrição |
|---|---|
| users | Usuários da rede social |
| posts | Posts criados pelos usuários |

---

## WAL (Write Ahead Log)

O PostgreSQL registra alterações internamente através do WAL.

O Debezium utiliza logical replication para capturar:

- INSERT
- UPDATE
- DELETE

sem necessidade de polling ou queries periódicas.

---

## Debezium

Responsável por capturar alterações do PostgreSQL e transformá-las em eventos Kafka.

Responsabilidades:

- CDC em tempo real
- leitura do WAL lógico
- publicação de eventos nos tópicos Kafka

Exemplo de tópico:

```text
dbserver1.api_social_media.posts
```

---

## Kafka

Responsável pelo transporte dos eventos.

Funções principais:

- desacoplamento
- buffering
- streaming de eventos
- distribuição assíncrona

Cada tabela monitorada pelo Debezium gera um tópico dedicado.

---

## Consumers

Responsáveis por processar eventos Kafka e materializar read models.

Consumers implementados:

| Consumer | Responsabilidade |
|---|---|
| users_consumer | Sincronização de usuários |
| posts_consumer | Feed enriquecido |

---

## MongoDB

Responsável pelo read model otimizado da aplicação.

Objetivo:

- leitura rápida do feed
- documentos enriquecidos
- evitar joins em tempo real

Exemplo de documento:

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

# Estratégia de leitura e escrita

O projeto utiliza uma abordagem inspirada em CQRS.

## Write Model

Banco relacional:

```text
PostgreSQL
```

Responsável por:

- consistência
- integridade
- persistência oficial

---

## Read Model

Banco NoSQL:

```text
MongoDB
```

Responsável por:

- consultas rápidas
- feed otimizado
- documentos enriquecidos

---

# Fluxo completo de criação de post

## 1. Cliente envia request

```http
POST /posts
```

---

## 2. API persiste no PostgreSQL

Tabela:

```text
api_social_media.posts
```

---

## 3. PostgreSQL registra no WAL

Alteração registrada via logical replication.

---

## 4. Debezium captura mudança

Evento CDC é gerado automaticamente.

---

## 5. Evento enviado ao Kafka

Tópico:

```text
dbserver1.api_social_media.posts
```

---

## 6. Consumer processa evento

O consumer:

- interpreta payload CDC
- realiza enrichment
- monta documento final

---

## 7. MongoDB atualizado

Coleção:

```text
feed_posts
```

---

## 8. Feed API consulta MongoDB

```http
GET /feed
```

---

# Eventual Consistency

O sistema utiliza consistência eventual.

Isso significa que:

- PostgreSQL é a fonte oficial
- MongoDB pode ter pequeno atraso
- sincronização ocorre assíncronamente

Esse comportamento é esperado em arquiteturas orientadas a eventos.

---

# Motivação da arquitetura

A arquitetura foi escolhida para demonstrar:

- CDC real com Debezium
- streaming de eventos
- desacoplamento entre serviços
- read models otimizados
- pipelines assíncronas
- processamento orientado a eventos

---

# Benefícios da abordagem

## Escalabilidade

Leituras podem escalar independentemente das escritas.

---

## Desacoplamento

Consumers independentes podem ser adicionados sem alterar a API.

---

## Extensibilidade

Novos consumers podem:

- gerar analytics
- alimentar cache
- enviar notificações
- indexar busca
- produzir métricas

---

## Observabilidade

Eventos podem ser inspecionados em tempo real via Kafdrop.

---

# Limitações atuais

O projeto possui foco educacional e de arquitetura.

Não inclui:

- autenticação
- autorização
- rate limiting
- retry avançado
- DLQ
- métricas distribuídas
- tracing
- deploy cloud

---

# Próximos passos possíveis

- comments
- likes
- analytics
- observabilidade
- retry strategy
- async consumers
- particionamento Kafka
- deploy em Kubernetes
- monitoramento com Prometheus/Grafana