# ============================================================
# INGESTOR: IngestaoCentral
# Camada: infrastructure/ingestao/
# Descrição: Orquestra a ingestão completa de uma planilha mestre
#            que contém dados de múltiplas entidades por linha:
#            construtora, imobiliária, corretor, incorporadora,
#            empreendimento e unidades.
#
# Pipeline por linha:
#   1. Construtora → cadastrar ou reusar
#   2. Imobiliária → cadastrar ou reusar
#   3. Corretor    → cadastrar ou reusar
#   4. Incorporadora → cadastrar ou reusar
#   5. Empreendimento → cadastrar ou reusar
#   6. Unidade → cadastrar (vinculada ao empreendimento)
#   6.1. Financiamento → cadastrar default vinculado à unidade
#   7. Relacionamentos N:N → cadastrar ou reusar
#
# Sprint 10.5: Cache de Sessão (In-Memory) implementado para evitar 
#              duplicação de registros lidos da mesma planilha.
# ============================================================

from src.infrastructure.ingestao.normalizador import Normalizador

# Repositories
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository
from src.infrastructure.imobiliaria.repositories.imobiliaria_repository import ImobiliariaRepository
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository
from src.infrastructure.incorporadora.repositories.incorporadora_repository import IncorporadoraRepository
from src.infrastructure.construtora_imobiliaria.repositories.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository
from src.infrastructure.corretor_imobiliaria.repositories.corretor_imobiliaria_repository import CorretorImobiliariaRepository
# NOVO: Import repositório de Financiamento
from src.infrastructure.financiamento.repositories.financiamento_repository import FinanciamentoRepositorySQLite

# Services
from src.application.construtora.services.construtora_service import ConstrutoraService
from src.application.imobiliaria.services.imobiliaria_service import ImobiliariaService
from src.application.corretor.services.corretor_service import CorretorService
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.application.unidade.services.unidade_service import UnidadeService
from src.application.incorporadora.services.incorporadora_service import IncorporadoraService
from src.application.construtora_imobiliaria.services.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.application.corretor_imobiliaria.services.corretor_imobiliaria_service import CorretorImobiliariaService
# NOVO: Import serviço de Financiamento
from src.application.financiamento.services.financiamento_service import FinanciamentoService

# DTOs
from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO
from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO
from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO
# NOVO: Import DTO de Financiamento
from src.domain.financiamento.dto.tabela_financiamento_input_dto import TabelaFinanciamentoInputDTO


