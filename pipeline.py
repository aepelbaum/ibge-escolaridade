import pandas as pd
import matplotlib.pyplot as plt
from dados_ibge import buscar_dados_ibge, organizar_dados, filtrar_municipio


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