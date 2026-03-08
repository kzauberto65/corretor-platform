# 📘 CONTEXT.md — CORRETOR PLATFORM
> Cole este arquivo na raiz do projeto. Ele é o contexto base para toda sessão do Claude Code.
> Versão: 2026 | Status atual: Sprint 10 concluída | Próxima: Sprint 10.5

---

## 🧭 O QUE É ESTE PROJETO

Plataforma SaaS de Inteligência Imobiliária para corretores e imobiliárias.  
Combina CRM, motor de recomendação com IA, automação comercial e integração com tráfego pago.  
Estágio atual: MVP single-user (filho do fundador), Python + SQLite + Serverless + Clean Architecture.

**Pipeline central:**
```
Mailing → Lead → Offer → Matching → IA → Automação
```

---

## 🏗️ ARQUITETURA (CLEAN ARCHITECTURE — IMUTÁVEL)

```
src/
 ├── domain/           → DTOs, Entities, Interfaces de repositório
 ├── application/      → Services, Normalizers, Engines, Casos de uso
 ├── infrastructure/   → Repositórios concretos, Ingestores, Exporters, DB
 ├── interface/        → CLI, API (futura), Webhooks
 └── menu.py           → Menu principal
```

**Regras absolutas de arquitetura (nunca violar):**
- Engines ficam em `application/` — lógica pura, sem acesso a banco
- Repositórios ficam em `infrastructure/` — apenas CRUD, sem regra de negócio
- Services ficam em `application/` — orquestram engines e repositórios
- CLI chama Services, nunca Engines diretamente
- DTOs sempre usados entre camadas
- Sem inventar colunas ou campos não existentes no banco
- Sem alterar arquitetura sem instrução explícita

---

## 📁 ESTRUTURA DE PASTAS REAL (verificada via tree /f)

