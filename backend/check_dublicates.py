import json


with open('questions.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)

unique_questions = []
duplicates = []

for question in questions:
    if question['text'] in [q['text'] for q in unique_questions]:
        duplicates.append(question)
    else:
        unique_questions.append(question)

for duplicate in duplicates:
    print(duplicate)


with open('unique_questions.json', 'w', encoding='utf-8') as file:
    json.dump(unique_questions, file, ensure_ascii=False)