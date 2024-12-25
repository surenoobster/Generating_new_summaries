import json
from tqdm import tqdm

def open_file(file):
    entities = []
    with open(file, 'r') as f:
        for line in f.readlines():
            entities.append(json.loads(line))
    return entities

def save_file(data, file):
    with open(file, 'w') as f:
        for line in data:
            f.write(json.dumps(line) + "\n")

def get_prompt(flesch_summary):
    # Generate a prompt based on the flesch score
    prompt = 'Write highlights for this article with a Flesch-Kincaid score of ' + str(
        int(round(flesch_summary, 0))) + ":\n\n"
    return prompt

def transform_data(input_file, output_file):
    data = open_file(input_file)
    new_data = []

    for entry in tqdm(data):
        # Extract flesch scores
        flesch_summary = entry["summary_metrics"]["flesch"]
        flesch_input = entry["input_metrics"]["flesch"]

        # Generate prompt
        prompt = get_prompt(flesch_summary)
        entry["prompt"] = prompt
        entry["input_noprompt"] = entry["input"]
        entry["input"] = prompt + entry["input"]

        # Skip test entries with input flesch score >= 50
        if 'test' in input_file and flesch_input >= 50:
            continue

        new_data.append(entry)

    # Save the transformed data
    save_file(new_data, output_file)

# File paths
input_file = '/home/surenoobster/Documents/controllable-readability-summarization/src/18dec_retried_finalboss/valid_metrics_summary_article_cleaned.json'
output_file = '/home/surenoobster/Documents/controllable-readability-summarization/src/18dec_retried_finalboss/valid_score_category.json'

# Transform the data
transform_data(input_file, output_file)

print(f"Transformed data saved to: {output_file}")
