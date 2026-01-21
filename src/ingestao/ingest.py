# src/ingestao/ingest.py

import sys
from pathlib import Path
import shutil
from datetime import datetime

from src.ingestao.xls_parser import XLSParser
from src.ingestao.ingestao_central import IngestaoCentral


def main():

    pasta_entrada = Path("data/entrada")
    pasta_processado = Path("data/processado")
    pasta_erros = Path("data/erros")

    pasta_processado.mkdir(parents=True, exist_ok=True)
    pasta_erros.mkdir(parents=True, exist_ok=True)

    arquivos = list(pasta_entrada.glob("*.xls")) + list(pasta_entrada.glob("*.xlsx"))

    if not arquivos:
        print("Nenhum arquivo encontrado em /data/entrada")
        return

    parser = XLSParser()
    ingestor = IngestaoCentral()

    for arquivo in arquivos:
        print(f"\nProcessando arquivo: {arquivo.name}")

        try:
            registros = parser.ler(arquivo)
            resultado = ingestor.executar(registros)

            print(f"Sucesso: {resultado['sucesso']}")
            print(f"Erros: {len(resultado['erros'])}")

            # Gera timestamp para renomear o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            novo_nome = f"{arquivo.stem}_{timestamp}{arquivo.suffix}"

            # -------------------------------
            # EXIBIR DETALHES DOS ERROS
            # -------------------------------
            if resultado["erros"]:
                print("\n=== DETALHES DOS ERROS ===")
                for erro in resultado["erros"]:
                    print("\nLinha com erro:")
                    print(erro.get("linha"))
                    print("Motivo:")
                    print(" ", erro.get("erro"))

                destino = pasta_erros / novo_nome
                print("\nMovendo para /data/erros")

            else:
                destino = pasta_processado / novo_nome
                print("Movendo para /data/processado")

            shutil.move(str(arquivo), str(destino))

        except Exception as e:
            print(f"Erro crítico ao processar {arquivo.name}: {e}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            novo_nome = f"{arquivo.stem}_{timestamp}{arquivo.suffix}"

            destino = pasta_erros / novo_nome
            shutil.move(str(arquivo), str(destino))


if __name__ == "__main__":
    main()