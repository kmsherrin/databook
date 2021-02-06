from flask import Blueprint
from flask import render_template, url_for, flash, render_template, request, abort, redirect
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment, CommentReply, Tag
from app.posts.forms import PostForm, CommentForm, CommentReplyForm
from sqlalchemy import func


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():

    for key, value in request.form.items():
        print("key: {0}, value: {1}".format(key, value))

    form = PostForm()
    if form.validate_on_submit():

        print(form.data)

        post = Post(title=form.title.data, content=form.content.data, user=current_user, category=form.category.data)
        db.session.add(post)
        db.session.commit()

        for tag in form.tags:
            print(tag)
            tag_entry = Tag(tag=tag.data.strip(), post=post, user=current_user)
            db.session.add(tag_entry)
        db.session.commit()
        
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)

    comment_form = CommentForm()

    comment_reply_form = CommentReplyForm()

    if comment_form.validate():
        comment = Comment(content=comment_form.comment.data, post_id=post.id, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('New comment posted', 'success')
        return redirect(url_for('posts.post', post_id=post_id))

    if comment_reply_form.validate():
        print('posting a comment reply')
        parent_comment_id = comment_reply_form.parent_comment.data
        comment_reply = CommentReply(content=comment_reply_form.content.data, comment_id=parent_comment_id, user=current_user)
        db.session.add(comment_reply)
        db.session.commit()
        flash('Comment reply posted', 'success')
        return redirect(url_for('posts.post', post_id=post_id))

    if post:
        comments = Comment.query.filter_by(post_id=post_id)
        comment_replies = {}
        for comment in comments:
            comment_replies[comment.id] = CommentReply.query.filter_by(comment_id=comment.id)

        print(comment_replies)
        
    return render_template('view_post.html', title=post.title, post=post, comment_form=comment_form, post_editable=True, show_comments=True,
                            comments=comments, comment_reply_form=comment_reply_form, comment_replies=comment_replies)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post',form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/tag/<string:tag>/", methods=['GET'])
@login_required
def tagged_post(tag):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 5, type=int)

    posts = Post.query.join(Tag).filter_by(tag=tag).order_by(Post.date_posted.desc()).paginate(per_page=per_page, page=page)
    post_count = Post.query.join(Tag).filter_by(tag=tag).count()
    number_by_user = Post.query.join(Tag).filter_by(tag=tag).filter_by(user=current_user).count()

    return render_template('tag_posts.html', title=f'{tag} Posts', tag=tag, posts=posts, post_count=post_count, number_by_user=number_by_user)


@posts.route('/post/<int:post_id>/likes')
@login_required
def likes_on_post(post_id):
    post = Post.query.get_or_404(post_id)
    like_number = post.likes.count()

    return {"like_number": like_number}