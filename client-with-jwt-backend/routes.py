from flask import request, jsonify
from extensions import db, bcrypt
from models import User, Note
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
        identity=str(user.id)
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
        identity=str(user.id)
    )

    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }), 200

@jwt_required()
def create_note():

    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({
            "error": "Title and content are required"
        }), 400

    note = Note(
        title=title,
        content=content,
        user_id=user_id
    )
    db.session.add(note)
    db.session.commit()

    return jsonify({
        "message": "Note created",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content
        }
    }), 201


@jwt_required()
def get_notes():

    user_id = get_jwt_identity()
    page = request.args.get(
        "page",
        1,
        type=int
    )
    per_page = request.args.get(
        "per_page",
        5,
        type=int
    )
    notes = Note.query.filter_by(
        user_id=user_id
    ).paginate(
        page=page,
        per_page=per_page
    )

    return jsonify({
        "notes": [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content
            }
            for note in notes.items
        ],
        "page": notes.page,
        "pages": notes.pages,
        "total": notes.total
    }), 200

@jwt_required()
def get_note(id):

    user_id = get_jwt_identity()
    note = Note.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content
    }), 200

@jwt_required()
def update_note(id):

    user_id = get_jwt_identity()
    note = Note.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    data = request.get_json()
    if "title" in data:
        note.title = data["title"]

    if "content" in data:
        note.content = data["content"]

    db.session.commit()

    return jsonify({
        "message": "Note updated",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content
        }
    }), 200

@jwt_required()
def delete_note(id):

    user_id = get_jwt_identity()
    note = Note.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted"
    }), 200