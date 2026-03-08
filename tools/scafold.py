import os
import sys

CURRENT_SPRINT = "10.5"

def to_pascal_case(s: str) -> str:
    return ''.join(part.capitalize() for part in s.split('_'))

def to_snake_case(s: str) -> str:
    return s.lower().replace(' ', '_')

def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

def create_file(path: str, content: str) -> None:
    ensure_dir(path)
    if os.path.exists(path):
        print(f"⚠️  Pulei (já existe): {path}")
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.strip() + "\n")
        print(f"✅ Gerado: {path}")

def generate_scaffold(resource_name: str) -> None:
    slug = resource_name.strip().lower()
    pascal = to_pascal_case(slug)
    base = "src"

    print(f"\n🚀 Gerando scaffold para o domínio: '{slug}' (Pascal: {pascal})...\n")

    # 1) Entity
    path_entity = f"{base}/domain/{slug}/entities/{slug}_entity.py"
    content_entity = f"""# ============================================================
# ENTITY: {pascal}Entity
# Camada: domain/{slug}/entities/
# Descrição: Representa um {slug} persistido.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class {pascal}Entity:
    id: Optional[int] = None
    # Campos de domínio (desenhe conforme o modelo)
    # nome: Optional[str] = None
"""
    create_file(path_entity, content_entity)

    # 2) InputDTO
    path_input = f"{base}/domain/{slug}/dto/{slug}_input_dto.py"
    content_input = f"""# ============================================================
# DTO: {pascal}InputDTO
# Camada: domain/{slug}/dto/
# Descrição: Dados de entrada para criação/atualização de {slug}.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class {pascal}InputDTO:
    # Campos de entrada (ex.: nome, cidade, estado, etc.)
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    regiao: Optional[str] = None
    bairro: Optional[str] = None
    endereco: Optional[str] = None
    produto: Optional[str] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    periodo_lancamento: Optional[str] = None
    data_entrega: Optional[str] = None
    status_entrega: Optional[str] = None
    total_unidades: Optional[int] = None
    amenities: Optional[str] = None
    padrao_construtivo: Optional[str] = None
    incorporadora_id: Optional[int] = None
    proprietario_id: Optional[int] = None
    spe_id: Optional[int] = None
    unidade_referencia_id: Optional[int] = None
"""
    create_file(path_input, content_input)

    # 3) DTO (leitura)
    path_dto = f"{base}/domain/{slug}/dto/{slug}_dto.py"
    content_dto = f"""# ============================================================
# DTO: {pascal}DTO
# Camada: domain/{slug}/dto/
# Descrição: Leitura/retorno de {slug}.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class {pascal}DTO:
    id: Optional[int] = None
    # Campos de leitura (ex.: nome, cidade, estado, etc.)
"""
    create_file(path_dto, content_dto)

    # 4) NormalizedDTO
    path_norm = f"{base}/domain/{slug}/dto/{slug}_normalized_dto.py"
    content_norm = f"""# ============================================================
# DTO: {pascal}NormalizedDTO
# Camada: domain/{slug}/dto/
# Descrição: DTO normalizado antes da persistência.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class {pascal}NormalizedDTO:
    # Campos normalizados (ex.: nome, cidade, estado, etc.)
    # nome: Optional[str] = None
"""
    create_file(path_norm, content_norm)

    # 5) FilterDTO
    path_filter = f"{base}/domain/{slug}/dto/{slug}_filter_dto.py"
    content_filter = f"""# ============================================================
# DTO: {pascal}FilterDTO
# Camada: domain/{slug}/dto/
# Descrição: Parâmetros opcionais para consulta.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from dataclasses import dataclass
from typing import Optional

@dataclass
class {pascal}FilterDTO:
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    regiao: Optional[str] = None
    bairro: Optional[str] = None
    tipo: Optional[str] = None
    produto: Optional[str] = None
    status_entrega: Optional[str] = None
    periodo_lancamento: Optional[str] = None
    incorporadora_id: Optional[int] = None
    ordenar_por: Optional[str] = None
    ordem: str = "asc"
"""
    create_file(path_filter, content_filter)

    # 6) Repository (infra)
    path_repo = f"{base}/infrastructure/{slug}/repositories/{slug}_repository.py"
    content_repo = f"""# ============================================================
# REPOSITORY: {pascal}Repository
# Camada: infrastructure/{slug}/repositories/
# Descrição: Acesso a dados (CRUD) para {slug}.
# Sprint: {CURRENT_SPRINT}
# ============================================================

import sqlite3
from typing import Optional, List
from src.domain.{slug}.entities.{slug}_entity import {pascal}Entity

class {pascal}Repository:
    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _row_to_entity(self, row: sqlite3.Row) -> {pascal}Entity:
        return {pascal}Entity(id=row["id"])  # mapa simplificado

    def save(self, entity: {pascal}Entity) -> {pascal}Entity:
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO {slug}s (id) VALUES (NULL)", ())
            entity.id = cur.lastrowid
        return entity

    def update(self, entity: {pascal}Entity) -> {pascal}Entity:
        # Implementar conforme campos se necessário
        return entity

    def delete(self, id: int) -> bool:
        with self._conn() as conn:
            conn.execute("DELETE FROM {slug}s WHERE id = ?", (id,))
        return True

    def find_by_id(self, id: int) -> Optional[{pascal}Entity]:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM {slug}s WHERE id = ?", (id,)).fetchone()
        return self._row_to_entity(row) if row else None

    def find(self) -> List[{pascal}Entity]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM {slug}s").fetchall()
        return [self._row_to_entity(r) for r in rows]
"""
    create_file(path_repo, content_repo)

    # 7) Normalizer
    path_normz = f"{base}/application/{slug}/normalizers/{slug}_normalizer.py"
    content_normz = f"""# ============================================================
# NORMALIZER: {pascal}Normalizer
# Camada: application/{slug}/normalizers/
# Descrição: Transforma InputDTO em NormalizedDTO.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from typing import Optional
import json
from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO
from src.domain.{slug}.dto.{slug}_normalized_dto import {pascal}NormalizedDTO


class {pascal}Normalizer:

    @staticmethod
    def normalize(input_dto: {pascal}InputDTO) -> {pascal}NormalizedDTO:
        # Implementar limpeza básica; retorno vazio como placeholder
        return {pascal}NormalizedDTO()
"""
    create_file(path_normz, content_normz)

    # 8) Service
    path_service = f"{base}/application/{slug}/services/{slug}_service.py"
    content_service = f"""# ============================================================
# SERVICE: {pascal}Service
# Camada: application/{slug}/services/
# Descrição: Orquestra operações de {slug}.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from typing import List
from src.domain.{slug}.entities.{slug}_entity import {pascal}Entity
from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO
from src.domain.{slug}.dto.{slug}_dto import {pascal}DTO
from src.application.{slug}.normalizers.{slug}_normalizer import {pascal}Normalizer

class {pascal}Service:
    def __init__(self, repo):
        self.repo = repo

    def _entity_to_dto(self, entity: {pascal}Entity) -> {pascal}DTO:
        return {pascal}DTO(id=entity.id)

    def cadastrar(self, input_dto: {pascal}InputDTO) -> {pascal}DTO:
        normalized = {pascal}Normalizer.normalize(input_dto)
        # Converter normalized → entity (implementar conforme modelo)
        entity = {pascal}Entity(id=None)
        saved = self.repo.save(entity)
        return self._entity_to_dto(saved)

    def listar_todos(self) -> List[{pascal}DTO]:
        return [self._entity_to_dto(e) for e in self.repo.find()]
"""
    create_file(path_service, content_service)

    # 9) Ingestor
    path_ingest = f"{base}/infrastructure/ingestao/{slug}_ingestor.py"
    content_ingest = f"""# ============================================================
# INGESTOR: Ingestao{pascal}
# Camada: infrastructure/ingestao/
# Descrição: Ingestão a partir de planilhas para {slug}.
# Sprint: {CURRENT_SPRINT}
# ============================================================

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.xls_parser import XLSParser
from src.application.{slug}.services.{slug}_service import {pascal}Service
from src.infrastructure.{slug}.repositories.{slug}_repository import {pascal}Repository
from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO

class Ingestao{pascal}(BaseIngestor):
    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.service = {pascal}Service({pascal}Repository(db_path))
        self.parser = XLSParser()

    def carregar(self, fonte: str) -> list:
        return self.parser.parse(fonte)

    def transformar(self, dados: list) -> list[{pascal}InputDTO]:
        dtos = []
        for row in dados:
            dto = {pascal}InputDTO(
                nome=row.get("nome"),
                cidade=row.get("cidade"),
                estado=row.get("estado"),
                regiao=row.get("regiao"),
                bairro=row.get("bairro"),
                endereco=row.get("endereco"),
                produto=row.get("produto"),
                tipo=row.get("tipo"),
                descricao=row.get("descricao"),
                periodo_lancamento=row.get("periodo_lancamento"),
                data_entrega=row.get("data_entrega"),
                status_entrega=row.get("status_entrega"),
                total_unidades=row.get("total_unidades"),
                amenities=row.get("amenities"),
                padrao_construtivo=row.get("padrao_construtivo"),
                incorporadora_id=row.get("incorporadora_id"),
                proprietario_id=row.get("proprietario_id"),
                spe_id=row.get("spe_id"),
                unidade_referencia_id=row.get("unidade_referencia_id")
            )
            dtos.append(dto)
        return dtos

    def salvar(self, dtos: list[{pascal}InputDTO]) -> list:
        return [self.service.cadastrar(dto) for dto in dtos]
"""
    create_file(path_ingest, content_ingest)

    # 10) CLI
    path_cli = f"{base}/interface/cli/{slug}_cli.py"
    content_cli = f"""# ============================================================
# CLI: {slug}_cli.py
# Camada: interface/cli/
# Descrição: Interface CLI para gerenciamento de {slug}.
# Sprint: {CURRENT_SPRINT}
# ============================================================

import click
from src.infrastructure.{slug}.repositories.{slug}_repository import {pascal}Repository
from src.application.{slug}.services.{slug}_service import {pascal}Service
from src.domain.{slug}.dto.{slug}_input_dto import {pascal}InputDTO

repo = {pascal}Repository()
service = {pascal}Service(repo)

@click.group()
def {slug}():
    \"\"\"Gerenciamento de {slug} via CLI.\"\"\"
    pass

@{slug}.command()
@click.option('--nome', required=True, type=str, help='Nome do {slug}')
def cadastrar(nome):
    dto = {pascal}InputDTO(nome=nome)
    criado = service.cadastrar(dto)
    click.echo(f\"Created {slug}: ID {criado.id}\")
"""
    create_file(path_cli, content_cli)

    # 11) BaseIngestor
    path_base_ing = f"{base}/infrastructure/ingestao/base_ingestor.py"
    content_base_ing = f"""# ============================================================
# BASE: BaseIngestor
# Camada: infrastructure/ingestao/
# Descrição: Contrato base para ingestores.
# Sprint: {CURRENT_SPRINT}
# ============================================================

class BaseIngestor:
    def carregar(self, fonte: str) -> list[dict]:
        raise NotImplementedError("carregar() must be implemented")

    def transformar(self, dados: list[dict]):
        raise NotImplementedError("transformar() must be implemented")

    def salvar(self, dtos) -> list:
        raise NotImplementedError("salvar() must be implemented")

    def executar(self, fonte: str) -> list:
        dados = self.carregar(fonte)
        return self.transformar(dados)
"""
    create_file(path_base_ing, content_base_ing)

    # 12) XLSParser (se não existir)
    path_xls = f"{base}/infrastructure/ingestao/xls_parser.py"
    content_xls = f"""# ============================================================
# PARSER: XLSParser
# Camada: infrastructure/ingestao/
# Descrição: Lê arquivos XLS/XLSX e retorna lista de dicts.
# Sprint: {CURRENT_SPRINT}
# ============================================================

import pandas as pd
from pathlib import Path

class XLSParser:
    def parse(self, caminho: str, aba: str = None) -> list[dict]:
        caminho = Path(caminho)
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        xls = pd.ExcelFile(caminho)
        if aba is None:
            aba = xls.sheet_names[0]
        df = pd.read_excel(
            xls,
            sheet_name=aba,
            dtype=str,
            keep_default_na=False
        )
        xls.close()

        df.columns = [
            col.strip()
               .replace(" ", "_")
               .replace("\\n", "")
               .replace("\\r", "")
               .lower()
            for col in df.columns
        ]
        registros = df.to_dict(orient="records")
        registros = [r for r in registros if any(str(v).strip() for v in r.values())]
        print(f"[XLSParser] {len(registros)} linha(s) lida(s) da aba '{aba}' em '{caminho.name}'")
        return registros
"""
    create_file(path_xls, content_xls)

    print(f"\n✨ Scaffold concluído para '{slug}' com 12 peças!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python tools/scaffold.py <nome_recurso>")
        print("Ex: python tools/scaffold.py unidade")
        sys.exit(1)

    recurso = sys.argv[1]
    generate_scaffold(recurso)