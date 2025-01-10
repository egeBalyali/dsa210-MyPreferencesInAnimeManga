import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import seaborn as sns
import json
import os
import requests

input_file = "anime/normalCleanAnime.json"
# Sample Data
with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)  # Load the JSON data

# Preparing data
data_frame = pd.json_normalize(data, sep='_')
data_frame['taste_difference'] = data_frame['my_list_status_score'] - data_frame['mean']

"""
# 1. Popularity vs. Mean Score
plt.figure(figsize=(8, 6))
plt.scatter(data_frame['popularity'], data_frame['my_list_status_score'], color='blue', alpha=0.6)
plt.title('Popularity vs. Mean Score')
plt.xlabel('Popularity Rank')
plt.ylabel('Mean Score')
plt.grid(True)
plt.savefig('graphs/popularity_vs_mean_score.png')
plt.show()

# 2. Anime Status Distribution
# Anime Status Distribution
status_columns = [
    'statistics_status_watching',
    'statistics_status_completed',
    'statistics_status_on_hold',
    'statistics_status_dropped',
    'statistics_status_plan_to_watch'
]

# Convert columns to numeric in case of incorrect types
for col in status_columns:
    data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce')

status_counts = data_frame[status_columns].sum()
status_counts.index = ['Watching', 'Completed', 'On Hold', 'Dropped', 'Plan to Watch']

plt.figure(figsize=(8, 6))
status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Anime Status Distribution')
plt.ylabel('')
plt.savefig('graphs/anime_status_distribution.png')
plt.show()


# 3. Number of Episodes vs. Mean Score
plt.figure(figsize=(8, 6))
plt.scatter(data_frame['num_episodes'], data_frame['my_list_status_score'], color='green', alpha=0.6)
plt.title('Number of Episodes vs. Mean Score')
plt.xlabel('Number of Episodes')
plt.ylabel('Mean Score')
plt.grid(True)
plt.savefig('graphs/normalized_num_episodes_vs_mean_score.png')
plt.show()

# 4. Anime Genre Distribution
genre_list = [genre['name'] for genres in data_frame['genres'] for genre in genres]
genre_counts = Counter(genre_list)
plt.figure(figsize=(10, 6))
plt.bar(genre_counts.keys(), genre_counts.values(), color='orange')
plt.title('Anime Genre Distribution')
plt.xlabel('Genres')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graphs/anime_genre_distribution.png')
plt.show()

# 5. Anime Start Seasons
season_counts = data_frame['start_season_season'].value_counts()
plt.figure(figsize=(8, 6))
season_counts.plot(kind='bar', color='purple')
plt.title('Anime Start Seasons')
plt.xlabel('Season')
plt.ylabel('Count')
plt.savefig('graphs/anime_start_seasons.png')
plt.show()


# 7. Top Studios by Number of Anime Produced
studio_list = [studio['name'] for studios in data_frame['studios'] for studio in studios]
studio_counts = Counter(studio_list)
top_studios = dict(studio_counts.most_common(10))
plt.figure(figsize=(10, 6))
plt.bar(top_studios.keys(), top_studios.values(), color='teal')
plt.title('Top Studios by Number of Anime Produced')
plt.xlabel('Studio')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graphs/top_studios_by_anime_produced.png')
plt.show()


# 8. Genre vs. Mean Score
genre_scores = []
for _, row in data_frame.iterrows():
    for genre in row['genres']:
        genre_scores.append({'genre': genre['name'], 'mean_score': row['my_list_status_score']})

genre_scores_df = pd.DataFrame(genre_scores)

genre_mean_scores = genre_scores_df.groupby('genre')['mean_score'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 8))
genre_mean_scores.plot(kind='bar', color='skyblue')
plt.title('Average Mean Score by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Mean Score')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graphs/genre_vs_mean_score.png')
plt.show()
"""

"""

plt.figure(figsize=(10, 6))
plt.scatter(data_frame['mean'], data_frame['taste_difference'], color='blue', alpha=0.6)
plt.axhline(0, color='red', linestyle='--', label='No Difference')  # Line for zero difference
plt.title('Difference in Taste vs. Mean Score')
plt.xlabel('Mean Score')
plt.ylabel('Taste Difference (My Score - Mean Score)')
plt.legend()
plt.grid(True)
plt.savefig('graphs/taste_difference_vs_mean_score.png')
plt.show()"""

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
plt.savefig('graphs/taste_difference_by_genre.png')
plt.show()