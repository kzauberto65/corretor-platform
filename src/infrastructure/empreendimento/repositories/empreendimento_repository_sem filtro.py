import sqlite3
from src.domain.empreendimento.dto.empreendimento_dto import EmpreendimentoDTO

class EmpreendimentoRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def save(self, dto: EmpreendimentoDTO) -> EmpreendimentoDTO:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO empreendimentos (
                regiao, bairro, cidade, estado, produto, endereco,
                data_entrega, status_entrega, tipo, descricao, preco,
                proprietario_id, incorporadora_id, unidade_referencia_id,
                spe_id, periodo_lancamento, nome, tipologia
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dto.regiao, dto.bairro, dto.cidade, dto.estado, dto.produto,
            dto.endereco, dto.data_entrega, dto.status_entrega, dto.tipo,
            dto.descricao, dto.preco, dto.proprietario_id,
            dto.incorporadora_id, dto.unidade_referencia_id, dto.spe_id,
            dto.periodo_lancamento, dto.nome, dto.tipologia
        ))
        dto.id = cur.lastrowid
        conn.commit()
        conn.close()
        return dto

    def update(self, dto: EmpreendimentoDTO) -> EmpreendimentoDTO:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE empreendimentos SET
                regiao = ?, bairro = ?, cidade = ?, estado = ?, produto = ?,
                endereco = ?, data_entrega = ?, status_entrega = ?, tipo = ?,
                descricao = ?, preco = ?, proprietario_id = ?, incorporadora_id = ?,
                unidade_referencia_id = ?, spe_id = ?, periodo_lancamento = ?,
                nome = ?, tipologia = ?
            WHERE id = ?
        """, (
            dto.regiao, dto.bairro, dto.cidade, dto.estado, dto.produto,
            dto.endereco, dto.data_entrega, dto.status_entrega, dto.tipo,
            dto.descricao, dto.preco, dto.proprietario_id,
            dto.incorporadora_id, dto.unidade_referencia_id, dto.spe_id,
            dto.periodo_lancamento, dto.nome, dto.tipologia,
            dto.id
        ))
        conn.commit()
        conn.close()
        return dto

    def find(self):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM empreendimentos")
        rows = cur.fetchall()
        conn.close()
        return [EmpreendimentoDTO(*r) for r in rows]

    def find_by_id(self, id: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM empreendimentos WHERE id = ?", (id,))
        r = cur.fetchone()
        conn.close()
        return EmpreendimentoDTO(*r) if r else None

    def delete(self, id: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM empreendimentos WHERE id = ?", (id,))
        conn.commit()
        conn.close()
