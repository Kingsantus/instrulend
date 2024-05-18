from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Expirence, Review
from app import db
from .forms import ExpirenceForm, ReviewForm
from app.models import User

reviews = Blueprint('reviews', __name__)

@reviews.route('/expirence/new', methods=['GET', 'POST'])
@login_required
def expirence():
    form = ExpirenceForm()
    if form.validate_on_submit():
        expirence = Expirence(
            star_rating=form.rating.data,
            content=form.content.data,
            author6=current_user
        )
        
        db.session.add(expirence)
        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('expirence.html', title='New Post', form=form, legend='New Post')

@reviews.route('/review/<int:author_id>', methods=['GET', 'POST'])
@login_required
def review(author_id):
    author = User.query.get_or_404(author_id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            star_rating=form.rating.data,
            user_id=current_user.id,
            author_id=author.id,
            content=form.content.data
        )
        
        db.session.add(review)
        db.session.commit()

        flash('Your review has been submitted!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('review.html', title='Review User', form=form, legend='New Review')