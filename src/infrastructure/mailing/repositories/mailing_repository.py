import sqlite3
from src.domain.mailing.entities.mailing_entity import MailingEntity


class MailingRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # CADASTRAR
    # ---------------------------------------------------------
    def cadastrar(self, entity: MailingEntity) -> MailingEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO mailing (
                nome, email, telefone, origem, tags,
                data_ingestao, fonte_arquivo,
                valido, motivo_invalidacao, hash_unico,
                sexo, data_nascimento, idade, estado_civil, nacionalidade,
                profissao, empresa, cargo, renda_mensal, faixa_renda, escolaridade,
                cep, logradouro, numero, complemento, bairro, cidade, estado, pais,
                intencao, tipo_imovel, faixa_preco, preco_min, preco_max,
                quartos, vagas, metragem_min, metragem_max,
                bairro_interesse, cidade_interesse, urgencia, motivo,
                utm_source, utm_medium, utm_campaign, utm_term, utm_content,
                primeiro_contato, ultimo_contato, canal_preferido, score_mailing
            )
            VALUES (
                ?, ?, ?, ?, ?,
                ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?
            )
        """, (
            entity.nome, entity.email, entity.telefone, entity.origem, entity.tags,
            entity.data_ingestao, entity.fonte_arquivo,
            entity.valido, entity.motivo_invalidacao, entity.hash_unico,
            entity.sexo, entity.data_nascimento, entity.idade, entity.estado_civil, entity.nacionalidade,
            entity.profissao, entity.empresa, entity.cargo, entity.renda_mensal, entity.faixa_renda, entity.escolaridade,
            entity.cep, entity.logradouro, entity.numero, entity.complemento, entity.bairro, entity.cidade, entity.estado, entity.pais,
            entity.intencao, entity.tipo_imovel, entity.faixa_preco, entity.preco_min, entity.preco_max,
            entity.quartos, entity.vagas, entity.metragem_min, entity.metragem_max,
            entity.bairro_interesse, entity.cidade_interesse, entity.urgencia, entity.motivo,
            entity.utm_source, entity.utm_medium, entity.utm_campaign, entity.utm_term, entity.utm_content,
            entity.primeiro_contato, entity.ultimo_contato, entity.canal_preferido, entity.score_mailing
        ))

        entity.id = cur.lastrowid
        conn.commit()
        conn.close()
        return entity

    # ---------------------------------------------------------
    # ATUALIZAR
    # ---------------------------------------------------------
    def atualizar(self, entity: MailingEntity) -> MailingEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE mailing SET
                nome=?, email=?, telefone=?, origem=?, tags=?,
                data_ingestao=?, fonte_arquivo=?,
                valido=?, motivo_invalidacao=?, hash_unico=?,
                sexo=?, data_nascimento=?, idade=?, estado_civil=?, nacionalidade=?,
                profissao=?, empresa=?, cargo=?, renda_mensal=?, faixa_renda=?, escolaridade=?,
                cep=?, logradouro=?, numero=?, complemento=?, bairro=?, cidade=?, estado=?, pais=?,
                intencao=?, tipo_imovel=?, faixa_preco=?, preco_min=?, preco_max=?,
                quartos=?, vagas=?, metragem_min=?, metragem_max=?,
                bairro_interesse=?, cidade_interesse=?, urgencia=?, motivo=?,
                utm_source=?, utm_medium=?, utm_campaign=?, utm_term=?, utm_content=?,
                primeiro_contato=?, ultimo_contato=?, canal_preferido=?, score_mailing=?,
                atualizado_em=datetime('now')
            WHERE id=?
        """, (
            entity.nome, entity.email, entity.telefone, entity.origem, entity.tags,
            entity.data_ingestao, entity.fonte_arquivo,
            entity.valido, entity.motivo_invalidacao, entity.hash_unico,
            entity.sexo, entity.data_nascimento, entity.idade, entity.estado_civil, entity.nacionalidade,
            entity.profissao, entity.empresa, entity.cargo, entity.renda_mensal, entity.faixa_renda, entity.escolaridade,
            entity.cep, entity.logradouro, entity.numero, entity.complemento, entity.bairro, entity.cidade, entity.estado, entity.pais,
            entity.intencao, entity.tipo_imovel, entity.faixa_preco, entity.preco_min, entity.preco_max,
            entity.quartos, entity.vagas, entity.metragem_min, entity.metragem_max,
            entity.bairro_interesse, entity.cidade_interesse, entity.urgencia, entity.motivo,
            entity.utm_source, entity.utm_medium, entity.utm_campaign, entity.utm_term, entity.utm_content,
            entity.primeiro_contato, entity.ultimo_contato, entity.canal_preferido, entity.score_mailing,
            entity.id
        ))

        conn.commit()
        conn.close()
        return entity

    # ---------------------------------------------------------
    # CONSULTAR
    # ---------------------------------------------------------
    def consultar(self) -> list[MailingEntity]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mailing")
        rows = cur.fetchall()
        conn.close()

        print(">>> ROWS:", len(rows)) 
        print(">>> FIRST ROW:", rows[0] if rows else None)

        entidades = [] 
        for row in rows: 
            try: 
                entidades.append(self._row_to_entity(row)) 
            except Exception as e: 
                print(">>> ERRO NO MAPA:", e) 
                print(">>> ROW PROBLEMÁTICA:", row) 
        
        return entidades

        return [self._row_to_entity(row) for row in rows]

    # ---------------------------------------------------------
    # BUSCAR POR ID
    # ---------------------------------------------------------
    def buscar_por_id(self, id: int) -> MailingEntity | None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mailing WHERE id = ?", (id,))
        row = cur.fetchone()
        conn.close()

        return self._row_to_entity(row) if row else None

    # ---------------------------------------------------------
    # REMOVER
    # ---------------------------------------------------------
    def remover(self, id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM mailing WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True

    # ---------------------------------------------------------
    # CONVERSÃO row → Entity
    # ---------------------------------------------------------
    def _row_to_entity(self, row) -> MailingEntity:
        return MailingEntity(
            id=row[0],
            nome=row[1],
            email=row[2],
            telefone=row[3],
            origem=row[4],
            tags=row[5],
            data_ingestao=row[6],
            fonte_arquivo=row[7],
            valido=row[8],
            motivo_invalidacao=row[9],
            hash_unico=row[10],
            sexo=row[11],
            data_nascimento=row[12],
            idade=row[13],
            estado_civil=row[14],
            nacionalidade=row[15],
            profissao=row[16],
            empresa=row[17],
            cargo=row[18],
            renda_mensal=row[19],
            faixa_renda=row[20],
            escolaridade=row[21],
            cep=row[22],
            logradouro=row[23],
            numero=row[24],
            complemento=row[25],
            bairro=row[26],
            cidade=row[27],
            estado=row[28],
            pais=row[29],
            intencao=row[30],
            tipo_imovel=row[31],
            faixa_preco=row[32],
            preco_min=row[33],
            preco_max=row[34],
            quartos=row[35],
            vagas=row[36],
            metragem_min=row[37],
            metragem_max=row[38],
            bairro_interesse=row[39],
            cidade_interesse=row[40],
            urgencia=row[41],
            motivo=row[42],
            utm_source=row[43],
            utm_medium=row[44],
            utm_campaign=row[45],
            utm_term=row[46],
            utm_content=row[47],
            primeiro_contato=row[48],
            ultimo_contato=row[49],
            canal_preferido=row[50],
            score_mailing=row[51],
            criado_em=row[52],
            atualizado_em=row[53]
        )
