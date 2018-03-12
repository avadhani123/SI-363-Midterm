## Ankita Avadhani##




###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from apiclient.discovery import build
import requests, json
#import ankita_midterm.db


## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'random string that is hard to guess'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:ankita@localhost:aavadhan/364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)

######################################
######## HELPER FXNS (If any) ########
######################################

def get_movie_results(title):
    baseurl = 'http://www.omdbapi.com/?i=tt3896198&apikey=ea7c5baf'
    param_dict = {'t':title}
    response = requests.get(baseurl, params = param_dict).json()
    return(response)


def get_or_create_actor(name, popularity, movie_title):
    actor = db.session.query(Actor).filter_by(name=name).first()
    if actor:
        print(actor)
    else:
        actor = Actor(name=name, popularity=popularity)
        top_movie_id = db.session.query(Movie).filter_by(title=movie_title).first().id
        actor.top_movie_id = top_movie_id
        db.session.add(actor)
        db.session.commit()
        print(actor)

##################
##### MODELS #####
##################
class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    search_term = db.Column(db.String(64))
    def __repr__(self):
        return "Name: {0} \nFavorite Genre: {1} \n\n".format(self.name, self.query)

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    release_date = db.Column(db.String(10))
    description = db.Column(db.String(2000))
    rel = db.relationship('Actor', backref='Movies')
    def __repr__(self):
        return "Movie: {0} \nReleased: {1} \nDescription: {2} \n\n".format(self.title, self.release_date, self.description)
###################
###### FORMS ######
###################
class MovieForm(FlaskForm):
    actor = StringField("Enter your favorite actor! ", validators=[Required(), Length(min=1, max=64)])
    submit = SubmitField()
class MovieForm(FlaskForm):
    title = StringField("Enter the title of a movie to recieve information.",validators=[Required()])
    submit = SubmitField()

    def validate_actor(self, field):
        if len(field.data.split(' ')) < 2:
            raise ValidationError('Actor must have first and last name!')

#######################
###### VIEW FXNS ######
#######################




@app.route('/actors')
def popular_actors():
    return render_template('actors.html', actors=Actor.query.all())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')



# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True, debug=True)
