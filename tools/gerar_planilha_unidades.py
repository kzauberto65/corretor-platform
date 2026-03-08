import random
import openpyxl

# Lista dos seus empreendimentos extraída da sua mensagem
empreendimentos = [
    {"id": 1, "nome": "Itaim Prime", "tipo": "apartamento"},
    {"id": 2, "nome": "Moema Studios", "tipo": "apartamento"},
    {"id": 3, "nome": "Vila Olímpia Corporate", "tipo": "apartamento"},
    {"id": 4, "nome": "Brooklin High Life", "tipo": "apartamento"},
    {"id": 5, "nome": "Pinheiros Smart", "tipo": "apartamento"},
    {"id": 6, "nome": "Faria Lima Residence", "tipo": "apartamento"},
    {"id": 7, "nome": "Paulista Modern", "tipo": "apartamento"},
    {"id": 8, "nome": "Jardins Loft", "tipo": "apartamento"},
    {"id": 9, "nome": "Vila Nova Prime", "tipo": "apartamento"},
    {"id": 10, "nome": "Campo Belo Urban", "tipo": "apartamento"},
    {"id": 11, "nome": "Tatuapé Family", "tipo": "apartamento"},
    {"id": 12, "nome": "Santana Park", "tipo": "apartamento"},
    {"id": 13, "nome": "Saúde Green", "tipo": "apartamento"},
    {"id": 14, "nome": "Morumbi Vista", "tipo": "apartamento"},
    {"id": 15, "nome": "Vila Prudente Home", "tipo": "apartamento"},
    {"id": 16, "nome": "Perdizes Alto", "tipo": "apartamento"},
    {"id": 17, "nome": "Butantã Family", "tipo": "apartamento"},
    {"id": 18, "nome": "São Miguel Confort", "tipo": "apartamento"},
    {"id": 19, "nome": "Jabaquara Easy", "tipo": "apartamento"},
    {"id": 20, "nome": "São Domingos Res", "tipo": "apartamento"}
]

# Configurações de geração por perfil
perfis = {
    "HIS": {"andar": 1, "metral_inicial": 38.0, "quartos": 1, "vagas": 0, "valor_base": 180000.0},
    "HMP": {"andar": 2, "metral_inicial": 45.0, "quartos": 2, "vagas": 1, "valor_base": 240000.0},
    "R2V": {"andar": 3, "metral_inicial": 55.0, "quartos": 2, "vagas": 1, "valor_base": 340000.0},
    "Outros": {"andar": 4, "metral_inicial": 75.0, "quartos": 3, "vagas": 2, "valor_base": 550000.0}
}

# Colunas que o seu banco espera + a nova coluna para gerar o financiamento no ingestor
colunas = [
    "empreendimento_id", "codigo_unidade", "preco", "metragem", 
    "dormitorios", "suites", "vagas", "tipo_unidade", 
    "andar", "disponibilidade", "descricao_unidade", "observacoes",
    "tipo_financiamento"  # <--- NOVA COLUNA AQUI
]

# Inicializa o arquivo Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Unidades"
ws.append(colunas)

for emp in empreendimentos:
    if emp["tipo"].lower() == "casa":
        # Se for casa, gera apenas 1 unidade com perfil "Outros"
        ws.append([
            emp["id"], "Casa 1", 850000.00, 120.0, 
            3, 1, 2, "casa", 
            0, "disponivel", "Casa linear com amplo quintal", "Inventário gerado",
            "Outros" # tipo_financiamento
        ])
    else:
        # Se for apartamento, gera 20 (5 de cada perfil)
        for perfil_nome, config in perfis.items():
            andar = config["andar"]
            for i in range(1, 6):
                numero = f"{andar}0{i}"
                codigo_unidade = f"T-A {numero}"
                
                metragem = config["metral_inicial"] + (i * 0.5)
                preco = config["valor_base"] + (i * 2000.0)
                
                # Regra simples de suítes
                suites = 1 if config["quartos"] > 1 else 0
                
                # Sorteio pro status de venda
                status = random.choices(["disponivel", "vendida", "reservada"], weights=[80, 10, 10])[0]

                # Criando uma descrição realista pro corretor ler
                if andar == 4:
                    descricao = "Cobertura com vista livre e varanda gourmet."
                else:
                    descricao = f"Unidade padrão {andar}º andar, ótima ventilação."

                # Adiciona a linha
                ws.append([
                    emp["id"], 
                    codigo_unidade, 
                    round(preco, 2), 
                    round(metragem, 2), 
                    config["quartos"], 
                    suites, 
                    config["vagas"], 
                    "apartamento", 
                    andar, 
                    status, 
                    descricao, # Coluna descricao_unidade (agora realista)
                    "Inventário gerado via script", # Coluna observacoes
                    perfil_nome # Coluna tipo_financiamento (HIS, HMP, R2V, Outros)
                ])

# Salvando a planilha em XLSX
nome_arquivo = "unidades_inventario.xlsx"
wb.save(nome_arquivo)

print(f"Sucesso! Planilha '{nome_arquivo}' gerada com a nova coluna 'tipo_financiamento'.")