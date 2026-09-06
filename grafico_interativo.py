import requests
import pandas as pd
import plotly.graph_objects as go


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


def montar_grafico_com_filtro(df: pd.DataFrame, nome_arquivo: str) -> None:
    """Gera um gráfico de barras com um menu suspenso pra filtrar por município."""
    municipios = sorted(df["municipio"].unique())
    municipio_inicial = "Rio de Janeiro - RJ"

    fig = go.Figure()

    # Cria uma "trace" (camada de dados) para cada município, todas escondidas por padrão
    for municipio in municipios:
        dados_municipio = df[df["municipio"] == municipio]
        fig.add_trace(go.Bar(
            x=dados_municipio["nivel_instrucao"],
            y=dados_municipio["valor"],
            name=municipio,
            visible=(municipio == municipio_inicial),
            marker_color="steelblue"
        ))

    # Monta os botões do menu suspenso: cada botão mostra só a trace do município escolhido
    botoes = []
    for i, municipio in enumerate(municipios):
        visibilidade = [False] * len(municipios)
        visibilidade[i] = True
        botoes.append(dict(
            label=municipio,
            method="update",
            args=[{"visible": visibilidade},
                  {"title": f"Grau de Escolaridade — {municipio} (Censo 2022)"}]
        ))

    fig.update_layout(
        title=f"Grau de Escolaridade — {municipio_inicial} (Censo 2022)",
        xaxis_title="Nível de Instrução",
        yaxis_title="Pessoas de 18 anos ou mais",
        updatemenus=[dict(
            buttons=botoes,
            direction="down",
            showactive=True,
            x=1.0,
            xanchor="right",
            y=1.15,
            yanchor="top"
        )]
    )

    fig.write_html(nome_arquivo, include_plotlyjs=True)
    print(f"Gráfico interativo salvo em: {nome_arquivo}")


def main():
    codigo_uf_rj = "33"
    dados_brutos = buscar_dados_ibge(codigo_uf_rj)
    df = organizar_dados(dados_brutos)
    montar_grafico_com_filtro(df, "grafico_interativo.html")


if __name__ == "__main__":
    main()