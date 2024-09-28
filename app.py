import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your OpenAI API key here or use an environment variable
import os
import openai

openai.api_key = os.getenv("Key")

def parse_nutrition_info(info):
    nutrition_data = {
        "calories": "N/A",
        "carbs": "N/A",
        "proteins": "N/A",
        "fats": "N/A"
    }
    for line in info.split('\n'):
        if 'Calories' in line:
            nutrition_data['calories'] = line.split(': ')[1]
        elif 'Carbs' in line:
            nutrition_data['carbs'] = line.split(': ')[1]
        elif 'Proteins' in line:
            nutrition_data['proteins'] = line.split(': ')[1]
        elif 'Fats' in line:
            nutrition_data['fats'] = line.split(': ')[1]
    return nutrition_data


@app.route('/calculate', methods=['POST'])
def calculate_nutrition():
    try:
        data = request.get_json()
        food_input = data.get('foodInput', '')

        if not food_input:
            return jsonify({"success": False, "message": "No food items provided."})

        client = OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nutrition expert."},
                {"role": "user", "content": f"Calculate the total calories, carbs, proteins, and fats for the following food items: {food_input}."}
            ]
        )

        nutrition_info = response['choices'][0]['message']['content']
        nutrition_data = parse_nutrition_info(nutrition_info)

        return jsonify({"success": True, "nutrition": nutrition_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Failed to fetch nutrition data.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)