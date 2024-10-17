import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# repo_name,repo_owner,pr_created_at,pr_closed_or_merged_at,pr_state,pr_reviews_count,pr_review_duration_hours,pr_additions,pr_deletions,pr_changed_files,pr_comments_count,pr_participants_count,pr_description_length

# RQ5
def pr_size_review_count(dataframe):
    pr_size = dataframe['pr_size']
    review_count = dataframe['pr_reviews_count']
    plt.figure(figsize=(15, 6))

    plt.scatter(pr_size, review_count, label='Tamanho dos PRs', color='blue', marker='o', s=15)
    plt.title('Tamanho dos PRs X Quantidade de Revisões')
    plt.xlabel('Tamanho dos PRs')
    plt.ylabel('Quantidade de Revisões')

    plt.xscale('log')

    plt.tight_layout()
    plt.savefig('graphs/rq5.png')
    plt.clf()

# RQ6
def pr_analysis_duration_review_count(dataframe):
    pr_analysis_duration = dataframe['pr_analysis_duration']
    review_count = dataframe['pr_reviews_count']
    plt.figure(figsize=(15, 6))

    plt.scatter(pr_analysis_duration, review_count, label='Tempo de Análise', color='blue', marker='o', s=15)
    plt.title('Tempo de Análise X Quantidade de Revisões')
    plt.xlabel('Tempo de Análise')
    plt.ylabel('Quantidade de Revisões')

    plt.xscale('log')
    
    plt.tight_layout()
    plt.savefig('graphs/rq6.png')
    plt.clf()