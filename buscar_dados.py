import requests

# Código da Unidade da Federação do Rio de Janeiro no IBGE
codigo_uf_rj = "33"

# Tabela 10061: nível de instrução por município (Censo 2022)
# N6[N3[33]] = todos os municípios dentro do estado do RJ
url = (
    f"https://servicodados.ibge.gov.br/api/v3/agregados/10061"
    f"/periodos/2022/variaveis/2667"
    f"?localidades=N6[N3[{codigo_uf_rj}]]"
    f"&classificacao=1568[all]"
)

resposta = requests.get(url)
dados = resposta.json()

print(dados)