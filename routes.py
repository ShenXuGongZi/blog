from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Post
from forms import LoginForm, PostForm, ChangePasswordForm
import markdown
import os

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        flash('无效的用户名或密码')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_image(image):
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.root_path, 'static', 'images', filename)
        image.save(image_path)
        return filename
    return None

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            image_filename = save_image(form.image.data)
        post = Post(title=form.title.data, content=form.content.data, image_filename=image_filename)
        db.session.add(post)
        db.session.commit()
        flash('文章创建成功！')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image.data:
            post.image_filename = save_image(form.image.data)
        db.session.commit()
        flash('文章更新成功！')
        return redirect(url_for('view_post', id=post.id))
    return render_template('edit_post.html', form=form, post=post)

@app.route('/post/<int:id>')
def view_post(id):
    post = Post.query.get_or_404(id)
    content = markdown.markdown(post.content, extensions=['fenced_code', 'tables'])
    return render_template('post.html', post=post, content=content)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('密码已成功修改')
            return redirect(url_for('index'))
        else:
            flash('旧密码不正确')
    return render_template('change_password.html', form=form)

@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'msg': 'No file part'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'msg': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.root_path, 'static', 'images', filename)
        file.save(file_path)
        url = url_for('static', filename=f'images/{filename}')
        return jsonify({'success': True, 'url': url, 'filename': filename})
    
    return jsonify({'success': False, 'msg': 'File type not allowed'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已成功删除！')
    return redirect(url_for('index'))
