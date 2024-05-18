from flask import Blueprint, render_template, redirect, abort, request, flash, url_for
from flask_login import login_required, current_user
from .forms import PostForm
from app.models import Post
from app import db
from .utils import post_picture

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    picture_file = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = post_picture(form.picture.data)
            post = Post(
                title=form.title.data,
                description=form.description.data,
                price=form.price.data,
                city=form.city.data,
                category=form.category.data,
                image_file=picture_file,
                author=current_user
            )

        db.session.add(post)
        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, image_file=picture_file, legend='New Post')

@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403)  # HTTP 403 Forbidden

    form = PostForm()
    picture_file = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = post_picture(form.picture.data)
            post.image_file = picture_file
        # Update the post with the new data from the form
        post.title = form.title.data
        post.description = form.description.data
        post.price = form.price.data
        post.city = form.city.data
        post.category = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.home'))
    
    elif request.method == 'GET':
        # Pre-fill the form fields with the current post data
        form.title.data = post.title
        form.description.data = post.description
        form.price.data = int(post.price)
        form.city.data = post.city
        form.category.data = post.category
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', image_file=picture_file)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403)  # HTTP 403 Forbidden
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('main.home'))

