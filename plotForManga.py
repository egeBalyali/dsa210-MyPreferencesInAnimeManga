import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import seaborn as sns
import json
import os
import requests
from scipy.stats import pearsonr,spearmanr
input_file = "manga/normalCleanManga.json"
# Sample Data
with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)  # Load the JSON data

# Preparing data
data_frame = pd.json_normalize(data, sep='_')
data_frame['taste_difference'] = data_frame['my_list_status_score'] - data_frame['mean']
def calculate_correlations(x, y):
    pearson_corr, pearson_p_value = pearsonr(x, y)
    spearman_corr, spearman_p_value = spearmanr(x, y)
    return pearson_corr, pearson_p_value, spearman_corr, spearman_p_value

plt.figure(figsize=(10, 6))
plt.scatter(data_frame['popularity'], data_frame['my_list_status_score'], color='blue', alpha=0.6)
plt.title('Popularity vs. Mean Score')
plt.xlabel('Popularity')
plt.ylabel('My Score')
plt.grid(True)
pearson_corr_pop, p_value_pop, spearman_corr_pop, spearman_p_value_pop = calculate_correlations(data_frame['popularity'], data_frame['my_list_status_score'])
plt.legend([f'Pearson: {pearson_corr_pop:.3f}, p: {p_value_pop:.3f}\nSpearman: {spearman_corr_pop:.3f}, p: {spearman_p_value_pop:.3f}'], loc='best')
plt.savefig('mangagraphs/Normalized_popularity_vs_mean_score.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(data_frame['my_list_status_num_chapters_read'],data_frame['my_list_status_score'], color='green', alpha=0.6)
plt.title('Chapters Read vs. Given Score')
plt.xlabel('Chapters Read')
plt.ylabel('Score Given')
plt.grid(True)
pearson_corr_chap, p_value_chap, spearman_corr_chap, spearman_p_value_chap = calculate_correlations(data_frame['my_list_status_num_chapters_read'], data_frame['my_list_status_score'])
plt.legend([f'Pearson: {pearson_corr_chap:.3f}, p: {p_value_chap:.3f}\nSpearman: {spearman_corr_chap:.3f}, p: {spearman_p_value_chap:.3f}'], loc='best')
plt.savefig('mangagraphs/chapters_read_vs_score.png')
plt.show()


data_frame['genres_list'] = data_frame['genres'].apply(lambda x: [g['name'] for g in x])
exploded_df = data_frame.explode('genres_list')

genre_counts = exploded_df['genres_list'].value_counts()

plt.figure(figsize=(12, 8))
genre_counts.plot(kind='bar', color='purple', alpha=0.7)
plt.title('Genre Distribution')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('mangagraphs/genre_distribution.png')
plt.show()




media_type_scores = data_frame.groupby('media_type')['my_list_status_score'].mean().sort_values()

# Bar plot
plt.figure(figsize=(10, 6))
media_type_scores.plot(kind='bar', color='orange', alpha=0.7)
plt.title('Mean Score by Media Type')
plt.xlabel('Media Type')
plt.ylabel('Average Mean Score')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('mangagraphs/mean_score_by_media_type.png')
plt.show()

data_frame['progress_percentage'] = data_frame['my_list_status_num_chapters_read'] / data_frame['num_chapters'] * 100

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(data_frame['progress_percentage'], 
            data_frame['my_list_status_score'], color='red', alpha=0.6)
plt.title('Progress Percentage vs. Your Score')
plt.xlabel('Progress Percentage (%)')
plt.gca().invert_xaxis()
plt.ylabel('Your Score')
plt.grid(True)
plt.savefig('mangagraphs/progress_vs_score.png')
plt.show()



# Step 1: Explode the genres into separate rows
data_frame['genres_list'] = data_frame['genres'].apply(lambda x: [g['name'] for g in x])
exploded_df = data_frame.explode('genres_list')

# Step 2: Aggregate taste difference by genre
data_frame['taste_difference'] = data_frame['my_list_status_score'] - data_frame['mean']
genre_difference = exploded_df.groupby('genres_list')['taste_difference'].mean().sort_values()

# Step 3: Plot the bar graph
plt.figure(figsize=(12, 8))
plt.bar(genre_difference.index, genre_difference, color=['green' if x > 0 else 'red' for x in genre_difference])
plt.axhline(0, color='black', linestyle='--', linewidth=1)  # Zero line for reference
plt.title('Taste Difference by Genre')
plt.xlabel('Genre')
plt.ylabel('Taste Difference (My Score - Mean Score)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('mangagraphs/taste_difference_by_genre.png')
plt.show()

