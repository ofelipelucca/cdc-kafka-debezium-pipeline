# Decisões Arquiteturais

Este documento registra as principais decisões arquiteturais tomadas durante o desenvolvimento do projeto, os contextos envolvidos e os impactos de cada escolha.

---

# Objetivo

Documentar:

- decisões técnicas
- motivações
- trade-offs
- consequências arquiteturais

Essa prática facilita:

- manutenção
- evolução do projeto
- entendimento técnico
- rastreabilidade das escolhas

---

# Estrutura utilizada

Cada decisão segue o formato:

- Contexto
- Decisão
- Consequências

---

# Decisão 01 — Utilizar CDC com Debezium

## Contexto

O objetivo principal do projeto é demonstrar uma arquitetura orientada a eventos utilizando captura de mudanças em banco relacional.

Era necessário propagar alterações do PostgreSQL sem polling manual.

---

## Decisão

Utilizar:

```text
Debezium + Kafka Connect
```

consumindo alterações via logical replication do PostgreSQL.

---

## Consequências

### Positivas

- CDC em tempo real
- desacoplamento
- arquitetura moderna
- integração nativa com Kafka

### Negativas

- maior complexidade operacional
- dependência de Kafka Connect
- necessidade de logical replication

---

# Decisão 02 — PostgreSQL como write model

## Contexto

A aplicação possui entidades relacionais:

- users
- posts

Além disso, era necessário garantir:

- integridade
- consistência
- relacionamentos

---

## Decisão

Utilizar:

```text
PostgreSQL
```

como banco transacional principal.

---

## Consequências

### Positivas

- ACID
- integridade relacional
- confiabilidade

### Negativas

- joins custosos para feeds
- menor flexibilidade para leitura agregada

---

# Decisão 03 — MongoDB como read model

## Contexto

Feeds normalmente exigem:

- alta leitura
- documentos agregados
- consultas rápidas

Realizar joins em tempo real no PostgreSQL não era desejado.

---

## Decisão

Utilizar:

```text
MongoDB
```

como banco de leitura materializado.

---

## Consequências

### Positivas

- feed rápido
- documentos enriquecidos
- consultas simples

### Negativas

- consistência eventual
- duplicação de dados

---

# Decisão 04 — Arquitetura inspirada em CQRS

## Contexto

A separação entre leitura e escrita melhoraria:

- organização
- escalabilidade
- desacoplamento

---

## Decisão

Separar:

| Responsabilidade | Banco |
|---|---|
| Escrita | PostgreSQL |
| Leitura | MongoDB |

---

## Consequências

### Positivas

- read model especializado
- escalabilidade independente

### Negativas

- sincronização assíncrona
- maior complexidade arquitetural

---

# Decisão 05 — Feed servido exclusivamente pelo MongoDB

## Contexto

O feed é a principal consulta da aplicação.

Era importante demonstrar materialização de read model via CDC.

---

## Decisão

A rota:

```http
GET /feed
```

consulta apenas o MongoDB.

---

## Consequências

### Positivas

- prova clara do pipeline CDC
- baixa latência de leitura

### Negativas

- dependência dos consumers
- possível atraso de sincronização

---

# Decisão 06 — Utilizar GUID público

## Contexto

Expor IDs internos do banco não era desejado.

Além disso, GUIDs tornam a API mais próxima de cenários reais.

---

## Decisão

Todas as rotas públicas utilizam:

```text
guid
```

em vez de IDs internos.

---

## Consequências

### Positivas

- desacoplamento do banco
- melhor segurança
- API mais profissional

### Negativas

- payloads maiores
- necessidade de geração UUID

---

# Decisão 07 — Consumers independentes por entidade

## Contexto

Era importante manter:

- separação de responsabilidades
- baixo acoplamento
- possibilidade de expansão

---

## Decisão

Criar consumers específicos:

| Consumer | Responsabilidade |
|---|---|
| users_consumer | usuários |
| posts_consumer | feed |

---

## Consequências

### Positivas

- manutenção simplificada
- expansão facilitada

### Negativas

- mais processos
- mais componentes operacionais

---

# Decisão 08 — Enrichment no consumer

## Contexto

O feed precisava retornar:

- post
- dados do usuário

sem joins em tempo real.

---

## Decisão

Realizar enrichment no:

```text
posts_consumer
```

---

## Consequências

### Positivas

- feed pronto para leitura
- queries simples

### Negativas

- duplicação de dados
- necessidade de sincronização

---

# Decisão 09 — API minimalista

## Contexto

O foco principal do projeto é CDC e event streaming.

Não era desejado gastar tempo excessivo em:

- frontend
- autenticação
- regras complexas

---

## Decisão

Manter API simples:

- CRUD básico
- feed
- foco arquitetural

---

## Consequências

### Positivas

- foco no objetivo principal
- entrega mais rápida

### Negativas

- ausência de features comuns de produto real

---

# Decisão 10 — Rede social 100% API

## Contexto

O frontend não era relevante para os objetivos técnicos do projeto.

---

## Decisão

Não implementar frontend.

Toda interação ocorre via:

- Swagger
- requests HTTP
- scripts

---

## Consequências

### Positivas

- foco total no backend
- simplicidade operacional

### Negativas

- menor apelo visual

---

# Decisão 11 — Utilizar Docker Compose

## Contexto

O ambiente possui vários componentes distribuídos.

Era importante simplificar setup local.

---

## Decisão

Orquestrar infraestrutura com:

```text
docker compose
```

---

## Consequências

### Positivas

- onboarding simples
- ambiente reproduzível

### Negativas

- consumo elevado de recursos locais

---

# Decisão 12 — Utilizar geração massiva de dados

## Contexto

Poucos registros não demonstram pipelines CDC de forma convincente.

---

## Decisão

Criar scripts de stress test com:

- Faker
- paralelismo
- geração massiva de posts

---

## Consequências

### Positivas

- validação da pipeline
- demonstração de throughput

### Negativas

- maior consumo de recursos

---

# Possíveis decisões futuras

- particionamento Kafka
- retry strategy
- DLQ
- async consumers
- observabilidade
- métricas
- Kubernetes
- Redis cache
- Elasticsearch

---

# Conclusão

As decisões arquiteturais do projeto priorizam:

- desacoplamento
- event-driven architecture
- CDC real
- materialização de read models
- simplicidade operacional
- foco em arquitetura distribuída

buscando demonstrar conceitos modernos utilizados em sistemas orientados a eventos.