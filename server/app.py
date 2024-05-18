#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

#campers routes
@app.route('/campers')
def get_campers():
    # all_campers = [camper.to_dict() for camper in Camper.query.all()]
    # return all_campers, 200
    campers = []
    for camper in Camper.query.all():
        campers.append({
            "id": camper.id,
            "name": camper.name,
            "age": camper.age
        })
    return campers, 200


@app.route('/campers/<int:id>')
def get_camper(id:int):
    camper = Camper.query.where(Camper.id == id).first()
    if camper:
        return camper.to_dict(), 200
    return {"error": "Camper not found"}, 404


@app.route('/campers', methods=['POST'])
def post_camper():
    try:
        new_camper = Camper(name=request.json['name'], age=request.json['age'])
        db.session.add(new_camper)
        db.session.commit()
        return new_camper.to_dict(), 201
    except ValueError:
        return {"errors": 'Camper post failed'}, 400
    

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id:int):
    camper_to_pdate = Camper.query.where(Camper.id == id).first()

    if not camper_to_pdate:
        return {'error': 'Camper not found'}, 404
    
    else:
        try:
            camper = Camper.query.where(Camper.id == id).first()
            for key in request.json.keys():
                setattr(camper, key, request.json[key])
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(), 202
        except ValueError:
            return {'errors': ['validation errors']}, 400
        
# Activities routes
@app.route('/activities')
def get_activities():
    all_activities = [activity.to_dict() for activity in Activity.query.all()]
    return all_activities, 200


@app.route('/activities/<int:id>')
def get_activity(id:int):
    activity = Activity.query.where(Activity.id == id).first()
    if activity:
        return activity.to_dict(), 200
    return {"error": "Activity not found"}, 404


@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id:int):
    activity = Activity.query.where(Activity.id == id).first()
    if activity:
        db.session.delete(activity)
        db.session.commit()
        return {}, 204
    return {"error": "Activity not found"}, 404

#signups routes
@app.route('/signups', methods=['POST'])
def post_signup():
    try:
        new_signup = Signup(time=request.json['time'], camper_id=request.json['camper_id'], activity_id=request.json['activity_id'])
        db.session.add(new_signup)
        db.session.commit()
        return new_signup.to_dict(), 201
    except ValueError:
        return {"errors": ['validation errors']}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
