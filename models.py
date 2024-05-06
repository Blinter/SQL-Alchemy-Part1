"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False)

    middle_name = db.Column(db.String(50),
                            nullable=True)

    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(db.String(255),
                          nullable=False,
                          default='https://via.placeholder.com/30')

    def get_full_name(self):
        return self.first_name + \
        (" " + self.middle_name if len(self.middle_name) > 0 else "") + \
         " " + self.last_name

    @property
    def full_name(self):
        return self.get_full_name()

    def __repr__(self):
        """Show info about user."""

        return (f"<User ID={self.id} " +
                f"First Name={self.first_name} " +
                (f"Middle Name={self.middle_name} " if len(self.middle_name)
                 > 0 else "") +
                f"Last Name={self.last_name} " +
                f"Image URL={self.image_url}>")
