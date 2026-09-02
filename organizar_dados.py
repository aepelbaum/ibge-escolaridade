import requests
import pandas as pd

# Código da Unidade da Federação do Rio de Janeiro no IBGE
codigo_uf_rj = "33"

# Tabela 10061: nível de instrução por município (Censo 2022)
url = (
    f"https://servicodados.ibge.gov.br/api/v3/agregados/10061"
    f"/periodos/2022/variaveis/2667"
    f"?localidades=N6[N3[{codigo_uf_rj}]]"
    f"&classificacao=1568[all]"
)

resposta = requests.get(url)
dados = resposta.json()

# O JSON vem organizado por "categoria de escolaridade" (dados[0], dados[1]...)
# Dentro de cada categoria, tem uma lista de resultados por município
linhas = []

for categoria in dados:
    nome_categoria = categoria["variavel"]  # nome da variável (não usamos aqui, mas existe)
    for resultado in categoria["resultados"]:
        nivel_instrucao = resultado["classificacoes"][0]["categoria"]
        # "categoria" é um dicionário tipo {"codigo": "nome do nível de instrução"}
        nome_nivel = list(nivel_instrucao.values())[0]

        for serie in resultado["series"]:
            municipio = serie["localidade"]["nome"]
            valor = serie["serie"].get("2022")
            linhas.append({
                "municipio": municipio,
                "nivel_instrucao": nome_nivel,
                "valor": valor
            })

df = pd.DataFrame(linhas)
print(df.head(20))
print(f"\nTotal de linhas: {len(df)}")