from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

from . import db_session
from .users import User

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=False)
parser.add_argument('end_date', required=True)
parser.add_argument('is_finished', required=True)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users':
                            [item.to_dict(rules=('-jobs', '-jobs.user')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args['email']).first()
        if user:
            abort(418, message=f"User {args['email']} is already exist")
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            modified_date=args['modified_date']
        )
        user.set_password(user.hashed_password)
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(rules=('-jobs', '-jobs.user'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
