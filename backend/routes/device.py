from flask import Blueprint, request, jsonify
from database import devices_collection

device_bp = Blueprint('device', __name__)

@device_bp.route('/register', methods=['POST'])
def register_device():
    data = request.json

    # Check if device already registered
    existing = devices_collection.find_one({"device_id": data['device_id']})
    if existing:
        # Update pusher channel if device re-registers
        devices_collection.update_one(
            {"device_id": data['device_id']},
            {"$set": {"pusher_channel": data['pusher_channel']}}
        )
        return jsonify({"success": True, "message": "Device updated!"})

    # Register new device
    device = {
        "device_id": data['device_id'],
        "owner_email": data['owner_email'],
        "pusher_channel": data['pusher_channel'],
        "status": "sleeping"
    }
    devices_collection.insert_one(device)

    return jsonify({"success": True, "message": "Device registered successfully!"})

@device_bp.route('/status', methods=['GET'])
def get_status():
    device_id = request.args.get('device_id')
    device = devices_collection.find_one({"device_id": device_id})

    if not device:
        return jsonify({"success": False, "message": "Device not found"}), 404

    return jsonify({"success": True, "status": device['status']})