import datetime
import shutil
from pathlib import Path

from parsing import get_project_root
from persistencia.persistencia_adapter import PersistenciaAdapter
from ingestao.xls_parser import ler_xls
from ingestao.normalizador import normalizar


class ImportacaoService:

    def __init__(self):
        self.db = PersistenciaAdapter()
        self.root = get_project_root()

    def processar_arquivo(self, caminho):
        caminho = Path(caminho)
        nome_arquivo = caminho.name

        registros = ler_xls(caminho)

        id_importacao = self.db.registrar_importacao({
            "tipo": "xls",
            "arquivo": nome_arquivo,
            "origem": "manual",
            "total_registros": len(registros),
            "status": "processando",
            "data_execucao": datetime.datetime.now().isoformat()
        })

        sucesso = 0
        erros = 0
        log = []

        for r in registros:
            try:
                dados = normalizar(r)
                self.db.salvar_imovel(dados)
                sucesso += 1
            except Exception as e:
                erros += 1
                log.append(f"Erro no registro {r}: {e}")

        self.db.atualizar_importacao(
            id_importacao=id_importacao,
            sucesso=sucesso,
            erros=erros,
            log="\n".join(log)
        )

        destino = "data/processado" if erros == 0 else "data/erros"
        destino_final = self.root / destino / nome_arquivo

        destino_final.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(caminho), str(destino_final))

        print(f"Importação finalizada. Sucesso: {sucesso}, Erros: {erros}")