from flask import Blueprint, request, jsonify
from database import devices_collection
from dotenv import load_dotenv
import pusher, os

load_dotenv()

activation_bp = Blueprint('activation', __name__)

pusher_client = pusher.Pusher(
    app_id=os.getenv("PUSHER_APP_ID"),
    key=os.getenv("PUSHER_KEY"),
    secret=os.getenv("PUSHER_SECRET"),
    cluster=os.getenv("PUSHER_CLUSTER"),
    ssl=True
)

@activation_bp.route('/activate', methods=['POST'])
def activate():
    data = request.json
    device_id = data['device_id']

    # Find device in MongoDB
    device = devices_collection.find_one({"device_id": device_id})
    if not device:
        return jsonify({"success": False, "message": "Device not found"}), 404

    # Send ACTIVATE command via Pusher
    pusher_client.trigger(
        device['pusher_channel'],
        'phantom-command',
        {'command': 'ACTIVATE'}
    )

    # Update device status in MongoDB
    devices_collection.update_one(
        {"device_id": device_id},
        {"$set": {"status": "activated"}}
    )

    return jsonify({"success": True, "message": "Activation command sent!"})


@activation_bp.route('/catch', methods=['POST'])
def catch():
    data = request.json
    device_id = data['device_id']

    # Find device in MongoDB
    device = devices_collection.find_one({"device_id": device_id})
    if not device:
        return jsonify({"success": False, "message": "Device not found"}), 404

    # Send CATCH command via Pusher
    pusher_client.trigger(
        device['pusher_channel'],
        'phantom-command',
        {'command': 'CATCH'}
    )

    return jsonify({"success": True, "message": "Catch command sent!"})