```
corretor-platform/
│   corretor.db              ← BANCO PRINCIPAL (usar sempre este)
│   CONTEXT.md
│   ingest.bat / menu.bat    ← atalhos de execução
│   ingestao.py              ← legado, ainda funcional
│
├── data/
│   ├── entrada/lead/, mailing/
│   ├── erros/               ← arquivos rejeitados na ingestão
│   ├── exportacoes/ia/, mailing/, matching/, ofertas/
│   ├── logs/
│   └── processado/lead/, mailing/
│
├── src/
│   │   menu.py              ← menu principal ATIVO
│   │   menu_ant.py          ← legado (não apagar)
│   │   parsing.py
│   │
│   ├── application/
│   │   ├── construtora/normalizers/, services/
│   │   ├── construtora_imobiliaria/services/
│   │   ├── corretor/normalizers/, services/
│   │   ├── corretor_imobiliaria/services/
│   │   ├── corretor_unidade/services/
│   │   ├── empreendimento/normalizers/, services/
│   │   ├── ia/
│   │   │   ├── engine/ia_engine.py       ← ENGINE ATIVO
│   │   │   └── services/ia_service.py    ← SERVICE ATIVO
│   │   ├── imobiliaria/normalizers/, services/
│   │   ├── importacao/normalizers/, services/
│   │   ├── incorporadora/normalizers/, services/
│   │   ├── incorporadora_imobiliaria/services/
│   │   ├── lead/normalizers/, services/
│   │   ├── mailing/normalizers/, services/
│   │   ├── matching/
│   │   │   ├── engine/matching_engine.py ← ENGINE ATIVO
│   │   │   └── services/matching_service.py
│   │   ├── offer/
│   │   │   ├── matching/matching_engine.py ← ⚠️ DUPLICADO (verificar uso)
│   │   │   ├── normalizers/offer_normalizer.py
│   │   │   └── services/offer_service.py, offer_report_service.py
│   │   ├── servicos/        ← ⚠️ LEGADO — NÃO USAR EM CÓDIGO NOVO
│   │   │   (construtora_service, empreendimento_service, unidade_service,
│   │   │    unidade_referencia_service, query_service, ingestao_planilha_service,
│   │   │    gerenciador_arquivos, logger_ingestao)
│   │   ├── spe/normalizers/, services/
│   │   ├── unidade/normalizers/, services/
│   │   ├── unidade_referencia/normalizers/, services/
│   │   └── unidade_referencia_tipo/normalizers/, services/
│   │
│   ├── domain/
│   │   ├── construtora/dto/, entities/, interfaces/
│   │   ├── construtora_imobiliaria/dto/, entities/, normalizers/
│   │   ├── corretor/dto/, entities/, interfaces/
│   │   ├── corretor_imobiliaria/dto/, entities/, normalizers/
│   │   ├── corretor_unidade/dto/, entities/, normalizers/
│   │   ├── empreendimento/dto/, entities/, interfaces/
│   │   │   (empreendimento_dto, input_dto, filter_dto, normalized_dto)
│   │   ├── ia/
│   │   │   ├── dto/ia_input_dto.py
│   │   │   └── entities/ia_entity.py
│   │   ├── imobiliaria/dto/, entities/, interfaces/
│   │   ├── importacao/dto/, entities/
│   │   ├── incorporadora/dto/, entities/, interfaces/
│   │   ├── incorporadora_imobiliaria/dto/, entities/, normalizers/
│   │   ├── lead/dto/, entities/, interfaces/, normalizers/, repositories/
│   │   ├── mailing/dto/, entities/, interfaces/
│   │   ├── matching/dto/, entities/
│   │   │   (matching_input_dto, matching_result_dto, matching_entity)
│   │   ├── offer/dto/, entities/, interfaces/
│   │   ├── spe/dto/, entities/, interfaces/
│   │   ├── unidade/dto/, entities/, interfaces/
│   │   ├── unidade_referencia/dto/, entities/
│   │   └── unidade_referencia_tipo/dto/, entities/
│   │
│   ├── infrastructure/
│   │   ├── construtora/repositories/
│   │   │   (construtora_repository, construtora_imobiliaria_repository)
│   │   ├── construtora_imobiliaria/repositories/
│   │   ├── corretor/repositories/
│   │   │   (corretor_repository, corretor_imobiliaria_repository)
│   │   ├── corretor_imobiliaria/repositories/
│   │   ├── corretor_unidade/repositories/
│   │   ├── database/
│   │   │   ├── schema.sql        ← SOURCE OF TRUTH do schema
│   │   │   ├── corretor.db       ← NÃO usar (usar o da raiz)
│   │   │   └── migrations/
│   │   ├── empreendimento/repositories/empreendimento_repository.py
│   │   ├── ia/
│   │   │   ├── exporters/ (ia_exporter, ia_dashboard_exporter,
│   │   │   │               ia_exporter_completo, ia_whatsapp)
│   │   │   └── repositories/ia_repository.py
│   │   ├── imobiliaria/repositories/
│   │   ├── importacao/repositories/
│   │   ├── incorporadora/repositories/
│   │   ├── incorporadora_imobiliaria/repositories/
│   │   ├── ingestao/             ← PIPELINE CENTRAL DE INGESTÃO
│   │   │   ├── base_ingestor.py
│   │   │   ├── ingest.py
│   │   │   ├── ingestao_central.py
│   │   │   ├── ingestao_construtora.py
│   │   │   ├── ingestao_corretor.py
│   │   │   ├── ingestao_empreendimento.py
│   │   │   ├── ingestao_imobiliaria.py
│   │   │   ├── ingestao_lead.py
│   │   │   ├── ingestao_mailing.py
│   │   │   ├── ingestao_relacionamentos.py
│   │   │   ├── ingestao_unidade.py
│   │   │   ├── normalizador.py
│   │   │   └── xls_parser.py
│   │   ├── lead/repositories/lead_repository.py
│   │   ├── mailing/repositories/, exporters/
│   │   │   (mailing_exporter, mailing_resumido_exporter)
│   │   ├── matching/repositories/, exporters/
│   │   │   (matching_exporter, matching_exporter_completo,
│   │   │    matching_whatsapp_formatter)
│   │   ├── offer/repositories/, exporters/
│   │   │   (offer_exporter, offer_exporter_completo, offer_whatsapp_formatter)
│   │   ├── spe/repositories/
│   │   ├── unidade/repositories/
│   │   │   ├── unidade_repository.py
│   │   │   ├── unidade_referencia_repository.py  ← ⚠️ DUPLICADO
│   │   │   └── unidade_referencia_tipo_repository.py
│   │   ├── unidade_referencia/repositories/unidade_referencia_repository.py
│   │   ├── unidade_referencia_tipo/repositories/
│   │   └── shared/utils/base_repository.py
│   │
│   ├── interface/cli/
│   │   ├── construtora_cli.py
│   │   ├── construtora_imobiliaria_cli.py
│   │   ├── corretor_cli.py
│   │   ├── corretor_imobiliaria_cli.py
│   │   ├── corretor_unidade_cli.py
│   │   ├── empreendimento_cli.py     ← ATIVO
│   │   ├── ia_cli.py
│   │   ├── imobiliaria_cli.py
│   │   ├── importacao_cli.py
│   │   ├── incorporadora_cli.py
│   │   ├── incorporadora_imobiliaria_cli.py
│   │   ├── mailing_cli.py
│   │   ├── matching_cli.py
│   │   ├── offer_cli.py
│   │   ├── spe_cli.py
│   │   ├── unidade_cli.py
│   │   ├── unidade_referencia_cli.py
│   │   └── unidade_referencia_tipo_cli.py
│   │
│   ├── relatorios/relatorio_qualidade_dados.py
│   └── utils/
│
└── tests/application/
    (construtora, corretor, empreendimento, imobiliaria,
     incorporadora, offer, spe, unidade, unidade_referencia, etc.)
```

