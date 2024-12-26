import pandas as pd
import numpy as np
from collections import Counter

# Function to calculate Positional Entropy and Bias Score
def calculate_npb(correct_positions, alpha=0.5, beta=0.5):
    total_questions = len(correct_positions)
    counts = Counter(correct_positions)

    probabilities = np.array([counts.get(i, 0) / total_questions for i in range(1, 5)])
    entropy = -np.sum([p * np.log2(p) for p in probabilities if p > 0])
    max_entropy = 2  # Log2(4) for 4 positions
    bias_score = np.sum(np.abs(probabilities - 0.25))
    max_bias = 1.5  # Maximum bias

    normalized_entropy = 1 - (entropy / max_entropy)
    normalized_bias = bias_score / max_bias
    npb = alpha * normalized_entropy + beta * normalized_bias

    return npb, entropy, bias_score, probabilities

# Function to calculate GNPB
def calculate_gnpb(correct_positions, group_size=4, alpha=0.5, beta=0.5):
    groups = [correct_positions[i:i + group_size] for i in range(0, len(correct_positions), group_size)]
    group_npbs = []

    for group in groups:
        _, entropy, bias_score, _ = calculate_npb(group, alpha, beta)
        group_npb = alpha * (1 - (entropy / 2)) + beta * (bias_score / 1.5)
        group_npbs.append(group_npb)

    gnpb = np.mean(group_npbs)
    return gnpb, group_npbs

# Function to process a single CSV file
def process_csv(file_path):
    df = pd.read_csv(file_path)
    correct_positions = df['answer'].tolist()

    # Calculate NPB
    npb, entropy, bias_score, probabilities = calculate_npb(correct_positions)

    # Calculate GNPB
    gnpb, group_npbs = calculate_gnpb(correct_positions)

    return {
        "File": file_path,
        "NPB": npb,
        "Entropy": entropy,
        "Bias Score": bias_score,
        "Probabilities": probabilities,
        "GNPB": gnpb,
        "Group NPBs": group_npbs,
    }

# List of CSV files to process
csv_files = [

]

# Process each CSV file
results = []
for file in csv_files:
    results.append(process_csv(file))

# Display results
for result in results:
    print(f"File: {result['File']}")
    print(f"  NPB: {result['NPB']:.4f}")
    print(f"  Entropy: {result['Entropy']:.4f}")
    print(f"  Bias Score: {result['Bias Score']:.4f}")
    print(f"  Probabilities: {result['Probabilities']}")
    print(f"  GNPB: {result['GNPB']:.4f}")
    print(f"  Group NPBs: {result['Group NPBs']}")
    print()
