import requests
import pandas as pd


def buscar_dados_ibge(codigo_uf: str) -> dict:
    """Busca os dados brutos de escolaridade na API do IBGE, por estado."""
    url = (
        f"https://servicodados.ibge.gov.br/api/v3/agregados/10061"
        f"/periodos/2022/variaveis/2667"
        f"?localidades=N6[N3[{codigo_uf}]]"
        f"&classificacao=1568[all]"
    )
    resposta = requests.get(url)
    resposta.raise_for_status()
    return resposta.json()


def organizar_dados(dados_brutos: dict) -> pd.DataFrame:
    """Transforma o JSON bruto do IBGE numa tabela (DataFrame) organizada."""
    linhas = []
    for categoria in dados_brutos:
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
    df = df[df["nivel_instrucao"] != "Total"]
    df["valor"] = pd.to_numeric(df["valor"])
    return df


def filtrar_municipio(df: pd.DataFrame, nome_municipio: str) -> pd.DataFrame:
    """Filtra a tabela pra um único município."""
    return df[df["municipio"] == nome_municipio].copy()