from flask import Blueprint
from flask import render_template, url_for, flash, render_template, request, abort, redirect
from flask_login import current_user, login_required
from app import db
from app.models import Dataset, DatasetLocation
from app.datasets.forms import DatasetForm
from app.datasets.utils import upload_file
from sqlalchemy import func
import os
import time
import json

datasets = Blueprint('datasets', __name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "databook"

@datasets.route("/data/new", methods=['GET', 'POST'])
@login_required
def new_dataset():

    if request.method == 'POST':
        print(request.form)
        
        #if request.form['dataset_uploaded']:
        #    flash(f'Your dataset has been created!', 'success')
        #    return redirect(url_for('datasets.new_dataset'))
        
        dataset = Dataset(title=request.form['title'], abstract=request.form['abstract'], category=request.form['category'])
        db.session.add(dataset)
        db.session.commit()
    
        return json.dumps({"dataset_id": dataset.id})

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

        dataset_id = request.form['dataset_id']
        #print(f)
        curr_time = time.time()
        f.save(os.path.join('uploads', f'{current_user.id}-{curr_time}-{f.filename}'))
        
        resp = upload_file(f"uploads/{current_user.id}-{curr_time}-{f.filename}", BUCKET)

        dataset_loc = DatasetLocation(href=f'uploads/{current_user.id}-{curr_time}-{f.filename}', name=f.filename, dataset_id=dataset_id)
        db.session.add(dataset_loc)
        db.session.commit()

        os.remove(os.path.join('uploads', f'{current_user.id}-{curr_time}-{f.filename}'))

        return {"dataset_object": dataset_loc.id}