### ⚠️ Alertas críticos da estrutura real

**Banco de dados:** usar SEMPRE `corretor.db` na **raiz do projeto**. O `infrastructure/database/corretor.db` é redundante.

**Arquivos legado — não apagar, não usar em código novo:**
- `src/application/servicos/` — services antigos centralizados
- Qualquer arquivo `*_ant.py` ou `*_orig.py`
- `menu_ant.py`, `ingestao.py` na raiz
- `empreendimento_cli_ant.py`, `empreendimento_cli_sem_filtro.py`

**Duplicidades que exigem atenção ao importar:**
- `unidade_referencia_repository.py` → existe em `infrastructure/unidade/repositories/` E em `infrastructure/unidade_referencia/repositories/` — usar o de `unidade_referencia/`
- `matching_engine.py` → existe em `application/matching/engine/` E em `application/offer/matching/` — usar o de `matching/engine/`
- `construtora_imobiliaria_repository.py` → existe em `infrastructure/construtora/` E `infrastructure/construtora_imobiliaria/`
- `corretor_imobiliaria_repository.py` → existe em `infrastructure/corretor/` E `infrastructure/corretor_imobiliaria/`

**Módulos completos já implementados (além dos engines core):**
`construtora, construtora_imobiliaria, corretor, corretor_imobiliaria,
corretor_unidade, imobiliaria, importacao, incorporadora,
incorporadora_imobiliaria, spe, unidade, unidade_referencia, unidade_referencia_tipo`

---

## 🔁 PADRÕES DE CÓDIGO (SEMPRE SEGUIR)

### DTO
```python
class XInputDTO:
    def __init__(self, campo1: tipo, campo2: tipo):
        self.campo1 = campo1
        self.campo2 = campo2

class XEntity:
    id: int
    # campos...
    created_at: str
```

### Normalizer
```python
class XNormalizer:
    def normalize(self, row: dict) -> XInputDTO:
        return XInputDTO(
            campo=row.get("campo", "").strip()
        )
```

### Service
```python
class XService:
    def __init__(self, repo, engine=None):
        self.repo = repo
        self.engine = engine

    def run(self, dto):
        result = self.engine.executar(dto)
        self.repo.save(result)
```

