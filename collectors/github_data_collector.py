import requests
from utils.custom_exceptions import GitHubAPIError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from utils.utils import log_error
from datetime import datetime
import time

class GitHubDataCollector:
    def __init__(self, token):
        self.api_url = "https://api.github.com/graphql"
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def execute_query(self, query):
        try:
            # Suprimir avisos de certificado SSL inválido
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            # Fazer a requisição HTTP para a API do GitHub, ignorando a verificação do SSL
            response = requests.post(self.api_url, json={'query': query}, headers=self.headers, verify=False)

            if response.status_code == 200:
                result = response.json()
                if 'errors' in result:
                    log_error(f"GraphQL errors: {result['errors']}")
                    return
                return result
            else:
                log_error(f"Failed request with status code: {response.status_code} {response.text}")
                return
        except requests.exceptions.RequestException as e:
            log_error(f"RequestException: {e}")
            return

    def get_repositories(self, num_repos, batch_size=1, start_cursor=None, wait_time=2):
        all_repositories = []
        cursor = start_cursor  # Iniciar com o cursor armazenado, se fornecido

        while len(all_repositories) < num_repos:
            # Construção da string de consulta
            after_cursor = f', after: "{cursor}"' if cursor else ""

            query = f"""
            {{
            search(query: "stars:>1", type: REPOSITORY, first: {batch_size}{after_cursor}) {{
                nodes {{
                ... on Repository {{
                    name
                    owner {{
                        login
                    }}
                    createdAt
                    url
                    pullRequests(states: [MERGED, CLOSED]) {{
                        totalCount
                    }}
                    releases {{
                        totalCount
                    }}
                }}
                }}
                pageInfo {{
                    endCursor
                    hasNextPage
                }}
            }}
            }}
            """
            result = self.execute_query(query)
            
            # Retry se os dados não tiverem sido coletados
            if (result is None):
                continue

            # Filtrando os repositórios de acordo com a quantidade de PRs
            for repo in result['data']['search']['nodes']:
                if repo['pullRequests']['totalCount'] > 100:
                    all_repositories.append(repo)

            page_info = result['data']['search']['pageInfo']
            cursor = page_info['endCursor']  # Armazena o novo cursor

            if not page_info['hasNextPage']:
                break  # Se não houver mais páginas, sair do loop

            time.sleep(wait_time)  # Adiciona uma pausa de espera entre os batchs

        return all_repositories, cursor  # Retorna também o cursor para continuar depois


    def get_pull_requests(self, repo_name, repo_owner, pull_requests_limit=100, wait_time=2):
        all_pull_requests = []
        cursor = None  # Cursor inicial é None

        while len(all_pull_requests) < pull_requests_limit:
            after_cursor = f', after: "{cursor}"' if cursor else ""
            
            query = f"""
            {{
            repository(owner: "{repo_owner}", name: "{repo_name}") {{
                pullRequests(states: [MERGED, CLOSED], first: 10{after_cursor}) {{
                    nodes {{
                        createdAt
                        mergedAt
                        closedAt
                        reviews {{
                            totalCount
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
            }}
            }}
            """
            result = self.execute_query(query)

            pull_requests = result['data']['repository']['pullRequests']['nodes']
            for pr in pull_requests:
                # PRs com reviews e tempo > 1h
                review_count = pr['reviews']['totalCount']
                if review_count > 0:
                    created_at = pr['createdAt']
                    closed_at = ''
                    if pr['mergedAt']:
                        closed_at = pr['mergedAt']
                    else:
                        closed_at = pr['closedAt']
                    if closed_at:
                        created_at_dt = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                        merged_at_dt = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%SZ')
                        time_difference = merged_at_dt - created_at_dt

                        if time_difference.total_seconds() > 3600:
                            all_pull_requests.append(pr)

            page_info = result['data']['repository']['pullRequests']['pageInfo']
            cursor = page_info['endCursor']

            if not page_info['hasNextPage']:
                break
            
            time.sleep(wait_time)  # Adiciona uma pausa de espera entre as requisições de pull requests

        return all_pull_requests

