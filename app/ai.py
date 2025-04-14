from flask import Blueprint, request, jsonify
import google.generativeai as genai
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
import re, json, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini with API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

ai_bp = Blueprint("ai", __name__)

# Create Blueprint for AI routes
ai_bp = Blueprint('ai', __name__)

# AI Content Generation Route
# AI Content Generation Route
def clean_llm_json(text: str) -> str:
    """
    Removes triple backticks and parses + re-serializes to store clean JSON string
    """
    # Remove triple backticks and markdown language label
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        # Try to parse and re-serialize
        parsed = json.loads(cleaned)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from Gemini output: {e}")

@ai_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_content():
    data = request.get_json()
    business_type = data.get("business_type")
    industry = data.get("industry")

    if not business_type or not industry:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        prompt = f"""
        Generate website content in the following strict JSON format for a {business_type} in the {industry} industry.

        Return ONLY JSON and with thier content here json format is given and return the content in key value format and dont use '''json''' just give in proper json format according to the given bussiness type and industry.

        Format:
        {{
          "title": "Business Website Title",
          "hero": {{
            "headline": "Hero Headline",
            "subheadline": "Hero Subheadline",
          }},
          "about": "About section in 2-3 sentences.",
          "services": [
            "Service One",
            "Service Two",
            "Service Three"
          ]
        }}

        Ensure the response is valid JSON and reflects the business and industry context appropriately.
        """

        response = model.generate_content(prompt)
        generated_text = response.text
        cleaned_text = clean_llm_json(generated_text)


        current_user = get_jwt_identity()
        website_data = {
            "user": current_user,
            "business_type": business_type,
            "industry": industry,
            "content": cleaned_text
        }
        result = mongo.websites_collection.insert_one(website_data)
        website_data["_id"] = str(result.inserted_id)

        return jsonify({
            "msg": "Website content generated successfully.",
            "website": website_data
        }), 200

    except Exception as e:
        print("Error generating content:", str(e))
        return jsonify({"error": f"Error generating content: {str(e)}"}), 500

    


