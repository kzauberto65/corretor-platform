import sqlite3
from src.domain.lead.entities.lead_entity import LeadEntity


class LeadRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # CADASTRAR
    # ---------------------------------------------------------
    def cadastrar(self, entity: LeadEntity) -> LeadEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO lead (
                nome, email, telefone, origem, tags,
                intencao, tipo_imovel, faixa_preco, preco_min, preco_max,
                quartos, vagas, metragem_min, metragem_max,
                bairro_interesse, cidade_interesse, urgencia, motivo,
                utm_source, utm_medium, utm_campaign, utm_term, utm_content,
                canal_preferido,
                profile_json, historico_json,
                score_lead
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?,
                ?, ?,
                ?
            )
        """, (
            entity.nome, entity.email, entity.telefone, entity.origem, entity.tags,
            entity.intencao, entity.tipo_imovel, entity.faixa_preco, entity.preco_min, entity.preco_max,
            entity.quartos, entity.vagas, entity.metragem_min, entity.metragem_max,
            entity.bairro_interesse, entity.cidade_interesse, entity.urgencia, entity.motivo,
            entity.utm_source, entity.utm_medium, entity.utm_campaign, entity.utm_term, entity.utm_content,
            entity.canal_preferido,
            str(entity.profile_json), str(entity.historico_json),
            entity.score_lead
        ))

        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    # ---------------------------------------------------------
    # ATUALIZAR
    # ---------------------------------------------------------
    def atualizar(self, entity: LeadEntity) -> LeadEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE lead SET
                nome=?, email=?, telefone=?, origem=?, tags=?,
                intencao=?, tipo_imovel=?, faixa_preco=?, preco_min=?, preco_max=?,
                quartos=?, vagas=?, metragem_min=?, metragem_max=?,
                bairro_interesse=?, cidade_interesse=?, urgencia=?, motivo=?,
                utm_source=?, utm_medium=?, utm_campaign=?, utm_term=?, utm_content=?,
                canal_preferido=?,
                profile_json=?, historico_json=?,
                score_lead=?,
                atualizado_em=datetime('now')
            WHERE id=?
        """, (
            entity.nome, entity.email, entity.telefone, entity.origem, entity.tags,
            entity.intencao, entity.tipo_imovel, entity.faixa_preco, entity.preco_min, entity.preco_max,
            entity.quartos, entity.vagas, entity.metragem_min, entity.metragem_max,
            entity.bairro_interesse, entity.cidade_interesse, entity.urgencia, entity.motivo,
            entity.utm_source, entity.utm_medium, entity.utm_campaign, entity.utm_term, entity.utm_content,
            entity.canal_preferido,
            str(entity.profile_json), str(entity.historico_json),
            entity.score_lead,
            entity.id
        ))

        conn.commit()
        conn.close()
        return entity

    # ---------------------------------------------------------
    # CONSULTAR
    # ---------------------------------------------------------
    def consultar(self) -> list[LeadEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM lead")
        rows = cur.fetchall()
        conn.close()

        entidades = []
        for row in rows:
            try:
                entidades.append(self._row_to_entity(row))
            except Exception as e:
                print(">>> ERRO NO MAPA:", e)
                print(">>> ROW PROBLEMÁTICA:", row)

        return entidades

    # ---------------------------------------------------------
    # BUSCAR POR ID
    # ---------------------------------------------------------
    def buscar_por_id(self, id: int) -> LeadEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM lead WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        return self._row_to_entity(row) if row else None

    # ---------------------------------------------------------
    # REMOVER
    # ---------------------------------------------------------
    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM lead WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True

    # ---------------------------------------------------------
    # CONVERSÃO row → Entity
    # ---------------------------------------------------------
    def _row_to_entity(self, row) -> LeadEntity:
        return LeadEntity(
            id=row[0],
            nome=row[1],
            email=row[2],
            telefone=row[3],
            origem=row[4],
            tags=row[5],
            intencao=row[6],
            tipo_imovel=row[7],
            faixa_preco=row[8],
            preco_min=row[9],
            preco_max=row[10],
            quartos=row[11],
            vagas=row[12],
            metragem_min=row[13],
            metragem_max=row[14],
            bairro_interesse=row[15],
            cidade_interesse=row[16],
            urgencia=row[17],
            motivo=row[18],
            utm_source=row[19],
            utm_medium=row[20],
            utm_campaign=row[21],
            utm_term=row[22],
            utm_content=row[23],
            canal_preferido=row[24],
            profile_json=row[25],
            historico_json=row[26],
            score_lead=row[27],
            criado_em=row[28],
            atualizado_em=row[29]
        )