### Engine (lógica pura — sem banco)
```python
class XEngine:
    def executar(self, lead, imovel) -> tuple:
        # lógica determinística
        return score, reasons_json
```

### Repository
```python
class XRepository:
    def __init__(self, db_path="corretor.db"):
        self.db_path = db_path

    def save(self, dto): ...
    def list_all(self): ...
    def list_by_lead(self, lead_id): ...
    def list_best(self, lead_id, limit): ...
```

### CLI
```python
# Comandos padrão por módulo:
# run | run-all | list | best | export | export-all | whatsapp
python -m src.interface.cli.x_cli <comando> --args
```

---

## 🗃️ BANCO DE DADOS — SCHEMA REAL

**Arquivo:** `src/infrastructure/database/corretor.db`  
**Futuro:** PostgreSQL com `tenant_id` em todas as tabelas

---

### `lead`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
nome TEXT, email TEXT, telefone TEXT, origem TEXT
data_ingestao TEXT, status TEXT, tags TEXT, intencao TEXT
tipo_imovel TEXT, faixa_preco TEXT
preco_min REAL, preco_max REAL
quartos INTEGER, vagas INTEGER
metragem_min REAL, metragem_max REAL
bairro_interesse TEXT, regiao_interesse VARCHAR(255), cidade_interesse TEXT
urgencia TEXT, motivo TEXT
utm_source TEXT, utm_medium TEXT, utm_campaign TEXT, utm_term TEXT, utm_content TEXT
canal_preferido TEXT
profile_json TEXT, historico_json TEXT, score_lead REAL
criado_em TEXT DEFAULT datetime('now')
atualizado_em TEXT DEFAULT datetime('now')
```
⚠️ Campo de localização: `cidade_interesse`, `bairro_interesse`, `regiao_interesse` — normalizar antes de usar no IAEngine.

---

### `empreendimentos` (contexto institucional — Sprint 10.5 ✅)
```sql
id INTEGER PRIMARY KEY
nome TEXT, regiao TEXT, bairro TEXT, cidade TEXT, estado TEXT
produto TEXT, endereco TEXT, data_entrega TEXT, status_entrega TEXT
tipo TEXT, descricao TEXT, periodo_lancamento TEXT
amenities TEXT          -- JSON
padrao_construtivo TEXT -- JSON
total_unidades INTEGER
incorporadora_id INTEGER → incorporadora(id)
proprietario_id INTEGER → construtoras(id)
spe_id INTEGER → spe(id)
unidade_referencia_id INTEGER → unidades(id)
```
⚠️ Não tem mais: `preco`, `tipologia`, `metragem_min`, `metragem_max` — removidos na Sprint 10.5.

---

### `unidades` (entidade comercializável — Sprint 10.5 ✅)
```sql
id INTEGER PRIMARY KEY
empreendimento_id INTEGER NOT NULL → empreendimentos(id)
codigo_unidade TEXT
preco REAL, metragem REAL
dormitorios INTEGER, suites INTEGER, vagas INTEGER
tipo_unidade TEXT   -- studio / 1dorm / garden / cobertura / casa
andar INTEGER
disponibilidade TEXT  -- disponível / vendido / reservado
descricao_unidade TEXT
observacoes TEXT
created_at TEXT
```

---

### `unidade_referencia`
```sql
id INTEGER PRIMARY KEY
unidade_id INTEGER → unidades(id)
descricao TEXT
created_at TEXT
```

---

### `unidade_referencia_tipo`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
nome TEXT NOT NULL
```

---

### `ia_score`
```sql
id INTEGER PRIMARY KEY
unidade_id INTEGER → unidades(id)   ← ⚠️ era property_id, agora é unidade_id
lead_id INTEGER → lead(id)
similarity REAL
conversion_score REAL
lead_vector TEXT
property_vector TEXT
reasons_json TEXT
created_at TEXT
```

---

### `matching`
```sql
id INTEGER PRIMARY KEY
unidade_id INTEGER → unidades(id)   ← opera por unidade (Sprint 10.5)
lead_id INTEGER → lead(id)
score REAL
created_at TEXT
```

