from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False


class UserModelTestCase(TestCase):
    """Tests for model for User."""

    def setUp(self):
        """Clean up any existing Users."""

        with app.app_context():
            db.drop_all()
            db.create_all()
            self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_name(self):
        user = User(first_name="Tracy", middle_name="", last_name="Rera",
             image_url="https://via.placeholder.com/50")
        self.assertEqual(user.full_name, "Tracy Rera")
