# Stress Test

Este documento descreve a estratégia utilizada para geração massiva de dados e testes de throughput da pipeline CDC.

---

# Objetivo

O objetivo dos stress tests é validar:

- propagação CDC
- estabilidade da pipeline
- processamento assíncrono
- sincronização do MongoDB
- comportamento dos consumers
- throughput de eventos

---

# Estratégia utilizada

Os testes geram grandes volumes de:

- usuários
- posts

via API REST.

---

# Fluxo exercitado

```text
Script
  ↓
FastAPI
  ↓
PostgreSQL
  ↓
Debezium
  ↓
Kafka
  ↓
Consumers
  ↓
MongoDB
```

---

# Motivação

O projeto foi desenhado para demonstrar CDC e event streaming.

Gerar poucos registros manualmente não demonstra:

- paralelismo
- throughput
- estabilidade
- propagação em escala

---

# Script de geração

Localização:

```text
scripts/generate_fake_data.py
```

---

# Tecnologias utilizadas

| Tecnologia | Objetivo |
|---|---|
| Faker | geração de dados fake |
| requests | chamadas HTTP |
| ThreadPoolExecutor | paralelismo |
| logging | observabilidade |

---

# Estratégia de paralelismo

O script utiliza:

```python
ThreadPoolExecutor
```

para gerar múltiplas requests simultaneamente.

---

# Benefícios

## Maior throughput

Aumento significativo da taxa de requests.

---

## Simulação mais realista

Representa múltiplos clientes simultâneos.

---

## Estresse da pipeline

Kafka e consumers recebem eventos em alta velocidade.

---

# Configurações principais

```python
TOTAL_USERS = 100
TOTAL_POSTS = 10_000
MAX_WORKERS = 50
```

---

# Fluxo do script

## 1. Criação de usuários

```text
POST /users
```

---

## 2. Armazenamento dos GUIDs

Os GUIDs retornados pela API são mantidos em memória.

---

## 3. Criação massiva de posts

```text
POST /posts
```

---

## 4. Geração automática de eventos CDC

Cada insert dispara:

```text
PostgreSQL
↓
Debezium
↓
Kafka
```

---

# Exemplo simplificado

```python
with ThreadPoolExecutor(max_workers=MAX_WORKERS):
```

---

# Throughput observado

O throughput depende de:

- hardware
- Docker Desktop
- recursos disponíveis
- quantidade de workers
- capacidade do Kafka

---

# Gargalos identificados

Durante os testes, os principais gargalos observados foram:

| Componente | Possível gargalo |
|---|---|
| FastAPI | limite de workers |
| Kafka Connect | serialização |
| MongoDB | escrita intensa |
| Docker Desktop | memória insuficiente |

---

# Observabilidade

Os eventos podem ser acompanhados em tempo real.

---

# Kafka

## Kafdrop

```text
http://localhost:9000
```

Permite visualizar:

- tópicos
- offsets
- mensagens
- throughput

---

# MongoDB

## Mongo Express

```text
http://localhost:8081
```

Permite validar:

- sincronização
- crescimento do feed
- documentos enriquecidos

---

# Logs

Os scripts utilizam logging para acompanhamento:

```python
logging.info(
    f"[{i}/{TOTAL_POSTS}] posts created"
)
```

---

# Objetivo dos testes

Os testes não possuem foco em benchmark absoluto.

O objetivo principal é demonstrar:

- pipeline funcionando
- CDC em escala
- event streaming
- sincronização assíncrona

---

# Comportamentos observados

## Eventual consistency

Durante alto throughput, pode existir atraso entre:

```text
INSERT
↓
disponibilidade no feed
```

Esse comportamento é esperado.

---

# Consumers

Os consumers processam eventos continuamente.

A sincronização ocorre de forma incremental.

---

# Possíveis melhorias

## Async requests

Substituir requests síncronos por:

```text
httpx + asyncio
```

---

## Batch insert

Persistência em lote no MongoDB.

---

## Retry strategy

Reprocessamento automático de falhas.

---

## Metrics

Adicionar métricas com:

- Prometheus
- Grafana

---

## Particionamento Kafka

Distribuir eventos em múltiplas partições.

---

# Testes futuros

## Comments

Simulação de comentários em posts.

---

## Likes

Eventos de interação social.

---

## Feed personalizado

Materialização por usuário.

---

## Trending posts

Analytics em tempo real.

---

# Cuidados

## Docker Desktop

Kafka + Mongo + PostgreSQL podem consumir bastante memória.

Recomendado:

| Recurso | Valor |
|---|---|
| RAM | 6GB+ |
| CPU | 4+ |

---

# Limitações atuais

O projeto não implementa:

- benchmark formal
- métricas persistidas
- tracing distribuído
- monitoramento avançado
- autoscaling

---

# Conclusão

Os stress tests demonstram:

- capacidade da pipeline CDC
- propagação assíncrona de eventos
- integração entre PostgreSQL, Kafka e MongoDB
- funcionamento do read model
- comportamento de sistemas orientados a eventos sob carga

utilizando geração massiva de dados e paralelismo para simular cenários mais próximos de ambientes reais.