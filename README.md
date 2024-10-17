# Laboratório 3
- Daniel Leão
- Juliana Serra
- Letícia Fraga

## Pré requisitos

1. Ter o Python instalado

## Tutorial

1. Criar um arquivo ".env" com um token do GitHub e um array de tokens no formato do arquivo .env.example [Fine-grained Personal Access Tokens (github.com)](https://github.com/settings/tokens?type=beta)
2. Instalar as dependências do projeto
    - `pip install dotenv requests`
    - `pip install pandas`
    - `pip install scipy`
    - `pip install matplotlib`
    - `pip install seaborn`
3. Executar `./get_top_200_repos/main.py` para coletar os repositórios
4. Executar `./get_metrics/get_metrics.py` para coletar os pull requests dos repositórios
5. Executar `./get_metrics/generate_correlation_report.py` para coletar as correlações
6. Executar `./plot/main_plot.py` para gerar os gráficos referentes às questões
