import requests
from utils.custom_exceptions import GitHubAPIError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from utils.utils import log_error
from datetime import datetime

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
                    raise GitHubAPIError(status_code=response.status_code, message="API returned errors")
                return result
            else:
                log_error(f"Failed request with status code: {response.status_code}")
                raise GitHubAPIError(status_code=response.status_code)
        except requests.exceptions.RequestException as e:
            log_error(f"RequestException: {e}")
            raise GitHubAPIError(status_code=response.status_code, message=str(e))

    def get_repositories(self, num_repos, batch_size=3):
        all_repositories = []
        cursor = None  # Cursor inicial é None

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
            
            # Filtrando os repositórios de acordo com a quantidade de PRs
            for repo in result['data']['search']['nodes']:
                if (repo['pullRequests']['totalCount'] > 100):
                    all_repositories.append(repo)

            page_info = result['data']['search']['pageInfo']
            cursor = page_info['endCursor']

            if not page_info['hasNextPage']:
                break  # Se não houver mais páginas, sair do loop

        return all_repositories

    def get_pull_requests(self, repo_name, repo_owner, pull_requests_limit=100):
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

        return all_pull_requests
