# ADR-004: Ingestão Central - idempotência e deduplicação por sessão

Status: Proposto / Aceito

Contexto
- A Ingestão Central processa linhas de uma planilha mestre contendo dados de várias entidades.
- Sem controle, a ingestão pode criar duplicatas de entidades já existentes dentro da mesma execução ou entre execuções diferentes.
- Queremos evitar duplicação indesejada durante a ingestão, mantendo a capacidade de cadastrar ou reusar entidades com base em chaves de negócio estáveis.

Decisão
- Implementar deduplicação durante a ingestão usando um cache de sessão em memória (In-Memory Session Cache) por execução.
- A Ingestão Central deve:
  - Manter um cache por tipo de entidade (construtora, imobiliária, corretor, incorporadora, empreendimento) com uma chave de cache baseada em campos de negócio (ex.: nome + cpf/cnpj + telefone + email, conforme aplicável).
  - Reusar entidades já criadas no decorrer da mesma execução via cache, sem re-gerar IDs.
  - Registrar e retornar as entidades criadas/reutilizadas para cada linha processada.
  - Limpar o cache no início de cada nova invocação de executar(registros).
- Importante: o cache é apenas por execução (sessão em memória). Dados persistidos no banco devem evitar duplicatas entre execuções por meio de constraints (quando possível) ou por regras de negócio adicionais.
- Não eliminar duplicatas existentes no banco (a menos que seja parte de uma migração controlada). O objetivo é evitar duplicação durante a ingestão.

Consequências
- Vantagens:
  - Ingestão mais rápida (evita queries redundantes).
  - Garante idempotência por execução para o conjunto de linhas processadas.
  - Menor probabilidade de duplicação de entidades criadas a partir da mesma planilha.
- Desvantagens/Riscos:
  - Consumo de memória proporcional ao tamanho da ingestão (cache em memória).
  - Em cenários de ingestão paralela (multithreading/processos concorrentes), é necessário coordenação adicional (ex.: cache distribuído como Redis) para manter idempotência global.
  - Dados fora do fluxo atual (ou ingestões com diferenças de chave de negócio) podem exigir regras adicionais.
- Em relação a modelos existentes:
  - DTOs de criação devem suportar a re-use (get_or_create) quando possível.
  - Serviços de cada entidade devem retornar a instância existente quando encontrada pelo cache/uniqueness.

Alternativas consideradas
- Usar UNIQUE CONSTRAINTS/UPSERTs no banco de dados: mais seguro para evitar duplicatas em produção, porém pode exigir uma lógica de upsert muito cuidadosa e ainda não resolve duplicação dentro da mesma execução sem um mecanismo de identidade.
- Mantê-lo apenas no nível da aplicação (injeção de dependência): boa para desempenho, mas menos robusto em cenários de falha.
- Usar um cache distribuído (ex.: Redis) para ingestões multijogadores: mais complexo, mas necessário se houver ingestões concorrentes em múltiplos processos.

Rationale
- Performance: reduzir chamadas redundantes ao repositório.
- Consistência: evitar duplicação em uma única linha de ingestão.
- Simplicidade: a solução de cache de sessão é relativamente simples de implementar nos lugares já existentes (IngestaoCentral).

Implantação / Implementação
- Altere IngestaoCentral para:
  - Criar e manter self.cache_sessao no início de executar(registros).
  - Usar chaves normalizadas (lowercased/striped) para entidades na cache.
  - Reusar entidades a partir do cache quando encontradas.
  - Limpar ou re-inicializar o cache a cada nova invocação.
- Adicionar testes de integração que cubram:
  - Mesma linha repetida não gera duplicatas de entidades criadas.
  - Linhas diferentes com mesmo dados geram apenas uma instância por entidade.
  - Certificar que o retorno contém as referências corretas (empreendimento, unidade, etc.) sem duplicação.
- Observação sobre persistência: mantenha as constraints existentes para evitar inconsistências entre executões, se aplicável.

Efeitos colaterais
- Memória ocupada durante a ingestão: considerar limites para ingestões muito grandes.
- Em cenários de concorrência, pode ser necessário evoluir para cache distribuído.

Referências
- ADR-001 (padrões de arquitetura/ADR já existentes)
- Branche de Ingestão Central e DTOs: ConstrutoraInputDTO, ImobiliariaInputDTO, etc.

Plano de validação
- Criar casos de teste de ingestão com dados duplicados na mesma planilha para confirmar que não há duplicação durante a execução.
- Rodar a ingestão com dados simulados e comparar resultados com expectativas.

# ADR-004 — Ingestão Idempotente e Cache de Sessão

**Status:** Aceito (Sprint 10.5)
**Data:** 2026

---

## Contexto

Durante a Sprint 10.5, identificamos que a Ingestão Central, ao ler planilhas com múltiplas linhas referenciando a mesma entidade (ex: 50 apartamentos do mesmo prédio, com o mesmo corretor e a mesma incorporadora), estava gerando dezenas de registros duplicados no banco de dados.

O banco SQLite estava recebendo comandos `INSERT` repetidos porque o Ingestor não tinha memória do que havia acabado de processar na linha anterior durante a mesma sessão de execução.

---

## Decisão

Adotar o padrão de **Cache de Sessão em Memória (In-Memory Session Cache)** para todos os Ingestores da plataforma.

### Regras de Implementação:
1. O método `executar()` do Ingestor deve inicializar um dicionário vazio `self.cache_sessao` para mapear os itens instanciados (por entidade e por relacionamento).
2. Para cada linha lida, antes de acionar o `Service.cadastrar()`, o Ingestor deve verificar no cache se a chave única daquela entidade (ex: `nome_em_minusculas` ou `ID_A_ID_B` para N:N) já existe.
3. Se existir no cache: o objeto da memória é reaproveitado (não vai ao banco).
4. Se não existir: a entidade é cadastrada, e a entidade retornada vira um novo valor no dicionário de cache.
5. O cache deve ser destruído/resetado a cada nova invocação pública de ingestão para não comprometer a memória a longo prazo.

### Consequências
- **Vantagem:** Redução drástica de hits ao banco de dados, aumentando a velocidade da ingestão (I/O).
- **Vantagem:** Idempotência garantida na mesma planilha (evita lixo e duplicates).
- **Vantagem:** Relacionamentos (Foreign Keys) corretos e normalizados na origem.
- **Custo:** Suave aumento no consumo de memória RAM durante o loop da ingestão.

---

> 📌 **Rodapé:** Problema corrigido na Sprint 10.5. 
> Veja o impacto nas [Sprints 10.5 — Migração](../sprints/sprint10.5/sprint-10-5-migracao.md) e o contrato base [ADR-001](adr-001-contrato-arquitetura.md).