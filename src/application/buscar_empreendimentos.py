class BuscarEmpreendimentos:
    def __init__(self, query_service):
        self.query_service = query_service

    def executar(
        self,
        filtros,
        pagina=1,
        por_pagina=10,
        ordenar_por=None,
        ordem="asc"
    ):
        dados = self.query_service.buscar_empreendimentos(
            cidade=filtros.get("cidade"),
            regiao=filtros.get("regiao"),
            tipologia=filtros.get("tipologia"),
            periodo_lancamento=filtros.get("lancamento"),
            status=filtros.get("status"),
            preco_min=filtros.get("preco_min"),
            preco_max=filtros.get("preco_max"),
            ordenar_por=ordenar_por,
            ordem=ordem,
            pagina=pagina,
            por_pagina=por_pagina
        )

        total = self.query_service.contar_empreendimentos(filtros)

        return {
            "dados": dados,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total": total,
            "total_paginas": max(1, (total + por_pagina - 1) // por_pagina)
        }
