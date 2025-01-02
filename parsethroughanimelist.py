from bs4 import BeautifulSoup
import os
import json

# Paths for input and output files
html_file_path = 'Dekusdad\'s Anime List - MyAnimeList.net.html'
output_text_path = 'data/EgeAnimeInfo.txt'
output_json_path = 'data/EgeAnimeJSON.json'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_text_path), exist_ok=True)

# Open and read the downloaded HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all entries in the table body
entries = soup.find_all('tbody', class_='list-item')

# List to hold extracted data
data = []

# Loop through each entry and extract required data
for entry in entries:
    show_data = {}

    # Extract the show ID (from the first 'href' in the 'data image' column)
    image_td = entry.find('td', class_='data image')
    if image_td:
        anchor = image_td.find('a', class_='link sort')
        if anchor and 'href' in anchor.attrs:
            show_url = anchor['href']
            show_id = show_url.split('/')[-2]  # Extracting the ID from the URL (e.g., 9513)
        else:
            show_id = None
    else:
        show_id = None

    # Extract the name of the show (from the 'data title' column)
    show_name = entry.find('td', class_='data title clearfix').find('a', class_='link sort').text.strip()
    if show_name in ["${ item.title_localized || item.anime_title }", ""]:
        show_name = None  # If it's a placeholder or empty

    # Extract the progress (from the 'data progress' column)
    progress_td = entry.find('td', class_='data progress')
    progress_numbers = progress_td.find_all('span')
    
    if len(progress_numbers) == 2:
        # If there are two numbers, the show is not finished, we extract them
        current_progress = progress_numbers[0].text.strip()
        total_progress = progress_numbers[1].text.strip()
        progress = f"{current_progress}/{total_progress}"
    else:
        # If there's only one number, the show is finished
        progress = progress_numbers[0].text.strip() if progress_numbers else None

    if progress == "0":
        progress = "-"  # Handle 0 as a finished case

    # Extract the score (from the 'data score' column)
    score_span = entry.find('td', class_='data score').find('span', class_='score-label')
    if score_span:
        score = score_span.text.strip()
    else:
        score = "N/A"

    # Store the extracted data in a dictionary
    show_data['id'] = show_id
    show_data['name'] = show_name
    show_data['progress'] = progress
    show_data['score'] = score

    # Append the data to the list
    data.append(show_data)

# Write the parsed data to the text file
with open(output_text_path, 'w', encoding='utf-8') as output_file:
    for show in data:
        output_file.write(f"ID: {show['id']}\n")
        output_file.write(f"Name: {show['name']}\n")
        output_file.write(f"Progress: {show['progress']}\n")
        output_file.write(f"Score: {show['score']}\n")
        output_file.write('-' * 40 + '\n')

# Write the parsed data to the JSON file
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
