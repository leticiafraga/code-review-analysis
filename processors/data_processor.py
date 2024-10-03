import pandas as pd
from datetime import datetime
from utils.utils import log_error
from utils.custom_exceptions import DataProcessingError
import os

class DataProcessor:
    def __init__(self):
        self.data = pd.DataFrame()

    def process_raw_data(self, raw_data):
        try:
            data = {
                "name": [],
                "createdAt": [],
                "pullRequests": [],
                "releases": [],
                "url": [],
            }

            if isinstance(raw_data, list):
                for repo in raw_data:
                    if not isinstance(repo, dict):
                        print(f"Skipping invalid repo structure: {repo}")
                        continue

                    name = repo.get("name", "N/A")
                    created_at = repo.get("createdAt", "N/A")
                    pull_requests_count = repo.get("pullRequests", {}).get("totalCount", 0)
                    releases_count = repo.get("releases", {}).get("totalCount", 0)
                    url = repo.get("url", "N/A")
                    updated_at = repo.get("updatedAt", "N/A")

                    data["name"].append(name)
                    data["createdAt"].append(created_at)
                    data["pullRequests"].append(pull_requests_count)
                    data["releases"].append(releases_count)
                    data["url"].append(url)

            self.data = pd.DataFrame(data)

            return self.data

        except Exception as e:
            log_error(f"Unexpected error during data processing: {e}")
            raise DataProcessingError(message=str(e))

    def save_to_csv(self, file_path):
        try:
            # Verificar se o arquivo já existe
            file_exists = os.path.isfile(file_path)
            
            # Se o arquivo já existir, usar mode='a' (append), e header=False para não duplicar cabeçalhos
            self.data.to_csv(file_path, mode='a', header=not file_exists, index=False)
            print(f"Data saved to {file_path}")
        except Exception as e:
            log_error(f"Error saving data to CSV: {e}")
            raise
