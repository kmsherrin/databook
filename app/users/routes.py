from flask import Blueprint
from flask import render_template, url_for, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from app.users.utils import send_reset_email, save_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. A user account is not associated with that email address', 'danger')

    return render_template('login.html', title='Login', form=form)
 
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 5, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(user=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=per_page, page=page)

    return render_template('user_posts.html', title=f'{username} Posts', posts=posts, user=user)


@users.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with a link to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired password reset token!', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f'Your password has been updated! Please login with your updated credentials', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@users.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    elif action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    #return redirect(request.referrer)
    return {"result": True}

