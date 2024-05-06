"""Blogly application."""

from flask import Flask, request, redirect, render_template

from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_part1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET11!"
# debug = DebugToolbarExtension(app)


@app.route("/")
def home():
    """To Fix Later"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """List"""
    user = (User.query.order_by(User.last_name.asc())
            .order_by(User.first_name.asc())
            .all())
    return render_template("user.html", users=user)


@app.route("/users/new")
def add_new_user_form():
    """New User Form"""
    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Add"""
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = str(image_url) if image_url else None
    user = User(first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_apply(user_id):
    """Edit Apply"""
    user = db.get_or_404(User, user_id)
    user.first_name = request.form.get('first_name', None)
    user.middle_name = request.form.get('middle_name', None)
    user.last_name = request.form.get('last_name', None)
    image_url = request.form.get('image_url', False)
    user.image_url = str(image_url) if image_url else None
    user.verified = True
    db.session.commit()
    return redirect(f"/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete"""
    db.session.delete(db.get_or_404(User, user_id))
    db.session.commit()
    return redirect(f"/users")
