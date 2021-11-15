from re import template
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.service import Service
from flask_app.models.user import User
from flask_app.models.video import Video
from flask_app.models.review import Review

@app.route('/')
def index():
    # this method gets the four most recent reviews
    videos = Video.get_videos_with_recent_reviews()
    return render_template('index.html', videos = videos )
    
@app.route('/view_review/<int:video_id>')
def view_review(video_id):
    video_data = {
        'id' : video_id
    }
    v = Video.get_by_id(video_data)

    #check to see if logged in user has already reviewed this video
    reviewed = False
    for r in v.reviews:
        if r.user_id == session['user_id']:
            reviewed = True

    return render_template('review.html', video = v, reviewed = reviewed)

@app.route('/reviews')
def all_reviews():
    videos = Video.get_all_reviews()
    return render_template('list.html', videos = videos)

@app.route('/write_review')
def write_new_review():
    if 'user_id' not in session:
        redirect('/')
    
    services = Service.get_all();
    return render_template("write.html", services = services)

@app.route('/new_review', methods = ['POST'])
def create_video_review():
    video_data = {
        'category': request.form['category'],
        'title': request.form['title'],
        'img_url': request.form['img_url'],
        'info_url': request.form['info_url'],
        'type': request.form['type'],
        'user_id': session['user_id'],
        'service_id':request.form['service_id']
    }
    video_id = Video.create_video(video_data)

    review_data = {
        'user_id': session['user_id'],
        'video_id': video_id,
        'rating': request.form['rating'],
        'comments': request.form['comments']
    }
    Review.create_review(review_data)

    return redirect('/')

@app.route('/add_review/<int:video_id>')
def add_review(video_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': video_id
    }
    v = Video.get_by_id(data)
    return render_template('add_review.html', video = v)

@app.route('/add_review', methods = ['POST'])
def create_review():

    review_data = {
        'user_id': session['user_id'],
        'video_id': request.form['video_id'],
        'rating': request.form['rating'],
        'comments': request.form['comments']
    }
    Review.create_review(review_data)

    return redirect('/view_review/' + request.form['video_id'])

