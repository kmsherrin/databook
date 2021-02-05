"""
Main routes file, this only contains the route for the homepage
Included is the various filtering for the posts with which how they are
pulled from the db 
"""

from flask import Blueprint
from flask import render_template, request, Response
from app.models import Post, Like
from sqlalchemy import func, cast, Date
import datetime

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    
    # The request params passed into the url as queries
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 5, type=int)
    
    post_type = request.args.get('type', 'top', type=str)
    time = request.args.get('time', 'week', type=str)

    # Determing the time difference. This could probably be refactored into a dictionary + function 
    if time == 'now':
        td = (datetime.datetime.now() - datetime.timedelta(hours=1))
    elif time == 'today':
        td = (datetime.datetime.now() - datetime.timedelta(hours=24))
    elif time == 'week':
        td = (datetime.datetime.now() - datetime.timedelta(days=7))
    elif time == 'month':
        td = (datetime.datetime.now() - datetime.timedelta(days=30))
    elif time == 'all time':
        td = (datetime.datetime.now() - datetime.timedelta(days=10000))

    
    # Get the posts depending on the type of sorting used, i.e. most popular or newest
    if post_type == 'top':
        posts = Post.query.filter(func.date(Post.date_posted) >= td).join(Like).order_by(func.count(Like.post_id).desc(), Post.date_posted.desc()).group_by(Post.id).paginate(per_page=per_page, page=page)
        page_header = "Top Posts"
        post_type = 'top'    
    elif post_type == 'newest': 
        posts = Post.query.filter(func.date(Post.date_posted) >= td).order_by(Post.date_posted.desc()).paginate(per_page=per_page, page=page)
        page_header = "Newest Posts"
        post_type = 'newest'
    else:
        posts = Post.query.filter(func.date(Post.date_posted) >= td).join(Like).order_by(func.count(Like.post_id).desc(), Post.date_posted.desc()).group_by(Post.id).paginate(per_page=per_page, page=page)
        page_header = "Top Posts"   

    # Send response
    resp = Response(render_template('home.html', title='Home', posts=posts, page_header=page_header, time=time.capitalize(), type=post_type))
    resp.cache_control.public = True 
    resp.cache_control.max_age = 10 
    resp.cache_control.immutable = True
    resp.cache_control.no_store = True

    return resp



