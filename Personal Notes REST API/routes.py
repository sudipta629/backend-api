from flask import Blueprint, request, jsonify
from pip._internal.utils import hashes
from sqlalchemy import false
from werkzeug.security import generate_password_hash
from extensions import db
from models import Note,User

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/api/notes', methods=['POST'])
def create_note():
    # রিকোয়েস্টের হেডার থেকে ইউজার আইডি নেওয়া হচ্ছে
    user_id = request.headers.get('X-User-ID')

    if not user_id:
        return jsonify({"error": "Unauthorized! Access requires X-User-ID header."}), 401

    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required!"}), 400

    # নির্দিষ্ট ইউজারের আইডির সাথে নোটটি তৈরি করা
    new_note = Note(title=data['title'], content=data['content'], user_id=int(user_id))
    db.session.add(new_note)
    db.session.commit()

    return jsonify({"message": "Note created!", "note": new_note.to_dict()}), 201


@notes_bp.route('/api/notes', methods=['GET'])
def get_notes():
    user_id = request.headers.get('X-User-ID')

    if not user_id:
        return jsonify({"error": "Unauthorized!"}), 401

    # ডেটাবেস থেকে শুধু এই ইউজারের নোটগুলো ফিল্টার করা
    user_notes = Note.query.filter_by(user_id=int(user_id)).all()

    # আপনার তৈরি করা to_dict() মেথড ব্যবহার করে লিস্ট তৈরি
    return jsonify({"notes": [note.to_dict() for note in user_notes]}), 200

@notes_bp.route('/api/notes/search', methods=['GET'])
def search_notes():

    query_word = request.args.get('keyword', '')

    if not query_word:
        return jsonify({"error": "Please provide a keyword to search"}), 400


    search_results = Note.query.filter(
        (Note.title.contains(query_word)) | (Note.content.contains(query_word))
    ).all()

    return jsonify([note.to_dict() for note in search_results]), 200



@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    if 'title' in data: note.title = data['title']
    if 'content' in data: note.content = data['content']

    db.session.commit()
    return jsonify({"message": "Note updated successfully", "note": note.to_dict()}), 200


@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully"}), 200


@notes_bp.route('/notes/trash', methods=['GET'])
def get_trash_notes():

    trash_notes = Note.query.filter_by(is_deleted=True).all()

    output = []
    for note in trash_notes:
        note_data = {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'is_deleted': note.is_deleted
        }
        output.append(note_data)

    return {"trash_notes": output}, 200


@notes_bp.route('/api/notes/<int:note_id>/restore', methods=['PATCH'])
def restore_note(note_id):

    note = Note.query.get_or_404(note_id)

    if not note.is_deleted:
        return {"message": "Note is not in trash"}, 400

    note.is_deleted = false()
    db.session.commit()

    return jsonify({"message": "Note restored successfully"}), 200


@notes_bp.route('/api/register', methods=['PUT'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Please provide username and password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400


    hashed_password = generate_password_hash(data['password'])

    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user_id": new_user.id
    }), 201

