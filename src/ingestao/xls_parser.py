import pandas as pd
from pathlib import Path

def ler_xls(caminho):
    caminho = Path(caminho)
    try:
        df = pd.read_excel(caminho)
        return df.to_dict(orient="records")
    except Exception as e:
        raise Exception(f"Erro ao ler XLS: {e}")