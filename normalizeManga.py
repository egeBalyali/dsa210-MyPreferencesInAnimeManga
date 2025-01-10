import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import seaborn as sns
import json

# Input file
input_file = "anime/normalCleanAnime.json"

# Load JSON data
with open(input_file, "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Filter out entries with `my_list_status.score == 0`
filtered_data = [entry for entry in data if entry.get("my_list_status", {}).get("score", 0) > 0]

# Prepare data
data_frame = pd.json_normalize(filtered_data, sep='_')

# Adjust the mean scores based on my_list_status
def calculate_weighted_mean(row):
    """
    Calculate weighted mean using my_list_status scores and statuses.
    """
    weights = {
        'watching': row.get('statistics_status_watching', 0),
        'completed': row.get('statistics_status_completed', 0),
        'on_hold': row.get('statistics_status_on_hold', 0),
        'dropped': row.get('statistics_status_dropped', 0),
        'plan_to_watch': row.get('statistics_status_plan_to_watch', 0)
    }
    scores = {
        'watching': row.get('my_list_status_score_watching', 0),
        'completed': row.get('my_list_status_score_completed', 0),
        'on_hold': row.get('my_list_status_score_on_hold', 0),
        'dropped': row.get('my_list_status_score_dropped', 0),
        'plan_to_watch': row.get('my_list_status_score_plan_to_watch', 0)
    }
    total_weight = sum(weights.values())
    if total_weight == 0:
        return row.get('mean', 0)  # Fall back to existing mean if no weights
    weighted_mean = sum(weights[status] * scores[status] for status in weights) / total_weight
    return weighted_mean

# Add weighted mean to the DataFrame
data_frame['adjusted_mean'] = data_frame.apply(calculate_weighted_mean, axis=1)

# Visualizations
# 1. Popular
