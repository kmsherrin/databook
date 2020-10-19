from flask import Blueprint
from flask import render_template, request, Response
from app.models import Post, Like
from sqlalchemy import func, cast, Date
import datetime

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 5, type=int)
    
    post_type = request.args.get('type', 'top', type=str)
    time = request.args.get('time', 'week', type=str)

    if time == 'now':
        td = (datetime.datetime.now() - datetime.timedelta(hours=1))
    elif time == 'today':
        td = (datetime.datetime.now() - datetime.timedelta(hours=24))
    elif time == 'week':
        td = (datetime.datetime.now() - datetime.timedelta(days=7))
    elif time == 'month':
        td = (datetime.datetime.now() - datetime.timedelta(days=30))

    if post_type == 'top':
        posts = Post.query.filter(func.date(Post.date_posted) >= td).join(Like).order_by(func.count(Like.post_id).desc(), Post.date_posted.desc()).group_by(Post.id).paginate(per_page=per_page, page=page)
        page_header = "Top Posts"    
    elif post_type == 'newest': 
        posts = Post.query.filter(func.date(Post.date_posted) >= td).order_by(Post.date_posted.desc()).paginate(per_page=per_page, page=page)
        page_header = "Newest Posts"
    else:
        posts = Post.query.filter(func.date(Post.date_posted) >= td).join(Like).order_by(func.count(Like.post_id).desc(), Post.date_posted.desc()).group_by(Post.id).paginate(per_page=per_page, page=page)
        page_header = "Top Posts"   

    resp = Response(render_template('home.html', title='Home', posts=posts, page_header=page_header, time=time.capitalize()))
    resp.cache_control.public = True 
    resp.cache_control.max_age = 10 
    resp.cache_control.immutable = True
    resp.cache_control.no_store = True

    return resp



