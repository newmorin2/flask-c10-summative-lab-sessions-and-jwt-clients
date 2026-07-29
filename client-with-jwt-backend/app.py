from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
import models
from routes import signup, login, me, create_note, get_notes ,get_note, update_note, delete_note

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

app.add_url_rule(
    "/signup",
    view_func=signup,
    methods=["POST"]
)
app.add_url_rule(
    "/login",
    view_func=login,
    methods=["POST"]
)
app.add_url_rule(
    "/me",
    view_func=me,
    methods=["GET"]
)
app.add_url_rule(
    "/notes",
    view_func=create_note,
    methods=["POST"]
)
app.add_url_rule(
    "/notes",
    view_func=get_notes,
    methods=["GET"]
)
app.add_url_rule(
    "/notes/<int:id>",
    view_func=get_note,
    methods=["GET"]
)
app.add_url_rule(
    "/notes/<int:id>",
    view_func=update_note,
    methods=["PATCH"]
)
app.add_url_rule(
    "/notes/<int:id>",
    view_func=delete_note,
    methods=["DELETE"]
)


@app.route("/")
def home():
    return {"message": "Notes API is running!"}

if __name__ == "__main__":
    app.run(debug=True, port=5555)