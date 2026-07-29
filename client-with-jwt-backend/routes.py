from flask import request, jsonify
from extensions import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token

def signup():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")
    errors = []

    if not username:
        errors.append("Username is required")

    if not password:
        errors.append("Password is required")

    if password != password_confirmation:
        errors.append("Passwords do not match")

    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:
        errors.append("Username already exists")

    if errors:
        return jsonify({
            "errors": errors
        }), 400

    password_hash = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    user = User(
        username=username,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()
    token = create_access_token(
        identity=user.id
    )

    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 201


def login():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return jsonify({
            "errors": [
                "Invalid username or password"
            ]
        }), 401

    password_valid = bcrypt.check_password_hash(
        user.password_hash,
        password
    )

    if not password_valid:
        return jsonify({
            "errors": [
                "Invalid username or password"
            ]
        }), 401
    token = create_access_token(
        identity=user.id
    )

    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 200