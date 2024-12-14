from exts import db
from app import app
from models import User, Organization

with app.app_context():
    # db.drop_all()
    # db.create_all()
    Organization.init_db()
    User.init_db()

