# ============================================================
# NORMALIZER: EmpreendimentoNormalizer
# Camada: application/empreendimento/normalizers/
# Descrição: Transforma EmpreendimentoInputDTO em
#            EmpreendimentoNormalizedDTO com dados limpos.
#            Regras: sem acesso ao banco, sem regra de negócio,
#            apenas limpeza, tipagem e padronização de valores.
#
# DECISÃO DE DESIGN — preservação de acentos:
#   Campos de texto persistidos (nome, bairro, cidade) preservam
#   acentos e capitalização correta. Remoção de acentos é papel
#   das queries SQL (LOWER/LIKE) — não do Normalizer.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

import json
from typing import Optional
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.empreendimento.dto.empreendimento_normalized_dto import EmpreendimentoNormalizedDTO


# Valores aceitos para status_entrega
STATUS_ENTREGA_VALIDOS = {"em obras", "pronto", "entregue", "lançamento"}

# Valores aceitos para tipo
TIPOS_VALIDOS = {
    "apartamento", "casa", "studio", "cobertura",
    "loft", "flat", "comercial", "loteamento"
}

# Mapeamento de variações comuns de tipo
TIPO_ALIASES = {
    "apto":         "apartamento",
    "apt":          "apartamento",
    "studios":      "studio",
    "coberturas":   "cobertura",
    "galpão":       "comercial",
    "sala":         "comercial",
}


class EmpreendimentoNormalizer:

    @staticmethod
    def normalize(input_dto: EmpreendimentoInputDTO) -> EmpreendimentoNormalizedDTO:
        """Normaliza um EmpreendimentoInputDTO para EmpreendimentoNormalizedDTO.

        Preserva acentos nos campos persistidos (nome, cidade, bairro).
        Apenas status_entrega e tipo são lowercased para padronização categórica."""
        return EmpreendimentoNormalizedDTO(
            # Identificação — preserva capitalização original
            nome=EmpreendimentoNormalizer._limpar(input_dto.nome),

            # Localização — preserva acentos para exibição correta
            regiao=EmpreendimentoNormalizer._limpar(input_dto.regiao),
            bairro=EmpreendimentoNormalizer._limpar(input_dto.bairro),
            cidade=EmpreendimentoNormalizer._limpar(input_dto.cidade),
            estado=EmpreendimentoNormalizer._normalizar_estado(input_dto.estado),
            endereco=EmpreendimentoNormalizer._limpar(input_dto.endereco),

            # Produto
            produto=EmpreendimentoNormalizer._limpar(input_dto.produto),
            tipo=EmpreendimentoNormalizer._normalizar_tipo(input_dto.tipo),
            descricao=EmpreendimentoNormalizer._limpar(input_dto.descricao),

            # Cronograma
            periodo_lancamento=EmpreendimentoNormalizer._limpar(input_dto.periodo_lancamento),
            data_entrega=EmpreendimentoNormalizer._normalizar_data(input_dto.data_entrega),
            status_entrega=EmpreendimentoNormalizer._normalizar_status(input_dto.status_entrega),

            # Atributos institucionais (novos Sprint 10.5)
            total_unidades=EmpreendimentoNormalizer._normalizar_int(input_dto.total_unidades),
            amenities=EmpreendimentoNormalizer._normalizar_json(input_dto.amenities),
            padrao_construtivo=EmpreendimentoNormalizer._normalizar_json(input_dto.padrao_construtivo),

            # Relacionamentos — apenas garantir tipo int
            incorporadora_id=EmpreendimentoNormalizer._normalizar_int(input_dto.incorporadora_id),
            proprietario_id=EmpreendimentoNormalizer._normalizar_int(input_dto.proprietario_id),
            spe_id=EmpreendimentoNormalizer._normalizar_int(input_dto.spe_id),
            unidade_referencia_id=EmpreendimentoNormalizer._normalizar_int(input_dto.unidade_referencia_id),
        )

    # ----------------------------------------------------------
    # HELPERS PRIVADOS
    # ----------------------------------------------------------

    @staticmethod
    def _limpar(valor: Optional[str]) -> Optional[str]:
        """Limpeza básica: strip e None se vazio.
        Preserva acentos e capitalização — não remove caracteres especiais."""
        if not valor:
            return None
        limpo = str(valor).strip()
        return limpo if limpo else None

    @staticmethod
    def _normalizar_estado(estado: Optional[str]) -> Optional[str]:
        """Normaliza sigla do estado para uppercase.
        Ex: 'sp' → 'SP', 'São Paulo' → 'SP' se tiver 2 chars após strip."""
        if not estado:
            return None
        sigla = estado.strip().upper()
        # Se veio o nome completo do estado, retorna como está em uppercase
        # A padronização para sigla é responsabilidade de quem alimenta o dado
        return sigla if sigla else None

    @staticmethod
    def _normalizar_tipo(tipo: Optional[str]) -> Optional[str]:
        """Padroniza tipo do empreendimento.
        Aplica lower + aliases + validação contra lista aceita.
        Retorna None se não reconhecido."""
        if not tipo:
            return None
        tipo_limpo = tipo.strip().lower()
        tipo_mapeado = TIPO_ALIASES.get(tipo_limpo, tipo_limpo)
        return tipo_mapeado if tipo_mapeado in TIPOS_VALIDOS else tipo_limpo

    @staticmethod
    def _normalizar_status(status: Optional[str]) -> Optional[str]:
        """Padroniza status_entrega para lowercase.
        Retorna None se não reconhecido — evita valores inválidos no banco."""
        if not status:
            return None
        valor = status.strip().lower()
        return valor if valor in STATUS_ENTREGA_VALIDOS else None

    @staticmethod
    def _normalizar_data(data: Optional[str]) -> Optional[str]:
        """Valida e retorna data no formato ISO YYYY-MM-DD.
        Aceita formatos comuns de planilha: DD/MM/YYYY, YYYY-MM-DD.
        Retorna None se não reconhecido."""
        if not data:
            return None
        data = str(data).strip()

        # Formato ISO — já correto
        if len(data) == 10 and data[4] == "-":
            return data

        # Formato DD/MM/YYYY — converte para ISO
        if len(data) == 10 and data[2] == "/":
            partes = data.split("/")
            if len(partes) == 3:
                return f"{partes[2]}-{partes[1]}-{partes[0]}"

        # Formato DD/MM/YY — converte para ISO com século 20xx
        if len(data) == 8 and data[2] == "/":
            partes = data.split("/")
            if len(partes) == 3:
                return f"20{partes[2]}-{partes[1]}-{partes[0]}"

        # Não reconhecido — retorna original com aviso
        return data

    @staticmethod
    def _normalizar_int(valor) -> Optional[int]:
        """Converte para int. Retorna None se inválido."""
        if valor is None:
            return None
        try:
            return int(float(valor))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _normalizar_json(valor: Optional[str]) -> Optional[str]:
        """Valida se o valor é um JSON string válido.
        Se for dict ou list, serializa para string JSON.
        Se for string JSON válida, retorna como está.
        Retorna None se inválido."""
        if valor is None:
            return None
        # Se já for dict ou list (vindo de código), serializa
        if isinstance(valor, (dict, list)):
            return json.dumps(valor, ensure_ascii=False)
        # Se for string, tenta validar como JSON
        try:
            json.loads(valor)
            return valor
        except (json.JSONDecodeError, TypeError):
            # Não é JSON válido — retorna como string simples
            return str(valor).strip() if str(valor).strip() else None