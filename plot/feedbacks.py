import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# repo_name,repo_owner,pr_created_at,pr_closed_or_merged_at,pr_state,pr_reviews_count,pr_review_duration_hours,pr_additions,pr_deletions,pr_changed_files,pr_comments_count,pr_participants_count,pr_description_length

def pr_size_feedback(dataframe):
    dataframe['pr_size'] = dataframe['pr_additions'] + dataframe['pr_deletions'] + dataframe['pr_changed_files']
    dataframe['feedback'] = dataframe['pr_state'].apply(lambda x: 'MERGED' if x == 'MERGED' else 'CLOSED')

    plt.figure(figsize=(10, 20))

    ax = sns.boxplot(x='feedback', y='pr_size', data=dataframe)

    ax.set_yscale('log')

    plt.title('Distribuição do Tamanho dos PRs por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Tamanho dos PRs')

    plt.tight_layout()

    plt.savefig('graphs/rq1.png')
    plt.clf()

def pr_analysis_duration_feedback(dataframe):
    dataframe['feedback'] = dataframe['pr_state'].apply(lambda x: 'MERGED' if x == 'MERGED' else 'CLOSED')

    dataframe['pr_closed_or_merged_at'] = pd.to_datetime(dataframe['pr_closed_or_merged_at'])
    dataframe['pr_created_at'] = pd.to_datetime(dataframe['pr_created_at'])
    dataframe['pr_analysis_duration'] = dataframe['pr_closed_or_merged_at'] - dataframe['pr_created_at']

    plt.figure(figsize=(10, 20))

    ax = sns.boxplot(x='feedback', y='pr_analysis_duration', data=dataframe)

    ax.set_yscale('log')

    plt.title('Distribuição do Tempo de Análise do PR por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Tempo de Análise (Horas)')

    plt.tight_layout()

    plt.savefig('graphs/rq2.png')
    plt.clf()

def pr_description_feedback(dataframe):
    dataframe['feedback'] = dataframe['pr_state'].apply(lambda x: 'MERGED' if x == 'MERGED' else 'CLOSED')

    plt.figure(figsize=(10, 20))

    ax = sns.boxplot(x='feedback', y='pr_description_length', data=dataframe)

    ax.set_yscale('log')

    plt.title('Distribuição do Tamanho das Descrições por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Tamanho das Descrições')

    plt.tight_layout()

    plt.savefig('graphs/rq3.png')
    plt.clf()

def pr_interactions_feedback(dataframe):
    dataframe['feedback'] = dataframe['pr_state'].apply(lambda x: 'MERGED' if x == 'MERGED' else 'CLOSED')
    # Todas as interações
    dataframe['pr_interactions'] = dataframe['pr_participants_count'] + dataframe['pr_comments_count']
    plt.figure(figsize=(10, 20))

    ax = sns.boxplot(x='feedback', y='pr_interactions', data=dataframe)

    ax.set_yscale('log')

    plt.title('Distribuição de Interações por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Número de interações')

    plt.tight_layout()

    plt.savefig('graphs/rq4.png')
    plt.clf()

    # Comentários
    plt.figure(figsize=(10, 20))

    ax = sns.boxplot(x='feedback', y='pr_comments_count', data=dataframe)

    ax.set_yscale('log')

    plt.title('Distribuição de Quantidade de Comentários por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Quantidade de Comentários')

    plt.tight_layout()

    plt.savefig('graphs/rq4_comments.png')
    plt.clf()

    # Participantes
    plt.figure(figsize=(10, 20))

    ax = sns.boxplot(x='feedback', y='pr_participants_count', data=dataframe)

    ax.set_yscale('log')

    plt.title('Distribuição de Quantidade de Participantes por Feedback Final')
    plt.xlabel('Feedback Final (Merged/Closed)')
    plt.ylabel('Quantidade de Participantes')

    plt.tight_layout()

    plt.savefig('graphs/rq4_participants.png')
    plt.clf()