---

### `offer`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
lead_id INTEGER NOT NULL → lead(id)
empreendimento_id INTEGER NOT NULL → empreendimentos(id)
score REAL NOT NULL
rationale TEXT NOT NULL
created_at TEXT DEFAULT datetime('now')
```
⚠️ Offer ainda referencia `empreendimentos` diretamente — avaliar migração para `unidades` em sprint futura.

---

### `historico_unidade`
```sql
id INTEGER PRIMARY KEY
unidade_id INTEGER NOT NULL → unidades(id)
campo TEXT NOT NULL
valor_antigo TEXT, valor_novo TEXT
changed_at TEXT DEFAULT CURRENT_TIMESTAMP
```

---

### `mailing`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
-- Básico: nome, email, telefone, origem, tags
-- Datas: data_ingestao, fonte_arquivo
-- Validação: valido INTEGER, motivo_invalidacao, hash_unico
-- Perfil pessoal: sexo, data_nascimento, idade, estado_civil,
--   nacionalidade, profissao, empresa, cargo, renda_mensal,
--   faixa_renda, escolaridade
-- Endereço: cep, logradouro, numero, complemento,
--   bairro, cidade, estado, pais
-- Perfil imobiliário: intencao, tipo_imovel, faixa_preco,
--   preco_min, preco_max, quartos, vagas,
--   metragem_min, metragem_max, bairro_interesse,
--   cidade_interesse, urgencia, motivo
-- Marketing: utm_source/medium/campaign/term/content,
--   primeiro_contato, ultimo_contato, canal_preferido, score_mailing
-- Auditoria: criado_em, atualizado_em
```

---

### Tabelas auxiliares (não alterar)
```sql
construtoras(id, nome, cnpj, contato, observacoes, fonte, data_registro, usuario_id, justificativa)
imobiliarias(id, nome, cnpj, contato, observacoes)
corretores(id, nome, telefone, email, creci, observacoes)
incorporadora(id, nome, cnpj, reputacao, historico_obra)
spe(id, nome, cnpj, observacoes)
importacoes(id, tipo, arquivo, origem, total_registros, status, data_execucao, sucesso, erros, log)
```

### Tabelas de relacionamento N:N (não alterar)
```sql
construtora_imobiliaria(construtora_id PK, imobiliaria_id PK, tipo_parceria, observacoes)
corretor_imobiliaria(corretor_id PK, imobiliaria_id PK, tipo_vinculo, observacoes)
corretor_unidade(corretor_id PK, unidade_id PK, tipo_vinculo, observacoes)
incorporadora_imobiliaria(incorporadora_id PK, imobiliaria_id PK, observacoes)
```

---

## ⚙️ ENGINES EXISTENTES

| Engine | Sprint | Função |
|---|---|---|
| Mailing Engine | 6 | Ingestão e normalização de mailings |
| Lead Engine | 7 | Criação e gestão de leads |
| Offer Engine | 8 | Geração de ofertas heurísticas |
| Matching Engine | 9 | Cruzamento lead × imóvel |
| IA Engine v1 | 10 | Vetorização + similaridade + conversão |

**Todos seguem o mesmo padrão:** Engine + Service + Repository + CLI + Exporter + WhatsApp Formatter

---

## 🤖 IA ENGINE v1 (Sprint 10) — IMPLEMENTADO

**Localização:**
```
src/application/ia/services/ia_service.py
src/application/ia/engine/ia_engine.py
src/domain/ia/dto/
src/domain/ia/entities/
src/infrastructure/ia/repositories/ia_repository.py
src/interface/cli/ia_cli.py
```

**O que faz:**
- Vetorização numérica do lead e do imóvel
- Cosine similarity entre vetores
- Previsão inicial de conversão (`conversion_score`)
- `reasons_json` explicável em linguagem comercial
- Normalização automática de campos `*_interesse` do lead
- Persistência em `ia_score`

