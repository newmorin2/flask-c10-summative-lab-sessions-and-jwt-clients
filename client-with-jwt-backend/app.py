from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

@app.route("/")
def home():
    return {"message": "Notes API is running!"}

if __name__ == "__main__":
    app.run(debug=True, port=5555)