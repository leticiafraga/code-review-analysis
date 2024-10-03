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

    def get_repositories(self, num_repos, batch_size=5):
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
                    createdAt
                    pullRequests(states: [MERGED, CLOSED], first: 5) {{
                        totalCount
                        nodes {{
                            createdAt
                            mergedAt
                            closedAt
                            reviews {{
                                totalCount
                            }}
                    }}
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

            # Filtrando os repositórios de acordo com os PRs
            for repo in result['data']['search']['nodes']:
                pull_requests = repo['pullRequests']['nodes']
                print(pull_requests)
                valid_pull_requests = []

                if len(pull_requests) < 100:
                    continue

                for pr in pull_requests:
                    review_count = pr['reviews']['totalCount']

                    # PR com review e tempo de review > 1h
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
                                valid_pull_requests.append(pr)

                if len(valid_pull_requests) > 0:
                    all_repositories.append(repo)

            page_info = result['data']['search']['pageInfo']
            cursor = page_info['endCursor']

            if not page_info['hasNextPage']:
                break  # Se não houver mais páginas, sair do loop

        return all_repositories
