from models import User, db
from app import app
import sqlalchemy as db2
from sqlalchemy_utils import database_exists, create_database


engine = db2.create_engine('postgresql:///blogly_part1')
if not database_exists(engine.url):
    create_database(engine.url, encoding='SQL_ASCII')
with app.app_context():
    db.drop_all()
    db.create_all()
    users = [
        User(first_name="Alice", middle_name="", last_name="Smith",
             image_url="https://via.placeholder.com/50"),
        User(first_name="Bob", middle_name="", last_name="Johnson",
             image_url="https://via.placeholder.com/50"),
        User(first_name="Trey", middle_name="M", last_name="Dwight",
             image_url="https://via.placeholder.com/50"),
    ]
    for user in users:
        db.session.add(user)
    try:
        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error committing data: {e}")