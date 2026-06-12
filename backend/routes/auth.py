from flask import Blueprint, request, jsonify
from database import users_collection, devices_collection
import os, hashlib

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    # Check if user already exists
    existing = users_collection.find_one({"email": data['email']})
    if existing:
        return jsonify({"success": False, "message": "User already exists"}), 400
    
    # Save new user
    user = {
        "name": data['name'],
        "email": data['email'],
        "password": hash_password(data['password']),
        "backup_email": data['backup_email'],
        "phone": data['phone']
    }
    users_collection.insert_one(user)
    
    return jsonify({"success": True, "message": "User registered successfully!"})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = users_collection.find_one({
        "email": data['email'],
        "password": hash_password(data['password'])
    })
    
    if not user:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    return jsonify({"success": True, "message": "Login successful!", "email": user['email']})