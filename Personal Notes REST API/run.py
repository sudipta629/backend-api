from flask import Flask
from config import Config
from extensions import db
from routes import notes_bp

app = Flask(__name__)
app.config.from_object(Config)

# ডেটাবেজ ইনিশিয়ালাইজ করা
db.init_app(app)

# ব্লুপ্রিন্ট রেজিস্টার করা
app.register_blueprint(notes_bp)

# ডেটাবেজ টেবিল তৈরি করা
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
