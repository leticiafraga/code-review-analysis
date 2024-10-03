import pandas as pd
from scipy.stats import pearsonr, spearmanr

# Função para calcular a correlação e retornar os resultados
def calculate_correlation(data, x_col, y_col, method="pearson"):
    if method == "pearson":
        corr, p_value = pearsonr(data[x_col], data[y_col])
    elif method == "spearman":
        corr, p_value = spearmanr(data[x_col], data[y_col])
    return corr, p_value

# Função para gerar as correlações e salvar em CSV
def generate_correlation_report(data, output_csv):
    results = []

    # 1. Relação entre o tamanho dos PRs e o feedback final
    data['feedback_final'] = data['pr_closed_or_merged_at'].notnull().astype(int)  # 1 se merged, 0 se closed
    data['tamanho'] = data['pr_additions'] + data['pr_deletions']  # Soma de adições e deleções

    corr, p_value = calculate_correlation(data, 'tamanho', 'feedback_final')
    results.append(['RQ01', 'Tamanho do PR', 'Feedback Final (Merged/Closed)', corr, p_value])

    # 2. Relação entre o tempo de análise dos PRs e o feedback final
    corr, p_value = calculate_correlation(data, 'pr_review_duration_hours', 'feedback_final')
    results.append(['RQ02', 'Tempo de Análise', 'Feedback Final (Merged/Closed)', corr, p_value])

    # 3. Relação entre a descrição dos PRs e o feedback final
    corr, p_value = calculate_correlation(data, 'pr_description_length', 'feedback_final')
    results.append(['RQ03', 'Descrição do PR', 'Feedback Final (Merged/Closed)', corr, p_value])

    # 4. Relação entre as interações nos PRs e o feedback final
    data['interacoes'] = data['pr_comments_count'] + data['pr_participants_count']
    corr, p_value = calculate_correlation(data, 'interacoes', 'feedback_final')
    results.append(['RQ04', 'Interações', 'Feedback Final (Merged/Closed)', corr, p_value])

    # 5. Relação entre o tamanho dos PRs e o número de revisões realizadas
    corr, p_value = calculate_correlation(data, 'tamanho', 'pr_reviews_count')
    results.append(['RQ05', 'Tamanho do PR', 'Número de Revisões', corr, p_value])

    # 6. Relação entre o tempo de análise dos PRs e o número de revisões realizadas
    corr, p_value = calculate_correlation(data, 'pr_review_duration_hours', 'pr_reviews_count')
    results.append(['RQ06', 'Tempo de Análise', 'Número de Revisões', corr, p_value])

    # 7. Relação entre a descrição dos PRs e o número de revisões realizadas
    corr, p_value = calculate_correlation(data, 'pr_description_length', 'pr_reviews_count')
    results.append(['RQ07', 'Descrição do PR', 'Número de Revisões', corr, p_value])

    # 8. Relação entre as interações nos PRs e o número de revisões realizadas
    corr, p_value = calculate_correlation(data, 'interacoes', 'pr_reviews_count')
    results.append(['RQ08', 'Interações', 'Número de Revisões', corr, p_value])

    # Converter resultados para um DataFrame e salvar em CSV
    results_df = pd.DataFrame(results, columns=['Pergunta de Pesquisa', 'Métrica X', 'Métrica Y', 'Correlação', 'p-value'])
    results_df.to_csv(output_csv, index=False)

# Leitura dos dados do CSV
data = pd.read_csv('repositorios_com_metricas.csv')

# Gerar o relatório de correlações e salvar em CSV
output_csv = 'correlacoes_metricas.csv'
generate_correlation_report(data, output_csv)

print(f"Relatório de correlações salvo em '{output_csv}'")
