from collectors.github_data_collector import GitHubDataCollector
from processors.data_processor import DataProcessor
from utils.utils import setup_logging, log_error
from utils.custom_exceptions import GitHubAPIError, DataProcessingError, DataAnalysisError
from dotenv import load_dotenv
import os

# Funções de carregar e salvar cursor
def save_cursor(cursor, file_path='cursor.txt'):
    try:
        with open(file_path, 'w') as f:
            f.write(cursor)
        print(f"Cursor salvo com sucesso em {file_path}")
    except IOError as e:
        print(f"Erro ao salvar o cursor: {e}")

def load_cursor(file_path='cursor.txt'):
    try:
        with open(file_path, 'r') as f:
            cursor = f.read().strip()
            if cursor:
                print(f"Cursor carregado com sucesso de {file_path}")
                return cursor
            else:
                print(f"Arquivo {file_path} está vazio.")
                return None
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return None
    except IOError as e:
        print(f"Erro ao carregar o cursor: {e}")
        return None

# Função principal
def main():
    setup_logging()  # Configuração de logs
    
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()
    
    try:
        # Obter o token da variável de ambiente
        token = os.getenv("GITHUB_TOKEN")
        
        if not token:
            raise ValueError("GitHub token não encontrado. Defina a variável de ambiente 'GITHUB_TOKEN'.")
        
        # Inicializar o coletor de dados do GitHub
        collector = GitHubDataCollector(token)
        
        # Carregar o cursor salvo, se houver
        start_cursor = load_cursor()  # Carrega o cursor salvo de 'cursor.txt'

        # Coletar dados de repositórios do GitHub
        if start_cursor:
            print("Continuando a partir do cursor salvo...")
            raw_data, last_cursor = collector.get_repositories(num_repos=1 ,start_cursor=start_cursor)
        else:
            print("Nenhum cursor salvo encontrado, começando do início.")
            raw_data, last_cursor = collector.get_repositories(num_repos=50)

        # Salvar o novo cursor após a coleta
        save_cursor(last_cursor)
        
        # Processar os dados coletados
        processor = DataProcessor()
        processed_data = processor.process_raw_data(raw_data)
        
        # Salvar os dados processados em um CSV
        processor.save_to_csv('../collected_data/top_200_repos.csv')

    except GitHubAPIError as e:
        log_error(f"GitHub API error: {e}")
        print("Erro na API do GitHub. Verifique os logs para mais detalhes.")
    except DataProcessingError as e:
        log_error(f"Data processing error: {e}")
        print("Erro no processamento dos dados. Verifique os logs para mais detalhes.")
    except DataAnalysisError as e:
        log_error(f"Data analysis error: {e}")
        print("Erro na análise dos dados. Verifique os logs para mais detalhes.")
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        print("Ocorreu um erro inesperado. Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main()
