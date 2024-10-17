import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from feedbacks import *
from review_count import *


if __name__ == "__main__":
    dataframe = pd.read_csv("../collected_data/repositorios_com_metricas.csv")

    dataframe['pr_size'] = dataframe['pr_additions'] + dataframe['pr_deletions'] + dataframe['pr_changed_files']
    dataframe['feedback'] = dataframe['pr_state'].apply(lambda x: 'MERGED' if x == 'MERGED' else 'CLOSED')

    dataframe['pr_closed_or_merged_at'] = pd.to_datetime(dataframe['pr_closed_or_merged_at'])
    dataframe['pr_created_at'] = pd.to_datetime(dataframe['pr_created_at'])
    analysis_duration = dataframe['pr_closed_or_merged_at'] - dataframe['pr_created_at']
    dataframe['pr_analysis_duration'] = analysis_duration.dt.total_seconds() / 3600

    dataframe['pr_interactions'] = dataframe['pr_participants_count'] + dataframe['pr_comments_count']

    # A. Feedback Final das Revisões (Status do PR)
    pr_size_feedback(dataframe)
    pr_analysis_duration_feedback(dataframe)
    pr_description_feedback(dataframe)
    pr_interactions_feedback(dataframe)

    # B. Número de Revisões
    pr_size_review_count(dataframe)
    pr_analysis_duration_review_count(dataframe)
    pr_description_review_count(dataframe)
    pr_interactions_review_count(dataframe)
