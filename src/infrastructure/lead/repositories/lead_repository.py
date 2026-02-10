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
            data_ingestao=row[5],
            status=row[6],
            tags=row[7],
            intencao=row[8],
            tipo_imovel=row[9],
            faixa_preco=row[10],
            preco_min=row[11],
            preco_max=row[12],
            quartos=row[13],
            vagas=row[14],
            metragem_min=row[15],
            metragem_max=row[16],
            bairro_interesse=row[17],
            regiao_interesse=row[18],
            cidade_interesse=row[19],
            urgencia=row[20],
            motivo=row[21],
            utm_source=row[22],
            utm_medium=row[23],
            utm_campaign=row[24],
            utm_term=row[25],
            utm_content=row[26],
            canal_preferido=row[27],
            profile_json=row[28],
            historico_json=row[29],
            score_lead=row[30],
            criado_em=row[31],
            atualizado_em=row[32]
        )

