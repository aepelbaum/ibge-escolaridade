import requests
import pandas as pd
import matplotlib.pyplot as plt

codigo_uf_rj = "33"

url = (
    f"https://servicodados.ibge.gov.br/api/v3/agregados/10061"
    f"/periodos/2022/variaveis/2667"
    f"?localidades=N6[N3[{codigo_uf_rj}]]"
    f"&classificacao=1568[all]"
)

resposta = requests.get(url)
dados = resposta.json()

linhas = []
for categoria in dados:
    for resultado in categoria["resultados"]:
        nivel_instrucao = resultado["classificacoes"][0]["categoria"]
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

# Filtra só o município do Rio de Janeiro (capital)
df_rio = df[df["municipio"] == "Rio de Janeiro - RJ"]

# Remove a linha "Total" (queremos só as categorias de escolaridade)
df_rio = df_rio[df_rio["nivel_instrucao"] != "Total"]

# Converte a coluna "valor" pra número (ela vem como texto da API)
df_rio["valor"] = pd.to_numeric(df_rio["valor"])

print(df_rio)

# Monta o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(df_rio["nivel_instrucao"], df_rio["valor"], color="steelblue")
plt.title("Grau de Escolaridade — Município do Rio de Janeiro (Censo 2022)")
plt.xlabel("Nível de Instrução")
plt.ylabel("Pessoas de 18 anos ou mais")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("grafico_escolaridade_rio.png")
plt.show()