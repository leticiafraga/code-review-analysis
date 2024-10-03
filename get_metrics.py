import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GRAPHQL_ENDPOINT = 'https://api.github.com/graphql'
HEADERS = {
    'Authorization': f'Bearer {GITHUB_TOKEN}'
}

# Função para rodar a consulta GraphQL
def run_query(query):
    response = requests.post(GRAPHQL_ENDPOINT, json={'query': query}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

# Função para coletar métricas dos PRs de um repositório com paginação
def get_pr_metrics(repo_owner, repo_name):
    has_next_page = True
    end_cursor = None
    pr_data_list = []

    while has_next_page:
        # Construir a query com paginação
        query = f"""
        {{
          repository(owner: "{repo_owner}", name: "{repo_name}") {{
            pullRequests(states: [MERGED, CLOSED], first: 50, after: "{end_cursor}") {{
              pageInfo {{
                endCursor
                hasNextPage
              }}
              nodes {{
                createdAt
                closedAt
                mergedAt
                additions
                deletions
                changedFiles
                comments {{
                  totalCount
                }}
                participants {{
                  totalCount
                }}
                bodyText
                reviews {{
                  totalCount
                }}
              }}
            }}
          }}
        }}
        """ if end_cursor else f"""
        {{
          repository(owner: "{repo_owner}", name: "{repo_name}") {{
            pullRequests(states: [MERGED, CLOSED], first: 50) {{
              pageInfo {{
                endCursor
                hasNextPage
              }}
              nodes {{
                createdAt
                closedAt
                mergedAt
                additions
                deletions
                changedFiles
                comments {{
                  totalCount
                }}
                participants {{
                  totalCount
                }}
                bodyText
                reviews {{
                  totalCount
                }}
              }}
            }}
          }}
        }}
        """
        # Executar a consulta
        result = run_query(query)

        # Processar os dados dos PRs
        pr_data = result['data']['repository']['pullRequests']['nodes']
        pr_data_list.extend(pr_data)

        # Atualizar a paginação
        has_next_page = result['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
        end_cursor = result['data']['repository']['pullRequests']['pageInfo']['endCursor']

    # Processar as métricas dos PRs
    metrics = []
    for pr in pr_data_list:
        created_at = datetime.strptime(pr['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
        closed_or_merged_at = pr['closedAt'] or pr['mergedAt']
        closed_or_merged_at = datetime.strptime(closed_or_merged_at, '%Y-%m-%dT%H:%M:%SZ')
        
        # Calcular a duração da revisão em horas
        review_duration_hours = (closed_or_merged_at - created_at).total_seconds() / 3600
        
        # Filtrar PRs cujo tempo de revisão é menor que 1 hora
        if review_duration_hours > 1:
            metrics.append({
                'created_at': pr['createdAt'],
                'closed_or_merged_at': closed_or_merged_at,
                'reviews_count': pr['reviews']['totalCount'],
                'review_duration_hours': review_duration_hours,
                'additions': pr['additions'],
                'deletions': pr['deletions'],
                'changed_files': pr['changedFiles'],
                'comments_count': pr['comments']['totalCount'],
                'participants_count': pr['participants']['totalCount'],
                'description_length': len(pr['bodyText']) if pr['bodyText'] else 0
            })
    return metrics

# Função para processar o arquivo CSV e coletar as métricas de cada repositório
def process_repositories(input_csv, output_csv):
    # Ler o arquivo CSV de entrada
    df = pd.read_csv(input_csv)

    rows = []
    for index, row in df.iterrows():
        repo_url = row['url']
        repo_owner = repo_url.split('/')[-2]  # Extrair o owner da URL
        repo_name = repo_url.split('/')[-1]  # Extrair o nome do repositório

        print(f"Processando {repo_owner}/{repo_name}...")

        # Coletar as métricas de PRs
        try:
            pr_metrics = get_pr_metrics(repo_owner, repo_name)
            for pr in pr_metrics:
                rows.append({
                    'repo_name': repo_name,
                    'repo_owner': repo_owner,
                    'pr_created_at': pr['created_at'],
                    'pr_closed_or_merged_at': pr['closed_or_merged_at'],
                    'pr_reviews_count': pr['reviews_count'],
                    'pr_review_duration_hours': pr['review_duration_hours'],
                    'pr_additions': pr['additions'],
                    'pr_deletions': pr['deletions'],
                    'pr_changed_files': pr['changed_files'],
                    'pr_comments_count': pr['comments_count'],
                    'pr_participants_count': pr['participants_count'],
                    'pr_description_length': pr['description_length']
                })
        except Exception as e:
            print(f"Erro ao processar {repo_owner}/{repo_name}: {e}")

    # Salvar os dados em um novo arquivo CSV
    result_df = pd.DataFrame(rows)
    result_df.to_csv(output_csv, index=False)

# Script principal
if __name__ == "__main__":
    # Arquivo de entrada e saída
    input_csv = 'processed_data.csv'  # O arquivo com os repositórios
    output_csv = 'repositorios_com_metricas.csv'  # O arquivo onde serão salvas as métricas
    
    # Processar repositórios e salvar métricas
    process_repositories(input_csv, output_csv)
    
    print(f"Métricas salvas no arquivo '{output_csv}'")
