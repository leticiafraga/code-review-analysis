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
    plt.title('Tempo de Análise (Horas) X Quantidade de Revisões')
    plt.xlabel('Tempo de Análise (Horas)')
    plt.ylabel('Quantidade de Revisões')

    plt.xscale('log')
    
    plt.tight_layout()
    plt.savefig('graphs/rq6.png')
    plt.clf()

# RQ7
def pr_description_review_count(dataframe):
    pr_description_length = dataframe['pr_description_length']
    review_count = dataframe['pr_reviews_count']
    plt.figure(figsize=(15, 6))

    plt.scatter(pr_description_length, review_count, label='Tamanho da Descrição', color='blue', marker='o', s=15)
    plt.title('Tamanho da Descrição X Quantidade de Revisões')
    plt.xlabel('Tamanho da Descrição')
    plt.ylabel('Quantidade de Revisões')

    plt.xscale('log')

    plt.tight_layout()
    plt.savefig('graphs/rq7.png')
    plt.clf()

# RQ8
def pr_interactions_review_count(dataframe):
    pr_interactions = dataframe['pr_interactions']
    review_count = dataframe['pr_reviews_count']
    comments_count = dataframe['pr_comments_count']
    participants_count = dataframe['pr_participants_count']

    plt.figure(figsize=(15, 6))

    plt.scatter(pr_interactions, review_count, label='Interações', color='blue', marker='o', s=15)
    plt.title('Interações X Quantidade de Revisões')
    plt.xlabel('Interações')
    plt.ylabel('Quantidade de Revisões')

    plt.tight_layout()
    plt.savefig('graphs/rq8.png')
    plt.clf()

    plt.figure(figsize=(15, 6))

    plt.scatter(pr_interactions, comments_count, label='Interações', color='blue', marker='o', s=15)
    plt.title('Comentários X Quantidade de Revisões')
    plt.xlabel('Comentários')
    plt.ylabel('Quantidade de Revisões')

    plt.tight_layout()
    plt.savefig('graphs/rq8_comments.png')
    plt.clf()

    plt.figure(figsize=(15, 6))

    plt.scatter(pr_interactions, participants_count, label='Interações', color='blue', marker='o', s=15)
    plt.title('Participantes X Quantidade de Revisões')
    plt.xlabel('Participantes')
    plt.ylabel('Quantidade de Revisões')

    plt.tight_layout()
    plt.savefig('graphs/rq8_participants.png')
    plt.clf()