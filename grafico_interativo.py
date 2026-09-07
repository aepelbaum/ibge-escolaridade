import pandas as pd
import plotly.graph_objects as go
from dados_ibge import buscar_dados_ibge, organizar_dados


def montar_grafico_com_filtro(df: pd.DataFrame, nome_arquivo: str) -> None:
    """Gera um gráfico de barras com um menu suspenso pra filtrar por município."""
    municipios = sorted(df["municipio"].unique())
    municipio_inicial = "Rio de Janeiro - RJ"

    fig = go.Figure()

    for municipio in municipios:
        dados_municipio = df[df["municipio"] == municipio]
        fig.add_trace(go.Bar(
            x=dados_municipio["nivel_instrucao"],
            y=dados_municipio["valor"],
            name=municipio,
            visible=(municipio == municipio_inicial),
            marker_color="steelblue"
        ))

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