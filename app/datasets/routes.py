from flask import Blueprint
from flask import render_template, url_for, flash, render_template, request, abort, redirect
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment, CommentReply, Tag, Dataset, DatasetLocation
from app.datasets.forms import DatasetForm
from app.datasets.utils import upload_file
from sqlalchemy import func
import os

datasets = Blueprint('datasets', __name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "databook"

@datasets.route("/data/new", methods=['GET', 'POST'])
@login_required
def new_dataset():

    if request.method == 'POST':
        print("GELLO FILES")
        print(request.form)
        print(request.files)
        #files = request.getlist('dataset')
        #print('files')
        #print(files)

    form = DatasetForm()
    if form.validate_on_submit():
        print(f'datasets data: {form.datasets}')
        # for files in form.datasets.getlist():
        #     print(filles)

    return render_template('create_dataset.html', title='New Dataset',form=form, legend='New Dataset')


@datasets.route("/data/upload", methods=['POST'])
@login_required
def upload_dataset():
    if request.method == "POST":
        f = request.files['file']
        #print(f)
        f.save(os.path.join('uploads', f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return {"file-upload": True}