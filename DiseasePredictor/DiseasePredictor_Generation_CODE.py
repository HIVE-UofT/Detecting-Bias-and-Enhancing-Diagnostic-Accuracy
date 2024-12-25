import pandas as pd
import random

# Load CSV files
disease_data = pd.read_csv('Source Data.csv')  # Contains "disease" and "Symptom" columns

# Initialize question storage
questions = []

# Loop through symptom count variations
for num_symptoms in range(3, 7):
    # Sequentially use diseases and their symptoms
    for index, row in disease_data.iterrows():
        disease = row['disease']
        symptoms = eval(row['Symptom'])  # Assuming symptoms are stored as a list-like string

        # Skip if there aren't enough symptoms for the current iteration
        if len(symptoms) < num_symptoms:
            continue

        # Select the top `num_symptoms` from the list
        selected_symptoms = symptoms[:num_symptoms]

        # Filter out diseases with overlapping symptoms
        def has_overlapping_symptoms(candidate_symptoms):
            return any(symptom in selected_symptoms for symptom in candidate_symptoms)

        other_diseases = disease_data[disease_data['disease'] != disease]
        valid_distractors = other_diseases[~other_diseases['Symptom'].apply(lambda x: has_overlapping_symptoms(eval(x)))]

        # Skip if not enough valid distractors are available
        if len(valid_distractors) < 3:
            continue

        # Select 3 random valid distractors
        random_distractors = random.sample(valid_distractors['disease'].tolist(), 3)

        # Combine the true disease with distractors
        options = [disease] + random_distractors

        # Generate 4 versions of the question with different answer positions
        for i in range(4):
            shuffled_options = options[:]  # Copy the options list
            random.shuffle(shuffled_options)  # Shuffle options

            # Ensure the correct answer appears in position (i+1)
            correct_option = shuffled_options.pop(shuffled_options.index(disease))
            shuffled_options.insert(i, correct_option)

            # Determine the index of the correct answer
            answer_index = shuffled_options.index(disease) + 1

            # Create the question template
            question_text = (f"A patient is presenting with the following symptoms: "
                             f"{', '.join(selected_symptoms)}. Based on these symptoms, which of the following diseases is the most likely diagnosis?\n"
                             f"1) {shuffled_options[0]} 2) {shuffled_options[1]} 3) {shuffled_options[2]} 4) {shuffled_options[3]}")

            # Store the question details
            questions.append({
                'Question': question_text,
                'Answer Disease': disease,
                'Answer Index': answer_index,
                'Number of Symptoms': num_symptoms
            })

# Convert questions to a DataFrame
questions_df = pd.DataFrame(questions)

# Save to CSV
questions_df.to_csv('5generated_questions.csv', index=False)

print("Questions generated and saved to 'generated_questions.csv'")