**Limitações conhecidas (v1):**
- Não usa embeddings textuais
- Não interpreta `profile_json` nem descrições
- Similaridade baixa para vetores de magnitude muito diferente
- Depende da estrutura atual da tabela `empreendimentos`

**Correções críticas aplicadas na Sprint 10:**
- Campo `quartos` removido do vetor do imóvel (não existe na tabela)
- Normalização de `cidade_interesse → cidade`, `bairro_interesse → bairro`
- Ajuste de pesos para urgência e localização
- Debug estruturado implementado

---

## 🚧 SPRINT 10.5 — EM ANDAMENTO

### ✅ Infraestrutura de dados: CONCLUÍDA

O banco está estável, limpo e pronto para ingestão. As quatro tabelas principais foram recriadas corretamente:

- `empreendimentos` — virou contexto institucional (sem preco, tipologia, metragem_min/max)
- `unidades` — nova entidade comercializável real
- `unidade_referencia` — histórico de snapshots para aprendizado da IA
- `offer` — alinhada ao novo schema

Todas sem colunas duplicadas, com FKs reais e estrutura consistente.

**Views corrigidas:**
- `vw_empreendimentos_completos`
- `vw_unidades_completas`
- `vw_tipologia_limpa`

**Tabelas auxiliares intactas (não mexer):**
`construtoras, imobiliarias, corretores, incorporadora,
construtora_imobiliaria, corretor_imobiliaria, corretor_unidade,
incorporadora_imobiliaria, lead, mailing, spe, importacoes, ia_score, matching`

**Índices:** apenas os do mailing estão presentes — correto.

---

### 🔄 Fase atual: Alinhamento do código ao novo schema

O próximo passo imediato é revisar e atualizar todo código da aplicação que acessa as tabelas refatoradas.

**O que revisar por tabela (`empreendimentos`, `unidades`, `unidade_referencia`, `offer`):**

1. **Queries SQL** — SELECT, INSERT, UPDATE, DELETE, JOINs, FKs, Views
2. **Models / DTOs / Classes** — campos removidos, renomeados, novos FK, tipos de dados
3. **Services dependentes** — ingestão, matching, IA, geração de ofertas, dashboards, APIs
4. **Endpoints de API** — `GET /empreendimentos`, `GET /unidades`, `GET /unidades/completas`, `POST /offer`, etc.
5. **Scripts de ingestão** — mapeamento de colunas, validação, normalização, criação de `unidade_referencia`

---

### 📋 Schema das tabelas novas/refatoradas

**`empreendimentos`** (contexto institucional)
```
nome, regiao, bairro, cidade, estado, produto, endereco,
data_entrega, status_entrega, tipo, descricao, periodo_lancamento,
amenities (JSON), padrao_construtivo (JSON), total_unidades,
incorporadora_id, proprietario_id, spe_id, unidade_referencia_id
```

**`unidades`** (entidade comercializável)
```
id, empreendimento_id, codigo_unidade, preco, metragem,
dormitorios, suites, vagas, tipo_unidade, andar,
disponibilidade, descricao_unidade, created_at
```

**`unidade_referencia`** (histórico de snapshots)
```
id, empreendimento_id, unidade_id, codigo, preco, metragem,
dormitorios, vagas, tipo_unidade, data_referencia, created_at
```

---

### 📄 Modelo de planilha para ingestão

**Para empreendimentos:** nome, regiao, bairro, cidade, estado, produto, endereco,
data_entrega, status_entrega, tipo, descricao, periodo_lancamento,
amenities, padrao_construtivo, total_unidades, incorporadora_id, proprietario_id, spe_id

**Para unidades:** empreendimento_id, codigo_unidade, preco, metragem,
dormitorios, suites, vagas, tipo_unidade, andar, disponibilidade, descricao_unidade

**Para unidade_referencia:** unidade_id, descricao

---

### ✅ Checklist final antes da ingestão real

