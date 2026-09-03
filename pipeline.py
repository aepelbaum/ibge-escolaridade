import requests
import pandas as pd
import matplotlib.pyplot as plt


def buscar_dados_ibge(codigo_uf: str) -> dict:
    """Busca os dados brutos de escolaridade na API do IBGE, por estado."""
    url = (
        f"https://servicodados.ibge.gov.br/api/v3/agregados/10061"
        f"/periodos/2022/variaveis/2667"
        f"?localidades=N6[N3[{codigo_uf}]]"
        f"&classificacao=1568[all]"
    )
    resposta = requests.get(url)
    resposta.raise_for_status()  # se der erro HTTP, já para aqui
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
    return pd.DataFrame(linhas)


def filtrar_municipio(df: pd.DataFrame, nome_municipio: str) -> pd.DataFrame:
    """Filtra a tabela pra um único município, removendo a linha 'Total'."""
    df_filtrado = df[df["municipio"] == nome_municipio].copy()
    df_filtrado = df_filtrado[df_filtrado["nivel_instrucao"] != "Total"]
    df_filtrado["valor"] = pd.to_numeric(df_filtrado["valor"])
    return df_filtrado


def montar_grafico(df: pd.DataFrame, titulo: str, nome_arquivo: str) -> None:
    """Gera e salva um gráfico de barras a partir dos dados filtrados."""
    plt.figure(figsize=(10, 6))
    plt.bar(df["nivel_instrucao"], df["valor"], color="steelblue")
    plt.title(titulo)
    plt.xlabel("Nível de Instrução")
    plt.ylabel("Pessoas de 18 anos ou mais")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()


def main():
    codigo_uf_rj = "33"
    municipio_alvo = "Rio de Janeiro - RJ"

    dados_brutos = buscar_dados_ibge(codigo_uf_rj)
    df = organizar_dados(dados_brutos)
    df_rio = filtrar_municipio(df, municipio_alvo)

    print(df_rio)

    montar_grafico(
        df_rio,
        titulo="Grau de Escolaridade — Município do Rio de Janeiro (Censo 2022)",
        nome_arquivo="grafico_escolaridade_rio.png"
    )


if __name__ == "__main__":
    main()