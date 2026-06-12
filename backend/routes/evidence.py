from flask import Blueprint, request, jsonify
from database import evidence_collection, devices_collection
import os, json
from datetime import datetime

evidence_bp = Blueprint('evidence', __name__)

# Create folder to store thief photos
os.makedirs("evidence_files", exist_ok=True)

@evidence_bp.route('/upload', methods=['POST'])
def upload_evidence():
    device_id = request.form.get('device_id')
    wifi_data = request.form.get('wifi_data')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if device exists
    device = devices_collection.find_one({"device_id": device_id})
    if not device:
        return jsonify({"success": False, "message": "Device not found"}), 404

    # Save thief photo if provided
    photo_path = None
    if 'photo' in request.files:
        photo = request.files['photo']
        photo_path = f"evidence_files/{device_id}_thief.jpg"
        photo.save(photo_path)

    # Save evidence to MongoDB
    evidence = {
        "device_id": device_id,
        "owner_email": device['owner_email'],
        "photo_path": photo_path,
        "wifi_data": json.loads(wifi_data) if wifi_data else [],
        "timestamp": timestamp
    }
    evidence_collection.insert_one(evidence)

    # Update device status
    devices_collection.update_one(
        {"device_id": device_id},
        {"$set": {"status": "evidence_received"}}
    )

    return jsonify({"success": True, "message": "Evidence uploaded successfully!"})


@evidence_bp.route('/get', methods=['GET'])
def get_evidence():
    device_id = request.args.get('device_id')

    evidence = evidence_collection.find_one(
        {"device_id": device_id},
        {"_id": 0}  # exclude MongoDB _id field
    )

    if not evidence:
        return jsonify({"success": False, "message": "No evidence found"}), 404

    return jsonify({"success": True, "evidence": evidence})