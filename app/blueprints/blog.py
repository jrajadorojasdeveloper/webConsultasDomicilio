from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required
from models import db, Post
from forms import PostForm
from datetime import datetime

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    posts = Post.query.filter_by(visible=True).order_by(Post.fecha_pub.desc()).all()
    return render_template('blog/index.html', posts=posts, now=datetime.now())

@blog_bp.route('/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug, visible=True).first_or_404()
    return render_template('blog/post.html', post=post, now=datetime.now())