import json
from readability import Readability
from datasets import load_dataset
import os
import random

# Update the path to your local dataset file
data_files = {
    "train": "/home/surenoobster/Documents/controllable-readability-summarization/src/18Dec/validation_greater_110_article_10_summary.json"
}

# Load dataset from local file
dataset = load_dataset("json", data_files=data_files)

# Function to compute readability metrics
def get_flesch_kincaid(text):
    r = Readability(text)
    fk = r.flesch_kincaid()
    return fk.score

def get_flesch(text):
    r = Readability(text)
    f = r.flesch()
    return f.score

def get_dale_chall(text):
    r = Readability(text)
    dc = r.dale_chall()
    return dc.score

def get_ari(text):
    r = Readability(text)
    ari = r.ari()
    return ari.score

def get_coleman_liau(text):
    r = Readability(text)
    cl = r.coleman_liau()
    return cl.score

def get_gunning_fog(text):
    r = Readability(text)
    gf = r.gunning_fog()
    return gf.score

def get_smog(text):
    r = Readability(text)
    s = r.smog()
    return s.score

def get_spache(text):
    r = Readability(text)
    s = r.spache()
    return s.score

def get_linsear_write(text):
    r = Readability(text)
    lw = r.linsear_write()
    return lw.score

# Function to compute all readability metrics
def compute_metrics(text):
    metrics = {}

    # Check for minimum word count (100 words)
    if len(text.split()) >= 100:
        try:
            metrics['flesch'] = round(get_flesch(text), 4)
        except Exception as e:
            metrics['flesch'] = None  # Or handle error as needed

        try:
            metrics['dale_chall'] = round(get_dale_chall(text), 4)
        except Exception as e:
            metrics['dale_chall'] = None  # Or handle error as needed

        try:
            metrics['coleman_liau'] = round(get_coleman_liau(text), 4)
        except Exception as e:
            metrics['coleman_liau'] = None  # Or handle error as needed

        try:
            metrics['gunning_fog'] = round(get_gunning_fog(text), 4)
        except Exception as e:
            metrics['gunning_fog'] = None  # Or handle error as needed
    else:
        # If the text is too short, we can assign default values or skip
        metrics['flesch'] = None
        metrics['dale_chall'] = None
        metrics['coleman_liau'] = None
        metrics['gunning_fog'] = None

    return metrics

# Function to save processed data to a file
def save_file(data, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as file_writer:
        for line in data:
            file_writer.write(json.dumps(line) + "\n")
def process_data():
    data = []
    output_dir = '/home/surenoobster/Documents/controllable-readability-summarization/src/18dec_retried_finalboss'

    # Process the entire dataset without sampling
    for idx in range(len(dataset['train'])):
        article = dataset['train']['article'][idx]
        summary = dataset['train']['summary'][idx]
        id_ = dataset['train']['id'][idx]

        entry = {}

        # Add the article (input) and compute its metrics
        entry['input'] = article
        entry['input_metrics'] = compute_metrics(entry["input"])

        # Add the summary and compute its metrics separately
        entry['summary'] = summary
        entry['summary_metrics'] = compute_metrics(entry["summary"])

        # Add the ID for reference
        entry['id'] = str(id_)

        # Append the entry to the data list
        data.append(entry)

    # Save the data to a JSON file
    save_file(data, f'{output_dir}/valid_metrics_summary_article_full.json')

# Process the "train" split dataset
process_data()

