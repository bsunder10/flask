from social import app, bcypt, db, login_manager
from flask import render_template, url_for, redirect, flash, request, abort
from social.form import LoginForm, RegisterForm, UpdateForm, PasswordForm, UsernameForm, PostForm, FeedbackForm
from social.model import User, Post, Feedback
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os
from PIL import Image
from datetime import datetime


@app.route('/')
def main():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm()
    return render_template('main.html', login_form=login_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return url_for('home')

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            if bcypt.check_password_hash(user.password, password):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Wrong password')
        else:
            flash('No user found with this username')
    return redirect(url_for('main'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        bcrypt_password = bcypt.generate_password_hash(password).decode('utf-8')

        add_user = User(username=username, email=email, password=bcrypt_password)
        db.session.add(add_user)
        db.session.commit()

        flash('Account created for Username {}'.format(form.username.data))

        return redirect(url_for('main'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


def save_pic(pic):
    random_hex = secrets.token_hex(8)
    img_name = current_user.username + ' - ' + random_hex
    _, f_ext = os.path.splitext(pic.filename)
    picture_fn = img_name+f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    img = url_for('static', filename='profile_pics/'+current_user.img_file)
    form = UpdateForm()
    form1 = PasswordForm()
    form2 = UsernameForm()
    if form.submit.data and form.validate():
        if form.pic.data:
            picture_file = save_pic(form.pic.data)
            current_user.img_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Profile has been updated')
        return redirect(url_for('home'))
    if form1.submit1.data and form1.validate():
        if bcypt.check_password_hash(current_user.password, form1.old_password.data):
            current_user.password = bcypt.generate_password_hash(form1.password.data).decode('utf-8')
            db.session.commit()
            flash('Your password has been updated')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Password')
    if form2.username.data != current_user.username:
        if form2.submit2.data and form2.validate():
            if current_user.username != form2.username.data:
                current_user.username = form2.username.data
                db.session.commit()
                flash('Your Profile has been Updated')
                return redirect(url_for('home'))

    if request.method == 'GET':
        form2.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('profile.html', img=img, form=form, form1=form1, form2=form2)


@app.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    pst = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', pst=pst)


@app.route('/post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        u = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(u)
        db.session.commit()
        flash('Your title has been posted')
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form)


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    pst = Post.query.get_or_404(post_id)
    if pst.author != current_user:
        r = 'not user'
    return render_template('post.html', post=pst)


@app.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    form = PostForm()
    pst = Post.query.get_or_404(post_id)
    if pst.author != current_user:
        abort(403)
    if form.validate_on_submit():
        pst.title = form.title.data
        pst.content = form.content.data
        pst.date_posted = datetime.now()
        db.session.commit()
        flash('Your post has been updated')
        return redirect(url_for('home'))
    if request.method == 'GET':
        form.title.data = pst.title
        form.content.data = pst.content
    return render_template('new_post.html', form=form)


@app.route('/post/<int:post_id>/delete')
@login_required
def post_delete(post_id):
    pst = Post.query.get_or_404(post_id)
    if pst.author != current_user:
        abort(403)
    db.session.delete(pst)
    db.session.commit()
    flash('Your post has been deleted')
    return redirect(url_for('home'))


@app.route('/user/<string:user>')
@login_required
def user_post(user):
    page = request.args.get('page', 1, type=int)
    usr = User.query.filter_by(username=user).first_or_404()
    post = Post.query.filter_by(author=usr).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('user_post.html', pst=post)


@app.route('/contact_us', methods=['POST', 'GET'])
@login_required
def contact_us():
    form = FeedbackForm()
    if form.validate_on_submit():
        comm = Feedback(name=current_user.name, email=current_user.email, user_name=current_user.username,
                        user_id=current_user.id, comment=form.comment.data)
        db.session.add(comm)
        db.session.commit()
        return redirect(url_for('home'))
    if request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.name.data = current_user.name

    return render_template('contact_us.html', form=form)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')