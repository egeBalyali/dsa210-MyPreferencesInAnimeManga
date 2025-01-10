import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import json
import joblib
import seaborn as sns
# Load dataset
with open('anime/cleanAnime.json', 'r') as file:
    anime_data = json.load(file)

# Normalize JSON data into a DataFrame
data_frame = pd.json_normalize(anime_data)

# Extract 'score' from 'my_list_status' and use it as the target column
if 'my_list_status.score' in data_frame.columns:
    data_frame['your_score'] = data_frame['my_list_status.score'].fillna(0)  # Replace NaN scores with 0
else:
    raise ValueError("'my_list_status.score' field is missing in the dataset.")

# Check for required fields
required_columns = ['mean', 'num_episodes', 'rating', 'genres']
missing_columns = [col for col in required_columns if col not in data_frame]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Extract unique genres from the dataset
genre_list = [
    genre['name'] 
    for genres in data_frame['genres'] 
    for genre in genres
]
unique_genres = list(set(genre_list))  # Remove duplicates to get unique genres

# Create columns for each unique genre and populate them
for genre in unique_genres:
    data_frame[f'genre_{genre}'] = data_frame['genres'].apply(
        lambda x: 1 if any(g['name'] == genre for g in x) else 0
    )

# Define features and target
features = ['mean', 'num_episodes', 'rating'] + [f'genre_{genre}' for genre in unique_genres]
target = 'your_score'

# Split data into training and testing
train_data, test_data = train_test_split(data_frame, test_size=0.2, random_state=42)

# Ensure all genre columns are present in both datasets
for genre in unique_genres:
    genre_column = f'genre_{genre}'
    if genre_column not in train_data:
        train_data[genre_column] = 0  # Add missing column with all zeros
    if genre_column not in test_data:
        test_data[genre_column] = 0  # Add missing column with all zeros

# Prepare feature matrices and target vectors
X_train = train_data[features]
y_train = train_data[target]
X_test = test_data[features]
y_test = test_data[target]

# Preprocessing pipeline
categorical_features = ['rating']
numeric_features = ['mean', 'num_episodes'] + [f'genre_{genre}' for genre in unique_genres]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

# Regression model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train the model
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

# Extract and print coefficients
# Get the feature names from the pipeline
numeric_feature_names = numeric_features
categorical_feature_names = model.named_steps['preprocessor'].transformers_[1][1].get_feature_names_out(categorical_features)
all_feature_names = numeric_feature_names + list(categorical_feature_names)

# Get the coefficients from the regressor
coefficients = model.named_steps['regressor'].coef_

# Combine feature names with coefficients
coefficients_df = pd.DataFrame({'Feature': all_feature_names, 'Coefficient': coefficients})
coefficients_df_sorted = coefficients_df.sort_values(by='Coefficient', ascending=False)

# Save coefficients and error metrics to a file
output_file = 'model_summary.txt'
with open(output_file, 'w') as f:
    f.write("Model Summary\n")
    f.write("========================\n")
    f.write(f"Mean Absolute Error: {mae:.2f}\n")
    f.write(f"Mean Squared Error: {mse:.2f}\n")
    f.write("\nCoefficients:\n")
    f.write(coefficients_df_sorted.to_string(index=False))
    f.write("\n")

print(f"Model summary saved to {output_file}")

# Visualize predictions vs. actual values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title('Predicted vs. Actual Scores')
plt.xlabel('Actual Scores')
plt.ylabel('Predicted Scores')
plt.grid(True)
plt.savefig('predicted_vs_actual_scores.png')
plt.show()

# Save the model for future use
joblib.dump(model, 'anime_score_predictor.pkl')



coefficients_df_sorted['Absolute Coefficient'] = coefficients_df_sorted['Coefficient'].abs()
coefficients_df_sorted = coefficients_df_sorted.sort_values(by='Absolute Coefficient', ascending=False)

# Plot the coefficients
plt.figure(figsize=(10, 8))
sns.barplot(
    data=coefficients_df_sorted,
    x='Coefficient',
    y='Feature',
    palette='coolwarm',
    orient='h'
)
plt.title('Feature Coefficients (Sorted by Absolute Value)', fontsize=14)
plt.xlabel('Coefficient Value', fontsize=12)
plt.ylabel('Features', fontsize=12)
plt.tight_layout()
plt.savefig('graphs/feature_coefficients.png')
plt.show()

# Create a summary figure for metrics
fig, ax = plt.subplots(figsize=(8, 4))
metrics = pd.DataFrame({'Metric': ['Mean Absolute Error', 'Mean Squared Error'], 'Value': [mae, mse]})
sns.barplot(data=metrics, x='Value', y='Metric', palette='viridis', ax=ax)
ax.set_title('Model Error Metrics', fontsize=14)
ax.set_xlabel('Error Value', fontsize=12)
ax.set_ylabel('Metrics', fontsize=12)
plt.tight_layout()
plt.savefig('graphs/error_metrics.png')
plt.show()