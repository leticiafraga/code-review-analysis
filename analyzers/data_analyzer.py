import pandas as pd
from utils.utils import log_error

class DataAnalyzer:
    def __init__(self, processed_data):
        self.processed_data = processed_data

    def analyze_general(self):
        try:
            general_analysis = {
                "median_age": self.processed_data['age'].median(),
                "median_pull_requests": self.processed_data['pullRequests'].median(),
                "median_releases": self.processed_data['releases'].median(),
                "median_update_frequency": self.processed_data['last_update'].median(),
                "median_issue_closure_ratio": self.processed_data['issue_closure_ratio'].median()
            }
            return general_analysis

        except Exception as e:
            log_error(f"Error during general analysis: {e}")
            raise

    def analyze_by_language(self):
        try:
            # Top 10 linguagens mais populares
            top_languages = [
                'JavaScript', 'Python', 'TypeScript', 'Java', 'C#',
                'C++', 'PHP', 'C', 'Shell', 'Go'
            ]

            # Contagem de repositórios por linguagem
            language_counts = self.processed_data['primaryLanguage'].value_counts()

            # Filtro para considerar apenas as linguagens mais populares
            popular_language_counts = language_counts[language_counts.index.isin(top_languages)]

            # Preparar o resultado para retorno
            language_analysis = {
                "total_repos_analyzed": len(self.processed_data),
                "popular_language_counts": popular_language_counts.to_dict(),
                "other_languages_count": language_counts[~language_counts.index.isin(top_languages)].sum()
            }

            return language_analysis

        except Exception as e:
            log_error(f"Error during language analysis: {e}")
            raise

