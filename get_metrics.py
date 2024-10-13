import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import concurrent.futures
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API
GITHUB_TOKENS = [
    '',
    '',
    ''
]
GRAPHQL_ENDPOINT = 'https://api.github.com/graphql'

# Função para rodar a consulta GraphQL com tentativas de repetição
def run_query(query, token, retries=50, delay=3):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    for attempt in range(retries):
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query}, headers=headers, timeout=100)
        if response.status_code == 200:
            return response.json()
        elif attempt < retries - 1:
            print(f"Erro na consulta, tentando novamente em {delay} segundos... (Tentativa {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            print(f"Erro na consulta: {response.status_code} - {response.text}")
            return False

# Função para coletar métricas dos PRs de um repositório com paginação
def get_pr_metrics(repo_owner, repo_name):
    has_next_page = True
    end_cursor = None
    pr_data_list = []
    token_it = 0

    while has_next_page:
        # Construir a query com paginação
        query = f"""
        {{
          repository(owner: "{repo_owner}", name: "{repo_name}") {{
            pullRequests(states: [MERGED, CLOSED], first: 30, after: "{end_cursor}") {{
              pageInfo {{
                endCursor
                hasNextPage
              }}
              nodes {{
                state
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
            pullRequests(states: [MERGED, CLOSED], first: 30) {{
              pageInfo {{
                endCursor
                hasNextPage
              }}
              nodes {{
                state
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
        result = run_query(query, GITHUB_TOKENS[token_it % 3])

        if result == False:
            continue

        # Processar os dados dos PRs
        pr_data = result['data']['repository']['pullRequests']['nodes']
        pr_data_list.extend(pr_data)
        print(f"Coletados {len(pr_data_list)} PRs até agora")

        # Atualizar a paginação
        has_next_page = result['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
        end_cursor = result['data']['repository']['pullRequests']['pageInfo']['endCursor']

        token_it += 1

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
            pr_metrics = {
                'created_at': pr['createdAt'],
                'closed_or_merged_at': pr['closedAt'] or pr['mergedAt'],
                'state': pr['state'],
                'reviews_count': pr['reviews']['totalCount'],
                'review_duration_hours': review_duration_hours,
                'additions': pr['additions'],
                'deletions': pr['deletions'],
                'changed_files': pr['changedFiles'],
                'comments_count': pr['comments']['totalCount'],
                'participants_count': pr['participants']['totalCount'],
                'description_length': len(pr['bodyText']) if pr['bodyText'] else 0
            }
            metrics.append(pr_metrics)
    return metrics

# Função auxiliar para processar um repositório
def process_repository(repo_url):
    repo_owner = repo_url.split('/')[-2]  # Extrair o owner da URL
    repo_name = repo_url.split('/')[-1]  # Extrair o nome do repositório

    print(f"Processando {repo_owner}/{repo_name}...")

    # Coletar as métricas de PRs
    try:
        pr_metrics = get_pr_metrics(repo_owner, repo_name)
        rows = []
        for pr in pr_metrics:
            rows.append({
                'repo_name': repo_name,
                'repo_owner': repo_owner,
                'pr_created_at': pr['created_at'],
                'pr_closed_or_merged_at': pr['closed_or_merged_at'],
                'pr_state': pr['state'],
                'pr_reviews_count': pr['reviews_count'],
                'pr_review_duration_hours': pr['review_duration_hours'],
                'pr_additions': pr['additions'],
                'pr_deletions': pr['deletions'],
                'pr_changed_files': pr['changed_files'],
                'pr_comments_count': pr['comments_count'],
                'pr_participants_count': pr['participants_count'],
                'pr_description_length': pr['description_length']
            })
        return rows
    except Exception as e:
        print(f"Erro ao processar {repo_owner}/{repo_name}: {e}")
        return []

# Função para processar o arquivo CSV e coletar as métricas de cada repositório com multithreading
def process_repositories(input_csv, output_csv, error_csv):
    # Ler o arquivo CSV de entrada
    df = pd.read_csv(input_csv)

    all_rows = []
    error_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(process_repository, row['url']): row['url'] for _, row in df.iterrows()}

        for future in concurrent.futures.as_completed(futures):
            repo_url = futures[future]
            try:
                rows = future.result()
                if isinstance(rows, list):
                    all_rows.extend(rows)
                else:
                    error_rows.append(rows)
            except Exception as e:
                print(f"Erro ao processar {repo_url}: {e}")
                error_rows.append({'repo_url': repo_url, 'error': str(e)})

    # Salvar os dados em um novo arquivo CSV
    result_df = pd.DataFrame(all_rows)
    result_df.to_csv(output_csv, index=False)

    # Salvar os repositórios com erro em um arquivo CSV separado
    error_df = pd.DataFrame(error_rows)
    error_df.to_csv(error_csv, index=False)

# Script principal
if __name__ == "__main__":
    # Arquivo de entrada e saída
    input_csv = 'processed_data.csv'  # O arquivo com os repositórios
    output_csv = 'repositorios_com_metricas_2.csv'  # O arquivo onde serão salvas as métricas
    error_csv = 'repositorios_com_erro.csv'  # O arquivo onde serão salvos os repositórios com erro
    
    # Processar repositórios e salvar métricas
    process_repositories(input_csv, output_csv, error_csv)
    
    print(f"Métricas salvas no arquivo '{output_csv}'")
    print(f"Repositórios com erro salvos no arquivo '{error_csv}'")
