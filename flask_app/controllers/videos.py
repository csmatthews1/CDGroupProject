from re import template
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.service import Service
from flask_app.models.user import User
from flask_app.models.video import Video
from flask_app.models.review import Review

@app.route('/video_reviews/<int:video_id>'):
def video_reviews(video_id):
    video_data = {
        'id' : video_id
    }
    v = Video.get_video_with_creator_rating(video_data)
    r = Review.get_all_reviews_for_video(video_data)
    return render_template('review.html', video = v, reviews = r)

@app.route('/all_reviews')
def all_reviews():
    v = Video.get_all_reviews()
    return render_template('list.html', videos = v)

@app.route('/add/Review_page')
def create_video_page():
    if 'user_id' not in session:
        redirect('/')
    return render_template(".html")

@app.route('/create/new_review', methods = ['POST'])
def create_video():
    if 'user_id' not in session:
        redirect('/')
    
    Review.create_review(request.form)
    Service.create_service(request.form)
    Video.create_video(request.form)
    return redirect('/home')

@app.route('/add/my_review/<int:video.id>')
def add_review(video_id):
    if 'user_id' not in session:
        return redirect('/home')
    data = {
        'id': video_id
    }
    v = Video.get_one(data)
    return render_template('add_review.html', video = v)

@app.route('/create/added_review', methods = ['POST'])
def create_review():
    if 'user_id' not in session:
        redirect('/')
    Review.create_review(request.form)
    return redirect('/home')