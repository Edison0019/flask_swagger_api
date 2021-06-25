# from flask import Flask, jsonify
from flask import jsonify, request
from flask_restx import Resource, Api, fields
from application import app, db
from application.models import User
from application.serializers import UserSchema


api = Api(app)

insert_model = api.model(
    'post',
    {
        'name': fields.String('enter name'),
        'email': fields.String('enter email'),
        'password' : fields.String('enter password')
    }
)

delete_model = api.model('delete',{'id':fields.Integer('enter the ID of the record')})

update_model = api.model(
    'update',
    {
        'id': fields.Integer('enter user id'),
        'name': fields.String('enter name'),
        'email': fields.String('enter email'),
        'password' : fields.String('enter password')
    }
)


@api.route('/users')
class HelloWorld(Resource):
    def get(self):
        try:
            user = User.query.all()
        except:
            return {'response': 'could not execute query'}
        schema = UserSchema(many=True)
        return jsonify(schema.dump(user))
    
    @api.expect(insert_model)
    def post(self):
        try:
            # saving the response from the post action
            rq = request.json
            new_user = User(name=rq['name'],email=rq['email'],password=rq['password'])
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not create user'}
        return {'response':'user created'}

    @api.expect(delete_model)
    def delete(self):
        try:
            user = User.query.get(request.json['id'])
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not delete user'}
        return {'response':'user removed'}

    @api.expect(update_model)
    def put(self):
        try:
            user = User.query.get(request.json['id'])
            user.name = request.json['name']
            user.email = request.json['email']
            user.password = request.json['password']
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not update user'}
        return {'response':'user updated'}

if __name__ == '__main__':
    app.run(debug=True)