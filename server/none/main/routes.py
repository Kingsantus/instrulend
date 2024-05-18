from flask import Blueprint, render_template, request
from app.models import Post, Review, Expirence
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(10).all()
    experiences = Expirence.query.filter(Expirence.star_rating >= 4).order_by(Expirence.star_rating.desc()).limit(10).all()
    return render_template('index.html', posts=posts, experiences=experiences)

@main.route("/about")
def about():
    return render_template('about.html', title='About Us')


@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5)
    reviews = Review.query.all()
    post_review_counts = {}

    for post in posts:
        review_count = Review.query.filter_by(author_id=post.author.id).count()
        post_review_counts[post.id] = review_count
    return render_template('home.html', posts=posts, reviews=reviews, post_review_counts=post_review_counts, page=page)
