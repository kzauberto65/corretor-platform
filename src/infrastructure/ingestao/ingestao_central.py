from src.infrastructure.ingestao.normalizador import Normalizador

# ============================
# REPOSITORIES
# ============================
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository
from src.infrastructure.imobiliaria.repositories.imobiliaria_repository import ImobiliariaRepository
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.infrastructure.unidade_referencia.repositories.unidade_referencia_repository import UnidadeReferenciaRepository
from src.infrastructure.incorporadora.repositories.incorporadora_repository import IncorporadoraRepository
from src.infrastructure.construtora_imobiliaria.repositories.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository
from src.infrastructure.corretor_imobiliaria.repositories.corretor_imobiliaria_repository import CorretorImobiliariaRepository

# ============================
# SERVICES
# ============================
from src.application.construtora.services.construtora_service import ConstrutoraService
from src.application.imobiliaria.services.imobiliaria_service import ImobiliariaService
from src.application.corretor.services.corretor_service import CorretorService
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.application.unidade_referencia.services.unidade_referencia_service import UnidadeReferenciaService
from src.application.incorporadora.services.incorporadora_service import IncorporadoraService
from src.application.construtora_imobiliaria.services.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.application.corretor_imobiliaria.services.corretor_imobiliaria_service import CorretorImobiliariaService

# ============================
# DTOs
# ============================
from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO
from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO
from src.domain.unidade_referencia.dto.unidade_referencia_input_dto import UnidadeReferenciaInputDTO
from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO


class IngestaoCentral:

    def __init__(self):
        self.norm = Normalizador()

        # SERVICES + REPOSITORIES
        self.construtora_service = ConstrutoraService(ConstrutoraRepository())
        self.imobiliaria_service = ImobiliariaService(ImobiliariaRepository())
        self.corretor_service = CorretorService(CorretorRepository())
        self.empreendimento_service = EmpreendimentoService(EmpreendimentoRepository())
        self.unidade_referencia_service = UnidadeReferenciaService(UnidadeReferenciaRepository())
        self.incorporadora_service = IncorporadoraService(IncorporadoraRepository())

        self.rel_construtora_imobiliaria = ConstrutoraImobiliariaService(ConstrutoraImobiliariaRepository())
        self.rel_corretor_imobiliaria = CorretorImobiliariaService(CorretorImobiliariaRepository())

    def executar(self, registros):
        resultados = []
        erros = []

        for linha in registros:
            try:
                resultado = self._processar_linha(linha)
                resultados.append(resultado)
            except Exception as e:
                erros.append({"linha": linha, "erro": str(e)})

        return {
            "sucesso": len(resultados),
            "erros": erros,
            "resultados": resultados
        }

    def _processar_linha(self, r):

        # -----------------------------
        # CONSTRUTORA
        # -----------------------------
        nome_construtora = self.norm.texto(r.get("Construtora"))
        construtora = None
        if nome_construtora:
            dto = ConstrutoraInputDTO(
                nome=nome_construtora,
                cnpj=None,
                contato=None,
                observacoes=None,
                fonte="ingestao",
                data_registro=None,
                usuario_id=None,
                justificativa=None
            )
            construtora = self.construtora_service.cadastrar(dto)

        # -----------------------------
        # IMOBILIÁRIA
        # -----------------------------
        nome_imobiliaria = self.norm.texto(r.get("Imobiliaria"))
        imobiliaria = None
        if nome_imobiliaria:
            dto = ImobiliariaInputDTO(
                nome=nome_imobiliaria,
                cnpj=None,
                contato=None,
                observacoes=None
            )
            imobiliaria = self.imobiliaria_service.cadastrar(dto)

        # -----------------------------
        # CORRETOR
        # -----------------------------
        nome_corretor = self.norm.texto(r.get("Corretor"))
        telefone = self.norm.limpar_telefone(r.get("Telefone"))
        email = self.norm.texto(r.get("Email"))
        corretor = None
        if nome_corretor:
            dto = CorretorInputDTO(
                nome=nome_corretor,
                telefone=telefone,
                email=email,
                creci=None,
                observacoes=None
            )
            corretor = self.corretor_service.cadastrar(dto)

        # -----------------------------
        # UNIDADE REFERÊNCIA
        # -----------------------------
        codigo_unidade = self.norm.texto(r.get("UnidadeReferencia"))
        unidade_ref = None
        if codigo_unidade:
#            dto = UnidadeReferenciaInputDTO(codigo=codigo_unidade)
            unidade_ref = self.unidade_referencia_service.criar_ou_obter(codigo_unidade)

        # -----------------------------
        # INCORPORADORA
        # -----------------------------
        nome_incorporadora = self.norm.texto(r.get("Incorporadora"))
        incorporadora = None
        if nome_incorporadora:
            dto = IncorporadoraInputDTO(
                nome=nome_incorporadora,
                cnpj=None,
                reputacao=None,
                historico_obra=None
            )
            incorporadora = self.incorporadora_service.cadastrar(dto)

        # -----------------------------
        # EMPREENDIMENTO
        # -----------------------------
        dto = EmpreendimentoInputDTO(
            nome=self.norm.texto(r.get("Empreendimento")),
            regiao=self.norm.texto(r.get("Regiao")),
            bairro=self.norm.texto(r.get("Bairro")),
            cidade=self.norm.texto(r.get("Cidade")),
            estado=self.norm.texto(r.get("Estado")),
            produto=self.norm.texto(r.get("Produto")),
            endereco=self.norm.texto(r.get("Endereco")),
            tipologia=self.norm.texto(r.get("Tipologia")),
            data_entrega=self.norm.data(r.get("DataEntrega")),
            status_entrega=self.norm.texto(r.get("StatusEntrega")),
            tipo=self.norm.texto(r.get("Tipo")),
            descricao=self.norm.texto(r.get("Descricao")),
            periodo_lancamento=self.norm.texto(r.get("PeriodoLancamento")),
            unidade_referencia_id=unidade_ref.id if unidade_ref else None,
            preco=self.norm.moeda(r.get("Valor")),
            spe_id=None,
            incorporadora_id=incorporadora.id if incorporadora else None,
            proprietario_id=None
        )

        empreendimento = self.empreendimento_service.cadastrar(dto)

        # -----------------------------
        # RELACIONAMENTOS (SEM CHECAGEM)
        # -----------------------------
        if construtora and imobiliaria:
            rel_dto = ConstrutoraImobiliariaInputDTO(
                construtora_id=construtora.id,
                imobiliaria_id=imobiliaria.id,
                tipo_parceria=None,
                observacoes=None
            )
            self.rel_construtora_imobiliaria.cadastrar(rel_dto)

        if corretor and imobiliaria:
            rel_dto = CorretorImobiliariaInputDTO(
                corretor_id=corretor.id,
                imobiliaria_id=imobiliaria.id,
                tipo_vinculo=None,
                observacoes=None
            )
            self.rel_corretor_imobiliaria.cadastrar(rel_dto)

        return {
            "construtora": construtora,
            "imobiliaria": imobiliaria,
            "corretor": corretor,
            "empreendimento": empreendimento,
            "unidade_referencia": unidade_ref,
            "incorporadora": incorporadora
        }
