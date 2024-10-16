import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# repo_name,repo_owner,pr_created_at,pr_closed_or_merged_at,pr_state,pr_reviews_count,pr_review_duration_hours,pr_additions,pr_deletions,pr_changed_files,pr_comments_count,pr_participants_count,pr_description_length

# RQ 1
def prs_size_feedback(dataframe):
    pr_size = dataframe['pr_additions'] + dataframe['pr_deletions'] + dataframe['pr_changed_files']
    feedback = dataframe['pr_state'].apply(lambda x: 1 if x == 'MERGED' else 0)

    plt.figure(figsize=(15, 6))

    # cbo_media
    plt.scatter(pr_size, feedback, label='Tamanho dos PRs', color='blue', marker='o', s=15)

    plt.title('Tamanho dos PRs X Feedback Final')
    plt.xlabel('Tamanho dos PRs')
    plt.ylabel('Feedback Final (Merged/Closed)')

    plt.tight_layout()

    plt.savefig('graphs/rq1.png')
    plt.clf()


def prs_size_feedback_boxplot(dataframe):
    dataframe['pr_size'] = dataframe['pr_additions'] + dataframe['pr_deletions'] + dataframe['pr_changed_files']
    dataframe['feedback'] = dataframe['pr_state'].apply(lambda x: 'MERGED' if x == 'MERGED' else 'CLOSED')

    plt.figure(figsize=(10, 6))

    sns.boxplot(x='feedback', y='pr_size', data=dataframe)

    plt.title('Distribuição do Tamanho dos PRs por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Tamanho dos PRs')

    plt.tight_layout()

    plt.savefig('graphs/rq1_boxplot.png')
    plt.clf()


if __name__ == "__main__":
    dataframe = pd.read_csv("repositorios_com_metricas.csv")

    prs_size_feedback(dataframe)
    prs_size_feedback_boxplot(dataframe)

