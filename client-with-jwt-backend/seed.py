from app import app
from extensions import db, bcrypt
from models import User, Note


with app.app_context():

    db.drop_all()
    db.create_all()

    user = User(
        username="demo",
        password_hash=bcrypt.generate_password_hash(
            "password123"
        ).decode("utf-8")
    )

    db.session.add(user)
    db.session.commit()

    note = Note(
        title="First note",
        content="This is sample data",
        user_id=user.id
    )

    db.session.add(note)
    db.session.commit()

    print("Database seeded!")