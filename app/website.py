from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app import mongo

website_bp = Blueprint('website', __name__)

# Helper to convert ObjectId to string
def serialize_website(website):
    website["_id"] = str(website["_id"])
    return website

# GET all websites for logged-in user
@website_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_websites():
    user_email = get_jwt_identity()
    websites = mongo.websites_collection.find({"user": user_email})
    return jsonify([serialize_website(w) for w in websites]), 200

# GET single website by ID
@website_bp.route('/<website_id>', methods=['GET'])
@jwt_required()
def get_website(website_id):
    user_email = get_jwt_identity()
    website = mongo.websites_collection.find_one({"_id": ObjectId(website_id), "user": user_email})
    if not website:
        return jsonify({"msg": "Website not found"}), 404
    return jsonify(serialize_website(website)), 200

# PUT (update) website content
@website_bp.route('/<website_id>', methods=['PUT'])
@jwt_required()
def update_website(website_id):
    from json import loads, dumps

    user_email = get_jwt_identity()
    updated_data = request.get_json()

    # Fetch website
    website = mongo.websites_collection.find_one({
        "_id": ObjectId(website_id),
        "user": user_email
    })

    if not website:
        return jsonify({"msg": "Website not found or unauthorized"}), 404

    try:
        existing_content = loads(website.get("content", "{}"))  # Parse JSON string to dict
    except Exception as e:
        return jsonify({"msg": "Corrupted content format", "error": str(e)}), 500

    # Define the structure schema (keys user is allowed to update)
    allowed_structure = {
        "title": str,
        "hero": {
            "headline": str,
            "subheadline": str
        },
        "about": str,
        "services": list
    }

    # Function to recursively validate and apply updates
    def validate_and_update(base, updates, schema):
        for key, value in updates.items():
            if key not in schema:
                return False, f"Invalid key: {key}"

            if isinstance(schema[key], dict):
                if not isinstance(value, dict):
                    return False, f"Expected object for '{key}'"
                valid, msg = validate_and_update(base[key], value, schema[key])
                if not valid:
                    return False, msg
            else:
                if not isinstance(value, schema[key]):
                    return False, f"Invalid type for '{key}', expected {schema[key].__name__}"
                base[key] = value
        return True, "OK"

    # Validate and update
    valid, msg = validate_and_update(existing_content, updated_data, allowed_structure)
    if not valid:
        return jsonify({"msg": msg}), 400

    # Save updated content as JSON string again
    updated_json_str = dumps(existing_content, ensure_ascii=False, indent=2)

    result = mongo.websites_collection.update_one(
        {"_id": ObjectId(website_id), "user": user_email},
        {"$set": {"content": updated_json_str}}
    )

    if result.matched_count == 0:
        return jsonify({"msg": "Unauthorized"}), 403

    return jsonify({"msg": "Content updated successfully"}), 200


# DELETE website
@website_bp.route('/<website_id>', methods=['DELETE'])
@jwt_required()
def delete_website(website_id):
    user_email = get_jwt_identity()

    result = mongo.websites_collection.delete_one({"_id": ObjectId(website_id), "user": user_email})

    if result.deleted_count == 0:
        return jsonify({"msg": "Website not found or unauthorized"}), 404

    return jsonify({"msg": "Website deleted successfully"}), 200