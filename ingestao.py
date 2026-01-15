import sys
import os
from src.servicos.ingestao_planilha_service import IngestaoPlanilhaService


def processar_arquivo(caminho):
    svc = IngestaoPlanilhaService()
    print(f"Processando arquivo: {caminho}")
    resultado = svc.processar_planilha(caminho)
    print(f"Ingestão concluída. Linhas processadas: {len(resultado)}")


def processar_todos():
    pasta = "data/entrada"
    if not os.path.exists(pasta):
        print(f"Pasta não encontrada: {pasta}")
        return

    arquivos = [f for f in os.listdir(pasta) if f.endswith(".xlsx")]

    if not arquivos:
        print("Nenhum arquivo .xlsx encontrado em data/entrada")
        return

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        processar_arquivo(caminho)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Ex: python ingestao.py data/entrada/teste.xlsx
        processar_arquivo(sys.argv[1])
    else:
        # Ex: python ingestao.py
        processar_todos()