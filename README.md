# 📊 Pipeline de Dados de Escolaridade — IBGE

Pipeline automatizado que busca dados públicos do **Censo 2022 (IBGE)** sobre nível de instrução da população, gera um gráfico de barras e envia o resultado por e-mail — tudo rodando sozinho, periodicamente, sem intervenção manual.

## 🎯 Sobre o projeto

Este projeto consome a **API SIDRA do IBGE** para obter dados de escolaridade do município do Rio de Janeiro, processa essas informações e as transforma em uma visualização clara. Todo o processo — da busca dos dados ao envio do resultado — é automatizado via **GitHub Actions**.

## ⚙️ Funcionalidades

- 🔎 Busca dados atualizados diretamente da API pública do IBGE (Tabela 10061 — Censo 2022)
- 🧹 Processa e organiza os dados com `pandas`
- 📈 Gera um gráfico de barras com `matplotlib`
- 🤖 Roda automaticamente todo mês via GitHub Actions (ou sob demanda, manualmente)
- 📧 Envia o gráfico atualizado por e-mail, com anexo, para uma lista de destinatários
- 🔒 Credenciais e dados sensíveis protegidos via GitHub Secrets

## 🛠️ Tecnologias utilizadas

- **Python 3.14**
- [`pandas`](https://pandas.pydata.org/) — tratamento de dados
- [`matplotlib`](https://matplotlib.org/) — geração do gráfico
- [`requests`](https://requests.readthedocs.io/) — consumo da API
- **GitHub Actions** — orquestração e agendamento do pipeline
- [`action-send-mail`](https://github.com/dawidd6/action-send-mail) — envio de e-mail via SMTP

## 📁 Estrutura do projeto

```
ibge-escolaridade/
├── .github/
│   └── workflows/
│       └── atualizar_grafico.yml    # Configuração da automação (GitHub Actions)
├── pipeline.py                       # Script principal: busca, organiza e plota os dados
├── grafico_escolaridade_rio.png       # Gráfico gerado (atualizado automaticamente)
└── README.md
```

## 🚀 Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/aepelbaum/ibge-escolaridade.git
   cd ibge-escolaridade
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```

3. Instale as dependências:
   ```bash
   pip install pandas matplotlib requests
   ```

4. Execute o pipeline:
   ```bash
   python pipeline.py
   ```

O gráfico será salvo como `grafico_escolaridade_rio.png` na raiz do projeto.

## 🤖 Automação (GitHub Actions)

O workflow `.github/workflows/atualizar_grafico.yml` é responsável por:

1. Rodar o `pipeline.py` automaticamente todo dia 1 de cada mês
2. Salvar o gráfico atualizado de volta no repositório
3. Enviar o resultado por e-mail para os destinatários configurados

Também é possível disparar essa execução manualmente, a qualquer momento, pela aba **Actions** do repositório (botão *Run workflow*).

### Configuração necessária

Para o envio de e-mail funcionar, é preciso configurar os seguintes **Secrets** no repositório (`Settings → Secrets and variables → Actions`):

| Secret | Descrição |
|---|---|
| `EMAIL_USUARIO` | E-mail usado para autenticar o envio |
| `EMAIL_SENHA_APP` | Senha de aplicativo (não a senha normal da conta) |
| `EMAIL_REMETENTE` | Nome e e-mail exibidos como remetente |
| `EMAIL_DESTINO` | Lista de destinatários, separados por vírgula |

## 📊 Fonte dos dados

Os dados utilizados são públicos e provêm do **Censo Demográfico 2022**, disponibilizados pelo IBGE através da [API SIDRA](https://sidra.ibge.gov.br/), especificamente a Tabela 10061 — *Pessoas de 18 anos ou mais de idade, por nível de instrução*.

## 👤 Autor

Projeto desenvolvido por Alexandre Epelbaum como parte de um estudo prático de automação de pipelines de dados com Python e GitHub Actions.

---

*Este projeto tem fins educacionais e de portfólio.*
