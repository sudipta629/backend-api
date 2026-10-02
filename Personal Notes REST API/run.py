from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ডেটাবেস কনফিগারেশন (SQLite ব্যবহার করা হয়েছে)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ডেটাবেস মডেল (Table Structure)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }


# ডেটাবেস টেবিল তৈরি করার জন্য ফাংশন
with app.app_context():
    db.create_all()


# ১. নতুন নোট তৈরি করা (Create / POST)
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and Content are required!"}), 400

    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()

    return jsonify({"message": "Note created successfully!", "note": new_note.to_dict()}), 201


# ২. সব নোট একসাথে দেখা (Read All / GET)
@app.route('/api/notes', methods=['GET'])
def get_all_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes]), 200


# ৩. নির্দিষ্ট একটি নোট আইডি দিয়ে দেখা (Read One / GET)
@app.route('/api/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get_or_404(id)
    return jsonify(note.to_dict()), 200


# ৪. নোট এডিট বা আপডেট করা (Update / PUT)
@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.get_json()

    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']

    db.session.commit()
    return jsonify({"message": "Note updated successfully!", "note": note.to_dict()}), 200


# ৫. নোট ডিলিট করা (Delete / DELETE)
@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
