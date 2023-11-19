import re
import os
import json

def extract_qa_pairs(text):
    # Remove markdown bold formatting
    text = re.sub(r'\*\*', '', text)
    text += "\n\n"

    # Define patterns for questions and answers
    q_pattern_1 = r'Q: (.*?)\n\s*A:'
    a_pattern_1 = r'Q:.*?\n\s*A: (.*?)\n\n'
    q_pattern_2 = r'\d+\.\s+(.*?)\n\s+-'
    a_pattern_2 = r'\d+\.\s+.*?\n\s+-\s*(.*?)\n\n'
    q_pattern_3 = r'\d+\.\s+(.*?)\n\s+'
    a_pattern_3 = r'\d+\.\s+.*?\n\s+(.*?)\n\n'

    # Extract questions and answers based on the three formats
    qa_pairs = []
    questions_1 = re.findall(q_pattern_1, text, re.DOTALL)
    answers_1 = re.findall(a_pattern_1, text, re.DOTALL)
    questions_2 = re.findall(q_pattern_2, text, re.DOTALL)
    answers_2 = re.findall(a_pattern_2, text, re.DOTALL)
    questions_3 = re.findall(q_pattern_3, text, re.DOTALL)
    answers_3 = re.findall(a_pattern_3, text, re.DOTALL)

    # show length of each list
    '''print(len(questions_1),len(answers_1),len(questions_2),len(answers_2),len(questions_3),len(answers_3))
    if len(questions_1) != len(answers_1):
        answers_1 = answers_1[1:len(questions_1)+1]
    if len(questions_2) != len(answers_2):
        answers_2 = answers_2[1:len(questions_2)+1]
    if len(questions_3) != len(answers_3):
        answers_3 = answers_3[1:len(questions_3)+1]
    print(len(questions_1),len(answers_1),len(questions_2),len(answers_2),len(questions_3),len(answers_3))
    '''

    # Combine questions and answers
    qa_pairs.extend(zip(questions_1, answers_1))
    if len(questions_1) == 0:
        qa_pairs.extend(zip(questions_2, answers_2))
        if len(questions_2) == 0:
            qa_pairs.extend(zip(questions_3, answers_3))

    # Remove any trailing whitespaces
    qa_pairs = [(q.strip(), a.strip()) for q, a in qa_pairs]

    return qa_pairs

# Example usage

# Get the directory path from user input
#directory = input("Enter the directory path: ")
directory = "d:/dropbox/llm/finetuning3/treatise"

# Function to extract QA pairs from a text file
def extract_qa_pairs_from_file(file_path):
    with open(file_path, 'r', encoding='cp949') as file:
        print(file_path)
        text = file.read()
        qa_pairs = extract_qa_pairs(text)
        #print(qa_pairs)
        return qa_pairs

# List all files in the directory
files = os.listdir(directory)

all_qa_pairs = []

# Process each text file in the directory
for file_name in files:
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory, file_name)
        qa_pairs = extract_qa_pairs_from_file(file_path)
        print(f"QA pairs from {file_name}:")
        print(len(qa_pairs))
        all_qa_pairs.extend(qa_pairs)
        #exit()
        #print()


# write all qa pairs to a file
system_message = "These questions and answers are based on The Treatise on Invertebrate Paleontology, Part O, Trilobita, which is a comprehensive scholarly reference that extensively covers the morphology, classification, and evolutionary history of trilobites, a group of extinct marine arthropods."
with open("d:/dropbox/llm/finetuning3/treatise_qa_pairs.txt", 'w', encoding='utf-8') as file:
    for qa_pair in all_qa_pairs:
        question = qa_pair[0]
        answer = qa_pair[1]
        # escape for json question and answer
        question = question.replace('"', '\\"')
        answer = answer.replace('"', '\\"')

        formatted_text = f'''{{"messages": [{{"role": "system", "content": "{system_message}"}},{{"role": "user", "content": "{question}"}},{{"role": "assistant", "content": "{answer}"}}]}}'''
        file.write(formatted_text+"\n")
        
#qa_pairs = extract_qa_pairs(example_text)

