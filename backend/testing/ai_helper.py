import environ
import json
from google import genai
from .models import Test, Question

env = environ.Env()

client = genai.Client(api_key=env('GEMINI_API_KEY'))


def generate_test_from_notes(topic):
    notes = topic.notes.all()
    if not notes.exists():
        return None

    notes_text = "\n\n".join(note.content for note in notes)

    prompt = f"""
Based on the following notes about "{topic.name}", generate 10 multiple choice questions.

Notes:
{notes_text}

Return ONLY valid JSON, no extra text, in this exact format:
[
    {{
        "question_text": "...",
        "option_a": "...",
        "option_b": "...",
        "option_c": "...",
        "option_d": "...",
        "correct_option": "A"
    }}
]
"""

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )

    cleaned = response.text.strip().removeprefix('```json').removeprefix('```').removesuffix('```').strip()

    try:
        questions_data = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    test = Test.objects.create(topic=topic, user=topic.user, title=f"{topic.name} — AI generated test")

    for item in questions_data:
        Question.objects.create(
            test=test,
            question_text=item['question_text'],
            option_a=item['option_a'],
            option_b=item['option_b'],
            option_c=item['option_c'],
            option_d=item['option_d'],
            correct_option=item['correct_option'],
        )

    return test