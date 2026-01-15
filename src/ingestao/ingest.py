import sys
from pathlib import Path

from ingestao.importacao_service import ImportacaoService

def main():
    if len(sys.argv) < 2:
        print("Uso: python ingest.py caminho_do_arquivo.xlsx")
        return

    caminho = Path(sys.argv[1])

    if not caminho.exists():
        print(f"Arquivo não encontrado: {caminho}")
        return

    service = ImportacaoService()
    service.processar_arquivo(caminho)

if __name__ == "__main__":
    main()