- [ ] Revisar todos os repositórios que acessam tabelas refatoradas
- [ ] Atualizar DTOs com campos corretos
- [ ] Atualizar Services (matching, IA, offer)
- [ ] Atualizar pipeline de ingestão (novo mapeamento de colunas)
- [ ] Testar inserts manuais
- [ ] Testar ingestão com 1 empreendimento + 3 unidades
- [ ] Testar views
- [ ] Testar matching por unidade
- [ ] Testar offer
- [ ] Testar IA (se aplicável)

---

### Fluxo pós-10.5
```
Lead + Unidades → IAEngine (v1.5) → DTO → IARepository → SQLite
```

---

## 🗺️ ROADMAP MACRO

| Sprints | Fase |
|---|---|
| 1–12 | Base do sistema (engines, cadastros, relatórios) |
| 13–22 | Mailing avançado, leads, IA, tráfego pago, automação |
| 23–30 | Multi-tenant, onboarding, billing, SaaS completo |

**Sprint 11 (prevista):** IA Vetorial v2 — embeddings reais, vetorização semântica, pesos dinâmicos, aprendizado contínuo.

---

## 📋 GOVERNANÇA DE SPRINTS

**Início de sprint:**
- Criar branch
- Travar escopo
- C4 inicial

**Fim de sprint:**
- Documentação técnica
- C4 final + XML draw.io
- Git: branch → merge → release → tag
- Mover pendências para backlog

**Regras fixas:**
- Sem alterar escopo durante sprint
- Sem reabrir sprint encerrada
- Sem discussões técnicas no encerramento

---

## 💡 INSTRUÇÕES PARA O CLAUDE CODE

Quando receber instruções nesta sessão:

1. **Sempre ler os arquivos existentes antes de criar novos** — nunca assuma estrutura sem verificar
2. **Nunca criar campos que não existam no banco** — verificar schema.sql antes de qualquer query
3. **Seguir os padrões de DTO, Service, Engine e Repository** descritos acima
4. **Normalizar campos `*_interesse` do lead** antes de qualquer operação de IA ou matching
5. **CLI sempre chama Service** — nunca Engine diretamente
6. **Engines são lógica pura** — sem sqlite3, sem I/O de arquivo
7. **Ao gerar código novo**, perguntar antes se há dúvida sobre campo existente no banco
8. **Documentação de sprint** sempre inclui: objetivo, escopo, arquitetura, decisões, validações, resultado
9. **Ao iniciar Sprint 10.5**, começar pela criação da tabela `unidades` e migração de dados

---

## 🚨 DIRETRIZ DE QUALIDADE ARQUITETURAL

**Instrução permanente:** Sempre que uma solução proposta ou código gerado não estiver aderente à arquitetura planejada, alertar ANTES de gerar o código, indicando:
- O que está fora do padrão
- Por que isso vai gerar retrabalho
- A alternativa correta

Nunca gerar código que force gambiarra na arquitetura para resolver um problema pontual.

---

## 🖥️ CLI → API → UI: ESTRATÉGIA DE EVOLUÇÃO

### Situação atual
Toda interação é via CLI. Isso é correto para o MVP mas **o código já deve ser escrito pensando na camada de API**.

### Regra crítica para todo código novo
**Services nunca devem depender da CLI.** Se um service está bem escrito, expor via API é apenas criar um controller/router que chama o mesmo service. Isso já está no contrato de arquitetura mas precisa ser reforçado:

```
CLI → Service → Engine → Repository   (hoje)
API → Service → Engine → Repository   (futuro — mesmo service, nova interface)
```

### Estrutura de API planejada
```
src/interface/api/
├── routers/          ← FastAPI routers por módulo
├── controllers/      ← recebem request, chamam service, retornam response
└── dtos/             ← request/response DTOs da API (diferentes dos internos)
```

Stack recomendada: **FastAPI** — assíncrono, tipado, gera documentação Swagger automática, padrão de mercado para Python APIs.

### O que isso significa na prática
Ao criar qualquer service novo, perguntar: *"um controller de API conseguiria chamar este service sem modificá-lo?"* Se a resposta for não, o service está errado.

