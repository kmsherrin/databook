"""
Main routes file, this only contains the route for the homepage
Included is the various filtering for the posts with which how they are
pulled from the db 
"""

from flask import Blueprint
from flask import render_template, request, Response
from app.models import Post, Like, Tag, User
from sqlalchemy import func, cast, Date, desc, text
from app.main.forms import SearchForm
import datetime
import time

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    
    # The request params passed into the url as queries
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 5, type=int)
    
    post_type = request.args.get('type', 'top', type=str)
    time_range = request.args.get('time', 'week', type=str)

    # Determing the time difference. This could probably be refactored into a dictionary + function 
    if time_range == 'now':
        td = (datetime.datetime.now() - datetime.timedelta(hours=1))
    elif time_range == 'today':
        td = (datetime.datetime.now() - datetime.timedelta(hours=24))
    elif time_range == 'week':
        td = (datetime.datetime.now() - datetime.timedelta(days=7))
    elif time_range == 'month':
        td = (datetime.datetime.now() - datetime.timedelta(days=30))
    elif time_range == 'all time':
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

    # Get the top tags
    top_tags = Tag.query.with_entities(Tag.tag, func.count(Tag.id).label('freq')).group_by(Tag.tag).order_by(desc(text('freq'))).limit(10)

    #top_users = User.query.with_entities(User.username, func.count(User.posts.likes).label('total_likes')).group_by(User.username).order_by(desc(text('total_likes'))).limit(10)
    #top_users = User.query.filter(User.username, func.count(Like.id).label('total_likes')).select_from(Post).join(Post.user_id).select_from(Like).join(Like.post_id).group_by(User.id).order_by(desc(text('total_likes')))
    #posts = Post.query.filter(func.date(Post.date_posted) >= td).join(Like).order_by(func.count(Like.post_id).desc(), Post.date_posted.desc()).group_by(Post.id).paginate(per_page=per_page, page=page) 
    #top_users = User.query.filter().join(Like, Like.author_id == User.id).group_by(Like.author_id).order_by(func.count(Like.post_id).desc())
    top_users = User.query.with_entities(User, func.count(Like.post_id).label('total_likes')).join(Like, Like.author_id == User.id).group_by(User.id).order_by(desc(text('total_likes'))).limit(5)

    # Send response
    resp = Response(render_template('home.html', title='Home', posts=posts, top_tags=top_tags, top_users=top_users, page_header=page_header, time=time_range.capitalize(), type=post_type))
    resp.cache_control.public = True 
    resp.cache_control.max_age = 10 
    resp.cache_control.immutable = True
    resp.cache_control.no_store = True

    return resp
 

@main.route("/about")
def about():
    return Response(render_template('about.html'))

@main.route("/search")
def search():
    search_term = request.args.get('searchq', '', type=str)

    clean_search_term = search_term

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 5, type=int)

    post_type = request.args.get('type', 'top', type=str)
    time_range = request.args.get('time', 'week', type=str)

    wildcard_prefix = request.args.get('wild-pre', True, type=bool)
    wildcard_suffix = request.args.get('wild-suf', True, type=bool)

    title_search = request.args.get('titleq', True, type=bool)
    content_search = request.args.get('contentq', False, type=bool)
    user_search = request.args.get('userq', False, type=bool)
    tag_search = request.args.get('tagq', False, type=bool)

    if search_term != '':
        if wildcard_prefix:
            search_term = '%' + search_term
        if wildcard_suffix:
            search_term = search_term + '%'

    posts = []
    st = time.time()
    post_count = Post.query.filter(Post.title.like(search_term)).count()

    posts = Post.query.filter(Post.title.like(search_term)).join(Like).order_by(func.count(Like.post_id).desc()).group_by(Post.id).paginate(per_page=per_page, page=page)
    et = time.time()
    query_time = et - st

    return Response(render_template('search.html', title=f"Search: {clean_search_term}", posts=posts, post_count=post_count, query_time=query_time, clean_search_term=clean_search_term))