class GitHubAPIError(Exception):
    """Exceção personalizada para erros da API do GitHub."""
    def __init__(self, status_code, message="Erro na requisição para a API do GitHub"):
        self.status_code = status_code
        self.message = f"{message}. Status Code: {status_code}"
        super().__init__(self.message)

class DataProcessingError(Exception):
    """Exceção personalizada para erros durante o processamento de dados."""
    def __init__(self, message="Erro durante o processamento dos dados"):
        self.message = message
        super().__init__(self.message)

class DataAnalysisError(Exception):
    """Exceção personalizada para erros durante a análise de dados."""
    def __init__(self, message="Erro durante a análise dos dados"):
        self.message = message
        super().__init__(self.message)
