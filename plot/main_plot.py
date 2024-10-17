import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from feedbacks import *


if __name__ == "__main__":
    dataframe = pd.read_csv("repositorios_com_metricas.csv")

    pr_size_feedback(dataframe)
    pr_analysis_duration_feedback(dataframe)
    pr_description_feedback(dataframe)
    pr_interactions_feedback(dataframe)
