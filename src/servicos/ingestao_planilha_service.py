import pandas as pd

from src.servicos.construtora_service import ConstrutoraService
from src.servicos.imobiliaria_service import ImobiliariaService
from src.servicos.corretor_service import CorretorService
from src.servicos.imovel_service import ImovelService
from src.servicos.unidade_service import UnidadeService
from src.servicos.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.servicos.corretor_imobiliaria_service import CorretorImobiliariaService
from src.servicos.gerenciador_arquivos import GerenciadorArquivos
from src.servicos.logger_ingestao import LoggerIngestao
from src.servicos.unidade_referencia_service import UnidadeReferenciaService


class IngestaoPlanilhaService:
    def __init__(self):
        self.construtora_svc = ConstrutoraService()
        self.imobiliaria_svc = ImobiliariaService()
        self.corretor_svc = CorretorService()
        self.imovel_svc = ImovelService()
        self.unidade_svc = UnidadeService()
        self.rel_construtora_imobiliaria_svc = ConstrutoraImobiliariaService()
        self.rel_corretor_imobiliaria_svc = CorretorImobiliariaService()
        self.arquivos = GerenciadorArquivos()
        self.logger = LoggerIngestao()
        self.unidade_referencia_svc = UnidadeReferenciaService()

    def carregar_planilha(self, caminho):
        return pd.read_excel(caminho, engine="openpyxl")

    def extrair_referencia(self, codigo):
        if not isinstance(codigo, str):
            return None
        partes = codigo.split()
        return partes[0] if partes else None

    def processar_linha(self, linha):
        # 1. Criar construtora
        construtora = self.construtora_svc.criar_construtora(
            nome=linha["Construtora"],
            cnpj=None,
            contato=None
        )

        # 2. Criar imobiliária
        imobiliaria = self.imobiliaria_svc.criar_imobiliaria(
            nome=linha["Imobiliaria"],
            cnpj=None,
            contato=None
        )

        # 3. Criar corretor
        corretor = self.corretor_svc.criar_corretor(
            nome=linha["Corretor"],
            telefone=linha.get("Telefone"),
            email=linha.get("Email")
        )

        # 4. Criar imóvel
        imovel = self.imovel_svc.criar_imovel(
            regiao=linha["Regiao"],
            bairro=linha["Bairro"],
            cidade=linha["Cidade"],
            estado=linha["Estado"],
            produto=linha["Produto"],
            endereco=linha.get("Endereco"),
            data_entrega=str(linha.get("DataEntrega")) if linha.get("DataEntrega") else None,
            status_entrega=linha.get("StatusEntrega"),
            tipo=linha.get("Tipo"),
            descricao=linha.get("Descricao")
        )

        # 4.1 Extrair referência da unidade
        referencia = self.extrair_referencia(linha["CodigoUnidade"])
        referencia_id = None

        if referencia:
            referencia_id = self.unidade_referencia_svc.criar_ou_obter(referencia)

        # 5. Criar unidade
        unidade = self.unidade_svc.criar_unidade(
            imovel_id=imovel["id"],
            construtora_id=construtora["id"],
            codigo_unidade=linha["CodigoUnidade"],
            metragem=linha["Metragem"],
            valor=linha["Valor"],
            observacoes=linha.get("Observacoes"),
            unidade_referencia_id=referencia_id
        )

        # 6. Criar relacionamentos N:N
        self.rel_construtora_imobiliaria_svc.vincular(
            construtora_id=construtora["id"],
            imobiliaria_id=imobiliaria["id"]
        )

        self.rel_corretor_imobiliaria_svc.vincular(
            corretor_id=corretor["id"],
            imobiliaria_id=imobiliaria["id"]
        )

        return {
            "construtora": construtora,
            "imobiliaria": imobiliaria,
            "corretor": corretor,
            "imovel": imovel,
            "unidade": unidade
        }

    def processar_planilha(self, caminho):
        self.logger.registrar(f"Iniciando ingestão do arquivo: {caminho}")

        df = self.carregar_planilha(caminho)
        resultados = []

        total_linhas = len(df)
        erros = 0

        self.logger.registrar(f"Total de linhas na planilha: {total_linhas}")

        for index, linha in df.iterrows():
            try:
                resultado = self.processar_linha(linha)
                resultados.append(resultado)
                self.logger.registrar(f"Linha {index + 1} processada com sucesso")
            except Exception as e:
                erros += 1
                self.logger.registrar(f"Erro na linha {index + 1}: {str(e)}")

        if erros == 0:
            self.logger.registrar("Ingestão concluída com sucesso (nenhum erro)")
            self.arquivos.mover_para_processado(caminho)
        else:
            self.logger.registrar(f"Ingestão concluída com {erros} erro(s)")
            self.arquivos.mover_para_erros(caminho)

        return resultados