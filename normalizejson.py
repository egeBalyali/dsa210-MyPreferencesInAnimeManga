import json

# Define the fields to remove
fields_to_remove = [
    "synopsis", "nsfw", "created_at", "updated_at",
    "authors", "pictures", "background", 
    "recommendations", "serialization", "alternative_titles", "main_picture","related_anime"
]

# Function to remove specified fields from a dictionary
def clean_object(obj):
    for field in fields_to_remove:
        obj.pop(field, None)  # Remove field if it exists
    return obj

# Function to filter objects with num_episodes <= 200
def filter_object(obj):
    if "num_episodes" in obj and isinstance(obj["num_episodes"], int):
        return obj["num_episodes"] <= 40
    return True  # Keep objects without the num_episodes field

# Main function to process the JSON file
def process_json_file(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)  # Load the JSON data
        data = [entry for entry in data if entry.get("my_list_status", {}).get("score", 0) > 0]
        if isinstance(data, list):
            # If the JSON data is a list of objects
            cleaned_data = [clean_object(obj) for obj in data if filter_object(obj)]
        elif isinstance(data, dict):
            # If the JSON data is a single object
            if filter_object(data):
                cleaned_data = clean_object(data)
            else:
                cleaned_data = {}
        else:
            raise ValueError("Unsupported JSON structure")

        with open(output_file, "w", encoding="utf-8") as outfile:
            json.dump(cleaned_data, outfile, indent=4, ensure_ascii=False)

        print(f"Processed JSON data has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output file paths
input_file = "manga/allInfo.json"  # Replace with the path to your input file
output_file = "manga/normalCleanAnime.json"  # Replace with the path to your output file

# Call the function
process_json_file(input_file, output_file)
