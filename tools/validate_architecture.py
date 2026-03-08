# ============================================================
# VALIDATOR: validate_architecture.py
# Camada: tools/
# Descrição: Valida se um domínio segue a arquitetura padrão
#            do projeto (12 peças mapeadas na Sprint 10.5).
#
# Uso:
#   python tools/validate_architecture.py construtora
#   python tools/validate_architecture.py --all
#
# Verifica:
#   1. Existência dos 12 arquivos obrigatórios
#   2. Classes esperadas dentro de cada arquivo
#   3. Imports cruzados (Service importa Normalizer, etc.)
#   4. Padrões de código (cabeçalho, Sprint, docstrings)
#   5. Antipatterns (acesso direto ao banco fora do repo, etc.)
#
# Sprint: 10.5
# ============================================================

import os
import sys
import re
from pathlib import Path

# --- CONSTANTE GLOBAL DA SPRINT ---
CURRENT_SPRINT = "10.5"
# ----------------------------------

# ----------------------------------------------------------
# CONFIGURAÇÃO: 12 peças obrigatórias
# ----------------------------------------------------------

def get_expected_files(slug: str, pascal: str) -> dict:
    """Retorna dict com path → validações esperadas para cada peça."""
    return {
        # ====== DOMAIN (5 peças) ======
        f"src/domain/{slug}/entities/{slug}_entity.py": {
            "label": "Entity",
            "classes": [f"{pascal}Entity"],
            "must_contain": ["@dataclass", "id:"],
            "must_not_contain": ["sqlite3", "import click"],
            "imports": [],
        },
        f"src/domain/{slug}/dto/{slug}_input_dto.py": {
            "label": "InputDTO",
            "classes": [f"{pascal}InputDTO"],
            "must_contain": ["@dataclass"],
            "must_not_contain": ["sqlite3"],
            "imports": [],
        },
        f"src/domain/{slug}/dto/{slug}_dto.py": {
            "label": "DTO (leitura)",
            "classes": [f"{pascal}DTO"],
            "must_contain": ["@dataclass", "id:"],
            "must_not_contain": ["sqlite3"],
            "imports": [],
        },
        f"src/domain/{slug}/dto/{slug}_normalized_dto.py": {
            "label": "NormalizedDTO",
            "classes": [f"{pascal}NormalizedDTO"],
            "must_contain": ["@dataclass"],
            "must_not_contain": ["sqlite3", "import click"],
            "imports": [],
        },
        f"src/domain/{slug}/dto/{slug}_filter_dto.py": {
            "label": "FilterDTO",
            "classes": [f"{pascal}FilterDTO"],
            "must_contain": ["@dataclass"],
            "must_not_contain": ["sqlite3"],
            "imports": [],
        },

        # ====== INFRASTRUCTURE (2 peças) ======
        f"src/infrastructure/{slug}/repositories/{slug}_repository.py": {
            "label": "Repository",
            "classes": [f"{pascal}Repository"],
            "must_contain": ["sqlite3", "_conn", "_row_to_entity", "PRAGMA foreign_keys"],
            "must_not_contain": ["import click", "EmpreendimentoNormalizer"], # Ajustar se houver outros normalizers
            "imports": [f"from src.domain.{slug}.entities.{slug}_entity import {pascal}Entity"], # Importa a própria entity do domínio
        },
        f"src/infrastructure/ingestao/{slug}_ingestor.py": {
            "label": "Ingestor",
            "classes": [f"Ingestao{pascal}"],
            "must_contain": ["BaseIngestor", "carregar", "transformar", "salvar"],
            "must_not_contain": [],
            "imports": [
                f"from src.infrastructure.ingestao.base_ingestor import BaseIngestor",
                f"from src.application.{slug}.services.{slug}_service import {pascal}Service",
            ],
        },

        # ====== APPLICATION (2 peças) ======
        f"src/application/{slug}/normalizers/{slug}_normalizer.py": {
            "label": "Normalizer",
            "classes": [f"{pascal}Normalizer"],
            "must_contain": ["normalize"],
            "must_not_contain": ["sqlite3", "import click", ".repo"],
            "imports": [
                f"from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO",
                f"from src.domain.{slug}.dto.{slug}_normalized_dto import {pascal}NormalizedDTO",
            ],
        },
        f"src/application/{slug}/services/{slug}_service.py": {
            "label": "Service",
            "classes": [f"{pascal}Service"],
            "must_contain": ["self.repo", "cadastrar", "_entity_to_dto"], # Adicionado _entity_to_dto como padrão
            "must_not_contain": ["sqlite3", "import click"],
            "imports": [
                f"from src.domain.{slug}.entities.{slug}_entity import {pascal}Entity",
                f"from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO",
                f"from src.domain.{slug}.dto.{slug}_dto import {pascal}DTO",
                f"from src.application.{slug}.normalizers.{slug}_normalizer import {pascal}Normalizer",
            ],
        },

        # ====== INTERFACE (1 peça) ======
        f"src/interface/cli/{slug}_cli.py": {
            "label": "CLI",
            "classes": [], # Pode não ter uma classe principal declarada no topo
            "must_contain": ["import click", "@click.group", "cadastrar"],
            "must_not_contain": ["sqlite3"],
            "imports": [
                f"from src.infrastructure.{slug}.repositories.{slug}_repository import {pascal}Repository",
                f"from src.application.{slug}.services.{slug}_service import {pascal}Service",
                f"from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO",
            ],
        },
    }


