from flask import Blueprint, request, jsonify
from sqlalchemy import false

from extensions import db
from models import Note

# 'notes' নামে একটি ব্লুপ্রিন্ট তৈরি করা হলো
notes_bp = Blueprint('notes', __name__)


# ১. নতুন নোট তৈরি করা
@notes_bp.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and Content are required"}), 400

    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "Note created successfully", "note": new_note.to_dict()}), 201


# ২. সব নোট দেখা
@notes_bp.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes]), 200


# ৩. টাইটেল ও কনটেন্ট দিয়ে সার্চ করা
# টাইটেল ও কনটেন্ট দিয়ে সার্চ করার সঠিক API এন্ডপয়েন্ট
@notes_bp.route('/api/notes/search', methods=['GET'])
def search_notes():
    # URL থেকে সার্চের শব্দটি নেওয়া (যেমন: ?keyword=your_word)
    query_word = request.args.get('keyword', '')

    # যদি ইউজার কোনো শব্দ না লেখে সার্চ করে
    if not query_word:
        return jsonify({"error": "Please provide a keyword to search"}), 400

    # ডেটাবেজে টাইটেল অথবা কনটেন্টের ভেতর শব্দটি খোঁজা
    search_results = Note.query.filter(
        (Note.title.contains(query_word)) | (Note.content.contains(query_word))
    ).all()

    # রেজাল্ট ফেরত দেওয়া
    return jsonify([note.to_dict() for note in search_results]), 200


# ৪. নির্দিষ্ট নোট এডিট করা
@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    if 'title' in data: note.title = data['title']
    if 'content' in data: note.content = data['content']

    db.session.commit()
    return jsonify({"message": "Note updated successfully", "note": note.to_dict()}), 200


# ৫. নোট মুছে ফেলা
@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully"}), 200




@notes_bp.route('/api/notes/<int:note_id>/restore', methods=['PATCH'])
def restore_note(note_id):

    note = Note.query.get_or_404(note_id)

    if not note.is_deleted:
        return {"message": "Note is not in trash"}, 400

    note.is_deleted = false()
    db.session.commit()

    return jsonify({"message": "Note restored successfully"}), 200