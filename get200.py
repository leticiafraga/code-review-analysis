import requests
import csv

def get_top_repositories():
    url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {
        "q": "stars:>1",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
    }

    repositories = []

    for page in range(1, 3):  # Para obter 200 repositórios, precisamos de 2 páginas (100 por página)
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            repositories.extend(data["items"])
        else:
            print(f"Erro ao buscar dados: {response.status_code}")
            return []

    return repositories

def save_to_csv(repositories, filename="top_200_repositories.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Owner", "Stars", "URL"])

        for repo in repositories:
            writer.writerow([repo["name"], repo["owner"]["login"], repo["stargazers_count"], repo["html_url"]])

def main():
    repositories = get_top_repositories()
    if repositories:
        save_to_csv(repositories)
        print("Dados dos 200 principais repositórios salvos em 'top_200_repositories.csv'")
    else:
        print("Não foi possível obter os repositórios.")

if __name__ == "__main__":
    main()