### Visão da UI futura
- Dashboard com métricas de conversão em tempo real
- Kanban de leads por estágio
- Mapa de calor de imóveis por região
- Feed de recomendações da IA por corretor
- Painel de tráfego pago integrado
- Mobile-first para corretores em campo
- UX encantadora e vendedora — não apenas funcional

---

## 🏠 INTELIGÊNCIA DE MERCADO IMOBILIÁRIO

Comportamentos e padrões do mercado brasileiro que devem informar decisões de produto e IA:

### Comportamento do comprador
- **Ciclo longo de decisão:** média de 6 a 18 meses entre primeiro contato e assinatura. O follow-up precisa ser persistente e inteligente, não agressivo.
- **Múltiplos decisores:** na maioria dos casos, cônjuge/família decide junto. O lead individual raramente decide sozinho — o `profile_json` pode capturar isso.
- **Ancoragem de preço:** compradores tendem a aceitar valores acima do topo da faixa declarada quando o imóvel entrega muito valor percebido. A IA deve considerar até 15-20% acima do `preco_max` declarado se o match de outros atributos for muito alto.
- **Urgência real vs. declarada:** urgência declarada ("preciso em 3 meses") raramente é real. Mas urgência combinada com evento de vida (casamento, filho, mudança de cidade) é altamente preditiva de conversão. Capturar `motivo` com granularidade é crítico.

### Comportamento do corretor
- **Regra 80/20 extrema:** 20% dos corretores geram 80% das vendas. A plataforma deve identificar e priorizar esses perfis.
- **Velocidade é tudo:** lead contactado em menos de 5 minutos tem conversão 9x maior. Automação de primeiro contato é prioridade.
- **Corretor trabalha com portfólio limitado:** conhece bem 5 a 15 empreendimentos. A IA deve recomendar além do portfólio habitual.
- **Resistência a tecnologia:** UX precisa ser simples e gerar resultado visível rápido. Dashboard deve mostrar "você ganhou X com esses leads esta semana".

### Padrões de imóvel que impactam conversão
- **Tipologia:** studios e 1 dormitório têm ciclo mais curto (investidor/solteiro). 3+ dormitórios têm ciclo mais longo (família). O IAEngine deve calibrar `urgencia_score` por tipologia.
- **Fase do empreendimento:** lançamento tem maior desconto e maior risco percebido. Pronto para morar tem conversão mais rápida. `status_entrega` + `data_entrega` devem ser fatores explícitos no vetor da unidade.
- **Planta vs. entregue:** comprador de planta tolera preço mais alto. Comprador de pronto quer desconto ou benefício imediato.
- **Vagas de garagem:** em São Paulo e capitais grandes, 0 vaga é deal-breaker para família. Deve ter peso alto no matching.

### Sazonalidade
- **Picos de venda:** março-abril (após carnaval) e agosto-outubro. Evitar lançamentos em dezembro-janeiro.
- **Tráfego pago:** CPC sobe em picos de mercado — a plataforma deve cruzar sazonalidade com orçamento de tráfego.

### Dados que aumentam conversão quando capturados
- Evento de vida: casamento, filho nascendo, aposentadoria, mudança de cidade
- Tipo de financiamento pretendido: FGTS, Minha Casa Minha Vida, financiamento puro, à vista
- Já tem imóvel para vender (comprador que precisa vender antes)
- Já foi atendido por outro corretor (lead quente mas insatisfeito)

### Sugestões de features de produto baseadas nisso
1. **Score de momento de compra** — cruzar urgência + evento de vida + tempo desde primeiro contato → prever janela de fechamento
2. **Alerta de reaquecimento de lead** — lead frio que volta a interagir (abre email, clica em link) deve gerar notificação imediata ao corretor
3. **Simulador de oferta** — dado o perfil do lead, simular qual combinação de condições (desconto, parcela, FGTS) maximiza conversão
4. **Ranking de empreendimentos por perfil de comprador** — não apenas matching genérico, mas *"para este perfil de lead, historicamente qual empreendimento converte mais"*
5. **Integração com calendário** — agendar follow-up automático baseado no ciclo médio de decisão do perfil