# ----------------------------------------------------------
# VALIDADORES
# ----------------------------------------------------------

def check_file_exists(path: str) -> tuple[bool, str]:
    if os.path.exists(path):
        return True, f"✅ Arquivo existe"
    return False, f"❌ Arquivo NÃO encontrado"


def check_classes(content: str, expected_classes: list[str]) -> list[str]:
    errors = []
    for cls in expected_classes:
        pattern = rf"class\s+{cls}[\s(:]"
        if not re.search(pattern, content):
            errors.append(f"❌ Classe '{cls}' não encontrada")
    return errors


def check_must_contain(content: str, patterns: list[str]) -> list[str]:
    errors = []
    for pattern in patterns:
        if pattern not in content:
            errors.append(f"❌ Padrão obrigatório ausente: '{pattern}'")
    return errors


def check_must_not_contain(content: str, patterns: list[str], label: str) -> list[str]:
    warnings = []
    for pattern in patterns:
        if pattern in content:
            warnings.append(f"⚠️  Antipattern em {label}: '{pattern}' não deveria estar aqui")
    return warnings


def check_imports(content: str, expected_imports: list[str]) -> list[str]:
    errors = []
    for imp in expected_imports:
        if imp not in content:
            errors.append(f"❌ Import ausente: '{imp}'")
    return errors


def check_header(content: str, sprint: str = CURRENT_SPRINT) -> list[str]:
    warnings = []
    if "# ====" not in content:
        warnings.append("⚠️  Cabeçalho padrão (# ====) ausente")
    # Ajuste para verificar se a sprint está presente de qualquer forma
    if f"Sprint: {sprint}" not in content and f"Sprint {sprint}" not in content:
        warnings.append(f"⚠️  Referência à Sprint {sprint} ausente no cabeçalho")
    return warnings

# Função to_pascal_case movida para cá para evitar NameError em check_rules
def to_pascal_case_func(slug: str) -> str:
    return ''.join(part.capitalize() for part in slug.split('_'))

# ----------------------------------------------------------
# VALIDAÇÃO DE SHARED (BaseIngestor + XLSParser)
# ----------------------------------------------------------

def validate_shared() -> tuple[int, int, list[str]]:
    """Valida os 2 arquivos compartilhados que não são por domínio."""
    errors = 0
    warnings = 0
    messages = []

    shared_files = {
        "src/infrastructure/ingestao/base_ingestor.py": {
            "label": "BaseIngestor",
            "classes": ["BaseIngestor"],
            "must_contain": ["carregar", "transformar", "salvar", "executar", "NotImplementedError"],
        },
        "src/infrastructure/ingestao/xls_parser.py": {
            "label": "XLSParser",
            "classes": ["XLSParser"],
            "must_contain": ["parse", "pandas", "to_dict"],
        },
    }

    for path, rules in shared_files.items():
        exists, msg = check_file_exists(path)
        if not exists:
            errors += 1
            messages.append(f"  {rules['label']}: {msg}")
            continue

        content = Path(path).read_text(encoding="utf-8")

        for err in check_classes(content, rules["classes"]):
            errors += 1
            messages.append(f"  {rules['label']}: {err}")

        for err in check_must_contain(content, rules["must_contain"]):
            errors += 1
            messages.append(f"  {rules['label']}: {err}")

    return errors, warnings, messages

# ----------------------------------------------------------
# VALIDAÇÃO PRINCIPAL POR DOMÍNIO
# ----------------------------------------------------------

