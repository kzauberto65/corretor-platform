from src.ingestao.normalizador import Normalizador
from src.servicos.construtora_service import ConstrutoraService
from src.servicos.imobiliaria_service import ImobiliariaService
from src.servicos.corretor_service import CorretorService
from src.servicos.empreendimento_service import EmpreendimentoService
from src.servicos.unidade_referencia_service import UnidadeReferenciaService
from src.servicos.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.servicos.corretor_imobiliaria_service import CorretorImobiliariaService
from src.servicos.incorporadora_service import IncorporadoraService


class IngestaoCentral:

    def __init__(self):
        self.norm = Normalizador()

        self.construtora_service = ConstrutoraService()
        self.imobiliaria_service = ImobiliariaService()
        self.corretor_service = CorretorService()
        self.empreendimento_service = EmpreendimentoService()
        self.unidade_referencia_service = UnidadeReferenciaService()
        self.incorporadora_service = IncorporadoraService()

        self.rel_construtora_imobiliaria = ConstrutoraImobiliariaService()
        self.rel_corretor_imobiliaria = CorretorImobiliariaService()

    def executar(self, registros):
        resultados = []
        erros = []

        for linha in registros:
            try:
                resultado = self._processar_linha(linha)
                resultados.append(resultado)
            except Exception as e:
                erros.append({
                    "linha": linha,
                    "erro": str(e)
                })

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
            construtora = self.construtora_service.criar_construtora(nome=nome_construtora)

        # -----------------------------
        # IMOBILIÁRIA
        # -----------------------------
        nome_imobiliaria = self.norm.texto(r.get("Imobiliaria"))
        imobiliaria = None
        if nome_imobiliaria:
            imobiliaria = self.imobiliaria_service.criar_imobiliaria(nome=nome_imobiliaria)

        # -----------------------------
        # CORRETOR
        # -----------------------------
        nome_corretor = self.norm.texto(r.get("Corretor"))
        telefone = self.norm.limpar_telefone(r.get("Telefone"))
        email = self.norm.texto(r.get("Email"))
        corretor = None
        if nome_corretor:
            corretor = self.corretor_service.criar_corretor(
                nome=nome_corretor,
                telefone=telefone,
                email=email
            )

        # -----------------------------
        # UNIDADE REFERÊNCIA
        # -----------------------------
        codigo_unidade = self.norm.texto(r.get("UnidadeReferencia"))
        unidade_ref = None
        if codigo_unidade:
            unidade_ref = self.unidade_referencia_service.criar_ou_obter(
                codigo=codigo_unidade
            )

        # -----------------------------
        # INCORPORADORA (FK)
        # -----------------------------
        nome_incorporadora = self.norm.texto(r.get("Incorporadora"))
        incorporadora = None
        if nome_incorporadora:
            incorporadora = self.incorporadora_service.criar_ou_obter(nome_incorporadora)

        # -----------------------------
        # EMPREENDIMENTO
        # -----------------------------
        nome_emp = self.norm.texto(r.get("Empreendimento"))

        empreendimento = self.empreendimento_service.criar_empreendimento(
            nome=nome_emp,
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
            unidade_referencia_id=unidade_ref["id"] if unidade_ref else None,
            preco=self.norm.moeda(r.get("Valor")),
            spe_id=self.norm.texto(r.get("SPE_ID")),
            incorporadora_id=incorporadora["id"] if incorporadora else None
        )

        # -----------------------------
        # RELACIONAMENTOS
        # -----------------------------
        if construtora and imobiliaria:
            self.rel_construtora_imobiliaria.vincular(
                construtora_id=construtora["id"],
                imobiliaria_id=imobiliaria["id"]
            )

        if corretor and imobiliaria:
            self.rel_corretor_imobiliaria.vincular(
                corretor_id=corretor["id"],
                imobiliaria_id=imobiliaria["id"]
            )

        return {
            "construtora": construtora,
            "imobiliaria": imobiliaria,
            "corretor": corretor,
            "empreendimento": empreendimento,
            "unidade_referencia": unidade_ref,
            "incorporadora": incorporadora
        }