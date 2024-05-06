from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTests(TestCase):
    def setUp(self):
        self.user_id = 0
        with app.app_context():
            User.query.delete()

            user = User(first_name="Tracy", middle_name="", last_name="Rera",
                     image_url="https://via.placeholder.com/50")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/users")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('Tracy', html)

    def test_form_adduser(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/users/new")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("<h1>Add User</h1>", html)

    def test_add_user(self):
        with app.app_context():
            with app.test_client() as client:
                d = {"first_name": "Treyer",
                     "middle_name": "",
                     "last_name": "Darell",
                     "image_url": ""}
                resp2 = client.post("/users/new", data=d, follow_redirects=True)
                resp2.get_data(as_text=True)

                resp = client.get("/users", follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("Treyer", html)

    def test_show_user(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get(f"/users/{self.user_id}")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h2>Tracy Rera</h2>', html)

    def test_edit_user(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get(f"/users/{self.user_id}/edit")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("Tracy", html)

    def test_delete_user(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get(f"/users/{self.user_id}/delete")
                db.session.delete(db.get_or_404(User, self.user_id))
                db.session.rollback()
