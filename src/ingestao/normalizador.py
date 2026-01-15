def normalizar(registro):

    def limpar_texto(v):
        return "" if v is None else str(v).strip()

    def limpar_float(v):
        try:
            return float(v)
        except:
            return 0.0

    return {
        "endereco": limpar_texto(registro.get("endereco")),
        "cidade": limpar_texto(registro.get("cidade")),
        "estado": limpar_texto(registro.get("estado")),
        "preco": limpar_float(registro.get("preco")),
        "proprietario_id": None
    }