import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_json(text):

    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    if text.startswith("json"):
        text = text[4:]

    return text.strip()


def generate_recipes(data):

    ingredients = ", ".join(data["ingredients"])

    prompt = f"""
You are an expert chef.

Generate 3 recipes using these ingredients:
{ingredients}

User preferences:
Vegetarian: {data['vegetarian']}
Spicy: {data['spicy']}
Healthy: {data['healthy']}
Difficulty: {data['difficulty']}
Cooking time: {data['time']}

Return ONLY valid JSON in this format:

[
  {{
    "name": "Recipe name",
    "ingredients":[{{"item":"ingredient","quantity":"amount"}}],
    "steps":["step1","step2","step3"],
    "difficulty":"easy/medium/hard",
    "time":"minutes"
  }}
]

Do NOT wrap the JSON in markdown.
Do NOT add explanations.
Do NOT give any line extra other than the recipe format asked for...nothing extra at all...please..
"""

    response = model.generate_content(prompt)

    text = response.text

    cleaned = extract_json(text)

    try:
        return json.loads(cleaned)
    except Exception as e:
        return {"error": "AI returned invalid format", "raw": text}