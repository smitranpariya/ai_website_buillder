from flask import Blueprint, render_template, abort
from app import mongo
from bson import ObjectId
import json


preview_bp = Blueprint('preview', __name__)

@preview_bp.route('/preview/<string:website_id>', methods=['GET'])
def preview_website(website_id):
    try:
        website = mongo.websites_collection.find_one({"_id": ObjectId(website_id)})
        if not website:
            return abort(404, "Website not found")

        raw_content = website.get("content", "")

        # Remove the markdown code block (```json ... ```)
        if raw_content.strip().startswith("```json"):
            raw_content = raw_content.strip()
            raw_content = raw_content.replace("```json", "", 1)
            raw_content = raw_content.replace("```", "", 1).strip()

        try:
            content = json.loads(raw_content)
        except json.JSONDecodeError as e:
            return abort(500, f"Error decoding content JSON: {str(e)}")

        # ✅ Title
        page_title = content.get("title", "Website Preview")

        # ✅ Hero Section
        hero = content.get("hero", {})
        hero_data = {
            "headline": hero.get("headline", ""),
            "subheadline": hero.get("subheadline", ""),
        }

        # ✅ About Section
        about_description = content.get("about", "")

        # ✅ Services Section
        raw_services = content.get("services", [])
        services = [{"title": s, "icon": "bi bi-check-circle"} for s in raw_services]

        return render_template(
            'preview_templates/index.html',
            page_title=page_title,
            hero=hero_data,
            about_description=about_description,
            services=services
        )

    except Exception as e:
        return abort(500, f"Error: {str(e)}")



