import json
from pathlib import Path

# Serviços e repositórios reais
from src.application.lead.services.lead_service import LeadService
from src.infrastructure.lead.repositories.lead_repository import LeadRepository

from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository

# IMPORT CORRETO — ESSA LINHA É O QUE FALTAVA
from src.domain.lead.dto.lead_input_dto import LeadInputDTO
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO


# Caminho ABSOLUTO para a pasta tests/data
BASE = Path(__file__).resolve().parent.parent / "tests" / "data"


def load_leads():
    path = BASE / "leads.json"
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return

    print("\n=== CARREGANDO LEADS ===")
    service = LeadService(LeadRepository())

    with open(path, "r", encoding="utf-8") as f:
        leads = json.load(f)

    for item in leads:
        dto = LeadInputDTO(
            nome=item["nome"],
            email=item["email"],
            telefone=item["telefone"],
            origem="json_test",
            tags=None,

            intencao=None,
            tipo_imovel=item["tipo_imovel"],
            faixa_preco=None,
            preco_min=item["preco_min"],
            preco_max=item["preco_max"],
            quartos=item["quartos"],
            vagas=None,
            metragem_min=item["metragem_min"],
            metragem_max=item["metragem_max"],
            bairro_interesse=item["bairro_interesse"],
            cidade_interesse=item["cidade_interesse"],
            urgencia=item["urgencia"],
            motivo=None,
            regiao_interesse=item["regiao_interesse"],

            utm_source=None,
            utm_medium=None,
            utm_campaign=None,
            utm_term=None,
            utm_content=None,
            canal_preferido=None,

            dados_completos=None
        )

        criado = service.cadastrar(dto)
        print(f"Lead criado: {criado.id} - {criado.nome}")


def load_empreendimentos():
    path = BASE / "empreendimentos.json"
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return

    print("\n=== CARREGANDO EMPREENDIMENTOS ===")
    service = EmpreendimentoService(EmpreendimentoRepository())

    with open(path, "r", encoding="utf-8") as f:
        emps = json.load(f)

    for item in emps:
        dto = EmpreendimentoInputDTO(
            nome=f"Emp {item['id']}",
            cidade=item["cidade"],
            regiao=item["regiao"],
            bairro=item["bairro"],
            tipo=item["tipo"],
            tipologia=item["tipologia"],
            quartos=item["quartos"],
            metragem_min=item["metragem_min"],
            metragem_max=item["metragem_max"],
            preco=item["preco"],
            estado="SP",
            produto="Residencial",
            endereco="Endereço Teste",
            data_entrega="2025-12-01",
            status_entrega="Em Obras",
            descricao="Importado via JSON",
            proprietario_id=None,
            incorporadora_id=None,
            unidade_referencia_id=None,
            spe_id=None,
            periodo_lancamento="2024"
        )

        criado = service.cadastrar(dto)
        print(f"Empreendimento criado: {criado.id} - {criado.nome}")


if __name__ == "__main__":
    print("\n=== IMPORTAÇÃO DE DADOS DE TESTE (JSON → BANCO) ===")
    print(f"Usando BASE = {BASE}")
    load_leads()
    load_empreendimentos()
    print("\n=== FIM DA IMPORTAÇÃO ===\n")