def validate_domain(slug: str) -> tuple[int, int]:
    pascal = to_pascal_case_func(slug) # Usa a função local
    expected = get_expected_files(slug, pascal)

    total_errors = 0
    total_warnings = 0

    print(f"\n{'='*60}")
    print(f"  VALIDAÇÃO: {pascal} ({slug})")
    print(f"  Sprint: {CURRENT_SPRINT}")
    print(f"{'='*60}")

    # Valida as 10 peças do domínio
    for path, rules in expected.items():
        label = rules["label"]
        print(f"\n  📄 {label} — {path}")

        exists, msg = check_file_exists(path)
        print(f"     {msg}")

        if not exists:
            total_errors += 1
            continue

        content = Path(path).read_text(encoding="utf-8")

        # Classes
        for err in check_classes(content, rules["classes"]):
            print(f"     {err}")
            total_errors += 1

        # Must contain
        for err in check_must_contain(content, rules["must_contain"]):
            print(f"     {err}")
            total_errors += 1

        # Must NOT contain (antipatterns)
        for warn in check_must_not_contain(content, rules["must_not_contain"], label):
            print(f"     {warn}")
            total_warnings += 1

        # Imports cruzados
        for err in check_imports(content, rules["imports"]):
            print(f"     {err}")
            total_errors += 1

        # Cabeçalho
        for warn in check_header(content, CURRENT_SPRINT): # Passa CURRENT_SPRINT explicitamente
            print(f"     {warn}")
            total_warnings += 1

        # Se passou tudo
        if not any([
            check_classes(content, rules["classes"]),
            check_must_contain(content, rules["must_contain"]),
            check_must_not_contain(content, rules["must_not_contain"], label),
            check_imports(content, rules["imports"]),
            check_header(content, CURRENT_SPRINT), # Passa CURRENT_SPRINT explicitamente
        ]):
            print(f"     ✅ Tudo OK")

    # Valida shared (BaseIngestor + XLSParser)
    print(f"\n  📦 Componentes compartilhados:")
    sh_errors, sh_warnings, sh_messages = validate_shared()
    total_errors += sh_errors
    total_warnings += sh_warnings
    for msg in sh_messages:
        print(f"  {msg}")
    if not sh_messages:
        print(f"     ✅ BaseIngestor + XLSParser OK")

    # Resumo
    print(f"\n{'='*60}")
    print(f"  RESUMO: {pascal}")
    print(f"  Erros    : {total_errors}")
    print(f"  Avisos   : {total_warnings}")
    if total_errors == 0 and total_warnings == 0:
        print(f"  Status   : ✅ ARQUITETURA 100% CONFORME")
    elif total_errors == 0:
        print(f"  Status   : ⚠️  CONFORME com avisos")
    else:
        print(f"  Status   : ❌ NÃO CONFORME — corrigir erros")
    print(f"{'='*60}\n")

    return total_errors, total_warnings


# ----------------------------------------------------------
# MODO --all: descobre todos os domínios automaticamente
# ----------------------------------------------------------

def discover_domains() -> list[str]:
    """Descobre domínios existentes em src/domain/"""
    domain_path = "src/domain"
    if not os.path.exists(domain_path):
        return []
    return [
        d for d in os.listdir(domain_path)
        if os.path.isdir(os.path.join(domain_path, d))
        and not d.startswith("_")
        and not d.startswith(".")
    ]

# Função to_pascal_case movida para cá
def to_pascal_case(s: str) -> str:
    return ''.join(part.capitalize() for part in s.split('_'))

# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python tools/validate_architecture.py construtora")
        print("  python tools/validate_architecture.py --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        domains = discover_domains()
        if not domains:
            print("Nenhum domínio encontrado em src/domain/")
            sys.exit(1)

        print(f"\n🔍 Validando {len(domains)} domínio(s): {', '.join(domains)}")
        grand_errors = 0
        grand_warnings = 0
        for d in sorted(domains):
            e, w = validate_domain(d)
            grand_errors += e
            grand_warnings += w

        print(f"\n{'#'*60}")
        print(f"  VALIDAÇÃO GERAL")
        print(f"  Domínios   : {len(domains)}")
        print(f"  Erros      : {grand_errors}")
        print(f"  Avisos     : {grand_warnings}")
        if grand_errors == 0:
            print(f"  Status     : ✅ TODOS CONFORMES")
        else:
            print(f"  Status     : ❌ CORREÇÕES NECESSÁRIAS")
        print(f"{'#'*60}\n")

    else:
        slug = sys.argv[1].lower().strip()
        validate_domain(slug)