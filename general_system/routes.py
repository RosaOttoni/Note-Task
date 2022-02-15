"""
home, contacts, users - Associated with the main pages. These functions are statics.
register_login - Associated with pages if the user is not logged in the site.
logout, my_profile, create_posts - Associated with restrict pages. A person just access if it has done the login.

"""

import secrets
import os
from flask import render_template, request, flash, redirect, url_for, abort
from general_system import app, data_base, bcrypt
from general_system.forms import FormCreateAccount, FormLogin, FormEditProfile, FormCreatePost
from general_system.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image


@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route("/contacts")
def contacts():
    return render_template('contacts.html')


@app.route("/users")
@login_required
def users():
    set_users = Usuario.query.all()
    return render_template('users.html', set_users=set_users)


@app.route("/register_login", methods=['GET', 'POST'])
def register_login():
    form_account = FormCreateAccount()
    form_login = FormLogin()

    if form_account.validate_on_submit() and "button_submit_account" in request.form:
        password_encrypted = bcrypt.generate_password_hash(form_account.password.data)
        people = Usuario(username=form_account.username.data, email=form_account.email.data,
                         password=password_encrypted)
        data_base.session.add(people)
        data_base.session.commit()
        flash(f'Cadastro de {form_account.username.data} realizado com sucesso.', 'alert-success')
        return redirect(url_for('home'))

    if form_login.validate_on_submit() and "button_submit_login" in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form_login.password.data):
            login_user(usuario, remember=form_login.remember_password.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')

            # Cath a specific parameter in the url
            # Always that a person non logged try accessing a restrict page, the program redirect to this function
            # Later, the under conditional verify what was the page that the user try to enter.

            next_parameter = request.args.get('next')
            if next_parameter:
                return redirect(next_parameter)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos.', 'alert-danger')

    return render_template('register_login.html', form_account=form_account, form_login=form_login)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Logout realizado com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route("/my_profile")
@login_required
def my_profile():
    image_id = url_for('static', filename='image_id_user/{}'.format(current_user.perf_photo))
    return render_template('my_profile.html', image_id=image_id)


def save_image_profile(image_profile):
    # code of image
    code_img = secrets.token_hex(8)
    # filename = name of the image with the extension
    # separate the name of the extension
    name_img, extension_img = os.path.splitext(image_profile.filename)

    # group name+code+extension
    name_file = name_img + code_img + extension_img

    # complete_path to save file in the images directory
    all_path = os.path.join(app.root_path, 'static/image_id_user', name_file)

    # Reduce the px of image and save image in the directory
    length = (400, 400)
    reduced_image = Image.open(image_profile)
    reduced_image.thumbnail(length)
    reduced_image.save(all_path)

    return name_file


def current_courses(form_profile):
    list_courses = []
    # Add the text from the label field for the courses.
    for field_form in form_profile:
        if 'course_' in field_form.name:
            if field_form.data:
                list_courses.append(field_form.label.text)
    return ';'.join(list_courses)


@app.route("/my_profile/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form_profile = FormEditProfile()
    image_id = url_for('static', filename='image_id_user/{}'.format(current_user.perf_photo))
    # Changing email or username
    if form_profile.validate_on_submit():
        current_user.username = form_profile.username.data
        current_user.email = form_profile.email.data
        if form_profile.photo_profile.data:
            name_file = save_image_profile(form_profile.photo_profile.data)
            current_user.perf_photo = name_file
        current_user.courses = current_courses(form_profile)

        data_base.session.commit()
        flash(f'Edição feita com sucesso!', 'alert-success')
        return redirect(url_for('my_profile'))
    # Automatic fill in the forms.
    elif request.method == 'GET':
        form_profile.username.data = current_user.username
        form_profile.email.data = current_user.email
    return render_template('edit_profile.html', image_id=image_id, form_profile=form_profile)


@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form_post = FormCreatePost()
    if form_post.validate_on_submit():
        post = Post(title=form_post.title.data, bory_text=form_post.bory_text.data, id_user=current_user.id, status=form_post.status.data, date_create=form_post.date.data)
        data_base.session.add(post)
        data_base.session.commit()
        flash(f'Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('create_posts.html', form_post=form_post)


@app.route('/expose_post/<post_id>', methods=['GET', 'POST'])
@login_required
def expose_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_edit_post = FormCreatePost()
        # Automatic fill in the forms.
        if request.method == 'GET':
            form_edit_post.title.data = post.title
            form_edit_post.bory_text.data = post.bory_text
            form_edit_post.date.data = post.date_create
            form_edit_post.status.data = post.status
        # Contrary of the above struct.
        # The user will fill the fields.
        elif form_edit_post.validate_on_submit():
            post.title = form_edit_post.title.data
            post.bory_text = form_edit_post.bory_text.data
            post.date_create = form_edit_post.date.data
            post.status = form_edit_post.status.data
            # Save in the base data.
            data_base.session.commit()
            flash(f'Post editado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form_edit_post = None

    return render_template('expose_post.html', post=post, form_post=form_edit_post)



@app.route('/expose_post/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        data_base.session.delete(post)
        data_base.session.commit()
        flash(f'Post excluido com sucesso', 'alert-warning')
        return redirect(url_for('home'))
    else:
        abort(403)