class IngestaoCentral:
    """Ingestor central com Cache de Sessão para deduplicação."""

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.norm = Normalizador()

        self.construtora_service = ConstrutoraService(ConstrutoraRepository(db_path))
        self.imobiliaria_service = ImobiliariaService(ImobiliariaRepository(db_path))
        self.corretor_service = CorretorService(CorretorRepository(db_path))
        self.empreendimento_service = EmpreendimentoService(EmpreendimentoRepository(db_path))
        self.unidade_service = UnidadeService(UnidadeRepository(db_path))
        self.incorporadora_service = IncorporadoraService(IncorporadoraRepository(db_path))
        self.rel_construtora_imobiliaria = ConstrutoraImobiliariaService(ConstrutoraImobiliariaRepository(db_path))
        self.rel_corretor_imobiliaria = CorretorImobiliariaService(CorretorImobiliariaRepository(db_path))
        
        # NOVO: Serviço de financiamento injetado
        self.financiamento_service = FinanciamentoService(FinanciamentoRepositorySQLite(db_path))

    def executar(self, registros: list[dict]) -> dict:
        """Processa lista de dicts (rows da planilha)."""
        resultados = []
        erros = []

        # RESET do Cache In-Memory para cada nova execução da Planilha
        # Isso impede duplicações em massa se o item se repetir nas linhas abaixos
        self.cache_sessao = {
            "construtora": {},
            "imobiliaria": {},
            "corretor": {},
            "incorporadora": {},
            "empreendimento": {},
            "unidade": {},  
            "rel_ci": set(),        # Controle de N:N
            "rel_cor_imo": set()    # Controle de N:N
        }

        for i, linha in enumerate(registros, start=1):
            try:
                resultado = self._processar_linha(linha)
                resultados.append(resultado)
            except Exception as e:
                erros.append({"linha": i, "dados": linha, "erro": str(e)})
                print(f"[IngestaoCentral] ❌ Linha {i}: {e}")

        print(f"\n[IngestaoCentral] Concluído: {len(resultados)} linha(s) processada(s), {len(erros)} erro(s)")
        return {
            "sucesso": len(resultados),
            "erros": erros,
            "resultados": resultados
        }

    def _processar_linha(self, r: dict) -> dict:
        # ----------------------------------------------------------
        # 1. CONSTRUTORA (Cadastrar ou Reusar via Cache)
        # ----------------------------------------------------------
        construtora = None
        nome_construtora = self.norm.texto(r.get("construtora"))
        
        if nome_construtora:
            chave_cache = str(nome_construtora).strip().lower()
            if chave_cache in self.cache_sessao["construtora"]:
                construtora = self.cache_sessao["construtora"][chave_cache]
            else:
                dto = ConstrutoraInputDTO(
                    nome=nome_construtora,
                    cnpj=self.norm.limpar_cnpj(r.get("construtora_cnpj")),
                    contato=None, observacoes=None, fonte="ingestao_central",
                    data_registro=None, usuario_id=None, justificativa=None
                )
                construtora = self.construtora_service.cadastrar(dto)
                self.cache_sessao["construtora"][chave_cache] = construtora

        # ----------------------------------------------------------
        # 2. IMOBILIÁRIA (Cadastrar ou Reusar via Cache)
        # ----------------------------------------------------------
        imobiliaria = None
        nome_imobiliaria = self.norm.texto(r.get("imobiliaria"))

        if nome_imobiliaria:
            chave_cache = str(nome_imobiliaria).strip().lower()
            if chave_cache in self.cache_sessao["imobiliaria"]:
                imobiliaria = self.cache_sessao["imobiliaria"][chave_cache]
            else:
                dto = ImobiliariaInputDTO(
                    nome=nome_imobiliaria,
                    cnpj=self.norm.limpar_cnpj(r.get("imobiliaria_cnpj")),
                    contato=None, observacoes=None
                )
                imobiliaria = self.imobiliaria_service.cadastrar(dto)
                self.cache_sessao["imobiliaria"][chave_cache] = imobiliaria

        # ----------------------------------------------------------
        # 3. CORRETOR (Cadastrar ou Reusar via Cache)
        # ----------------------------------------------------------
        corretor = None
        nome_corretor = self.norm.texto(r.get("correto"))
        
        if nome_corretor:
            chave_cache = str(nome_corretor).strip().lower()
            if chave_cache in self.cache_sessao["corretor"]:
                corretor = self.cache_sessao["corretor"][chave_cache]
            else:
                dto = CorretorInputDTO(
                    nome=nome_corretor,
                    telefone=self.norm.limpar_telefone(r.get("telefone")),
                    email=self.norm.texto(r.get("email")),
                    creci=self.norm.texto(r.get("creci")),
                    observacoes=None
                )
                corretor = self.corretor_service.cadastrar(dto)
                self.cache_sessao["corretor"][chave_cache] = corretor

        # ----------------------------------------------------------
        # 4. INCORPORADORA (Cadastrar ou Reusar via Cache)
        # ----------------------------------------------------------
        incorporadora = None
        nome_incorporadora = self.norm.texto(r.get("incorporadora"))
        
        if nome_incorporadora:
            chave_cache = str(nome_incorporadora).strip().lower()
            if chave_cache in self.cache_sessao["incorporadora"]:
                incorporadora = self.cache_sessao["incorporadora"][chave_cache]
            else:
                dto = IncorporadoraInputDTO(
                    nome=nome_incorporadora,
                    cnpj=self.norm.limpar_cnpj(r.get("incorporadora_cnpj")),
                    reputacao=None, historico_obra=None
                )
                incorporadora = self.incorporadora_service.cadastrar(dto)
                self.cache_sessao["incorporadora"][chave_cache] = incorporadora

        # ----------------------------------------------------------
        # 5. EMPREENDIMENTO (Cadastra ou Reusa via Cache)
        # ----------------------------------------------------------
        empreendimento_nome = self.norm.texto(r.get("empreendimento"))
        chave_empreendimento = str(empreendimento_nome).strip().lower() if empreendimento_nome else "sem_nome_gerado"

        # Flag para controlar se precisamos criar a "Unidade Referência"
        criou_empreendimento_agora = False

        if chave_empreendimento in self.cache_sessao["empreendimento"]:
            empreendimento = self.cache_sessao["empreendimento"][chave_empreendimento]
        else:
            dto_emp = EmpreendimentoInputDTO(
                nome=empreendimento_nome,
                regiao=self.norm.texto(r.get("regiao")),
                bairro=self.norm.texto(r.get("bairro")),
                cidade=self.norm.texto(r.get("cidade")),
                estado=self.norm.texto(r.get("estado")),
                produto=self.norm.texto(r.get("produto")),
                endereco=self.norm.texto(r.get("endereco")),
                tipo=self.norm.texto(r.get("tipo")),
                descricao=self.norm.texto(r.get("descricao")),
                periodo_lancamento=self.norm.texto(r.get("periodo_lancamento")),
                data_entrega=self.norm.data(r.get("data_entrega")),
                status_entrega=self.norm.texto(r.get("status_entrega")),
                total_unidades=self.norm.inteiro(r.get("total_unidades")),
                amenities=self.norm.texto(r.get("amenities")),
                padrao_construtivo=self.norm.texto(r.get("padrao_construtivo")),
                incorporadora_id=incorporadora.id if incorporadora else None,
                proprietario_id=construtora.id if construtora else None,
                spe_id=None,
                unidade_referencia_id=None  
            )
            empreendimento = self.empreendimento_service.cadastrar(dto_emp)
            self.cache_sessao["empreendimento"][chave_empreendimento] = empreendimento
            criou_empreendimento_agora = True  # Marca que é um prédio novo nesta sessão!

        # ----------------------------------------------------------
        # 6. UNIDADE REFERÊNCIA (Criada APENAS 1x por Empreendimento)
        # Tratamento rigoroso de nulos para proteger o IA Engine
        # ----------------------------------------------------------
        unidade = None
        
        if criou_empreendimento_agora:
            # Pega os dados da planilha, mas se vierem nulos, aplica um Default Seguro (Fallback)
            codigo_ref = self.norm.texto(r.get("codigo_unidade")) or "REF-001"
            preco_ref = self.norm.moeda(r.get("preco")) or 0.0
            metragem_ref = self.norm.flutuante(r.get("metragem")) or 0.0
            tipo_ref = self.norm.texto(r.get("tipo_unidade")) or "Referência"
            dormitorios_ref = self.norm.inteiro(r.get("dormitorios")) or 1
            
            dto_uni = UnidadeInputDTO(
                empreendimento_id=empreendimento.id,
                codigo_unidade=codigo_ref,
                preco=preco_ref,
                metragem=metragem_ref,
                dormitorios=dormitorios_ref,
                suites=self.norm.inteiro(r.get("suites")) or 0,
                vagas=self.norm.inteiro(r.get("vagas")) or 0,
                tipo_unidade=tipo_ref,
                andar=self.norm.inteiro(r.get("andar")) or 0,
                disponibilidade="referência", # Marca clara de que não é uma unidade real à venda
                descricao_unidade="Unidade base/referência gerada pela Ingestão Central",
                observacoes=None
            )
            unidade = self.unidade_service.cadastrar(dto_uni)
            
            # Aqui no futuro você pode chamar um:
            # self.empreendimento_service.vincular_unidade_referencia(empreendimento.id, unidade.id)
            
            # ----------------------------------------------------------
            # 6.1 FINANCIAMENTO PADRÃO DA UNIDADE (ADR-005)
            # ----------------------------------------------------------
            # Verifica se já existe um financiamento para evitar exception de banco UNIQUE
            financiamento_existente = self.financiamento_service.buscar_por_unidade(unidade.id)
            
            if not financiamento_existente:
                dto_fin = TabelaFinanciamentoInputDTO(
                    unidade_id=unidade.id,
                    perfil_comprador="Outros",
                    condicao_uso="Outros",
                    renda_teto_familiar=None,
                    renda_minima_exigida=None,
                    valor_entrada=0.0,
                    valor_mensais=0.0,
                    qtde_mensais=0,
                    valor_intermediarias=0.0,
                    qtde_intermediarias=0,
                    valor_chaves=0.0,
                    valor_financiamento=0.0
                )
                self.financiamento_service.cadastrar(dto_fin)
            # ----------------------------------------------------------

        # ----------------------------------------------------------
        # 7. RELACIONAMENTOS N:N (Evita gerar binds duplicados entre eles)
        # ----------------------------------------------------------
        if construtora and imobiliaria:
            chave_ci = f"{construtora.id}_{imobiliaria.id}"
            if chave_ci not in self.cache_sessao["rel_ci"]:
                self.rel_construtora_imobiliaria.cadastrar(ConstrutoraImobiliariaInputDTO(
                    construtora_id=construtora.id,
                    imobiliaria_id=imobiliaria.id,
                    tipo_parceria=None, observacoes=None
                ))
                self.cache_sessao["rel_ci"].add(chave_ci)

        if corretor and imobiliaria:
            chave_cor_imo = f"{corretor.id}_{imobiliaria.id}"
            if chave_cor_imo not in self.cache_sessao["rel_cor_imo"]:
                self.rel_corretor_imobiliaria.cadastrar(CorretorImobiliariaInputDTO(
                    corretor_id=corretor.id,
                    imobiliaria_id=imobiliaria.id,
                    tipo_vinculo=None, observacoes=None
                ))
                self.cache_sessao["rel_cor_imo"].add(chave_cor_imo)

        return {
            "construtora":    construtora,
            "imobiliaria":    imobiliaria,
            "corretor":       corretor,
            "incorporadora":  incorporadora,
            "empreendimento": empreendimento,
            "unidade":        unidade,
        }