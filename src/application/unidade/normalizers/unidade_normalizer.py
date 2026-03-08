# ============================================================
# NORMALIZER: UnidadeNormalizer
# Camada: application/unidade/normalizers/
# Descrição: Transforma dados brutos (UnidadeInputDTO) em dados
#            limpos e validados (UnidadeNormalizedDTO).
#            Regras: sem acesso ao banco, sem regra de negócio,
#            apenas limpeza, tipagem e padronização de valores.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO
from src.domain.unidade.dto.unidade_normalized_dto import UnidadeNormalizedDTO


# Valores aceitos para disponibilidade — qualquer outro será normalizado para None
DISPONIBILIDADES_VALIDAS = {"disponível", "vendido", "reservado"}

# Tipologias aceitas — padroniza variações comuns do mercado
TIPOS_VALIDOS = {
    "studio", "1dorm", "2dorm", "3dorm", "4dorm",
    "garden", "cobertura", "casa", "loft", "flat"
}

# Mapeamento de variações comuns para o valor padronizado
# Ex: planilha pode vir com "apartamento 2 quartos" → "2dorm"
TIPO_ALIASES = {
    "1 dorm":       "1dorm",
    "1 dormitório": "1dorm",
    "2 dorm":       "2dorm",
    "2 dormitórios":"2dorm",
    "3 dorm":       "3dorm",
    "3 dormitórios":"3dorm",
    "4 dorm":       "4dorm",
    "4 dormitórios":"4dorm",
    "studios":      "studio",
    "coberturas":   "cobertura",
    "gardens":      "garden",
}


class UnidadeNormalizer:

    @staticmethod
    def normalize(dto: UnidadeInputDTO) -> UnidadeNormalizedDTO:
        """Normaliza um UnidadeInputDTO para UnidadeNormalizedDTO.
        Aplica limpeza de strings, conversão de tipos e padronização
        de valores categóricos (tipo_unidade, disponibilidade)."""
        return UnidadeNormalizedDTO(
            empreendimento_id=dto.empreendimento_id,

            # Código: strip + uppercase para padronização
            codigo_unidade=dto.codigo_unidade.strip().upper() if dto.codigo_unidade else None,

            # Valores numéricos: garantir tipos corretos, None se inválido
            preco=UnidadeNormalizer._normalizar_float(dto.preco),
            metragem=UnidadeNormalizer._normalizar_float(dto.metragem),
            dormitorios=UnidadeNormalizer._normalizar_int(dto.dormitorios),
            suites=UnidadeNormalizer._normalizar_int(dto.suites, default=0),
            vagas=UnidadeNormalizer._normalizar_int(dto.vagas, default=0),

            # Tipologia: lower + strip + alias mapping
            tipo_unidade=UnidadeNormalizer._normalizar_tipo(dto.tipo_unidade),

            # Andar: int, 0 = térreo
            andar=UnidadeNormalizer._normalizar_int(dto.andar, default=0),

            # Disponibilidade: lower + validação contra valores aceitos
            disponibilidade=UnidadeNormalizer._normalizar_disponibilidade(dto.disponibilidade),

            # Textos livres: apenas strip
            descricao_unidade=dto.descricao_unidade.strip() if dto.descricao_unidade else None,
            observacoes=dto.observacoes.strip() if dto.observacoes else None,
        )

    # ----------------------------------------------------------
    # HELPERS PRIVADOS DE NORMALIZAÇÃO
    # ----------------------------------------------------------

    @staticmethod
    def _normalizar_float(valor) -> float | None:
        """Converte para float. Retorna None se inválido ou ausente.
        Aceita int, float, string numérica."""
        if valor is None:
            return None
        try:
            return float(valor)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _normalizar_int(valor, default: int | None = None) -> int | None:
        """Converte para int. Retorna default se inválido ou ausente.
        Usado para dormitorios, suites, vagas e andar."""
        if valor is None:
            return default
        try:
            return int(valor)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def _normalizar_tipo(tipo: str | None) -> str | None:
        """Padroniza o tipo de unidade.
        Aplica lower + strip, verifica aliases e valida contra lista aceita.
        Retorna None se não reconhecido — não inventa valores."""
        if not tipo:
            return None
        tipo_limpo = tipo.strip().lower()
        # Verificar alias primeiro (ex: "2 dorm" → "2dorm")
        tipo_mapeado = TIPO_ALIASES.get(tipo_limpo, tipo_limpo)
        # Validar contra lista de tipos aceitos
        return tipo_mapeado if tipo_mapeado in TIPOS_VALIDOS else None

    @staticmethod
    def _normalizar_disponibilidade(disponibilidade: str | None) -> str:
        """Padroniza o status de disponibilidade.
        Retorna 'disponível' como padrão seguro se não informado ou inválido.
        Isso evita que unidades novas fiquem sem status e sejam ignoradas pelo pipeline."""
        if not disponibilidade:
            return "disponível"
        valor = disponibilidade.strip().lower()
        return valor if valor in DISPONIBILIDADES_VALIDAS else "disponível"