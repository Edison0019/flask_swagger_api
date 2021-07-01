from flask import jsonify, request, session, abort
from flask_restx import Resource, Namespace, fields
from application.models import User, Company, db
from application.serializers import CompanySchema
from helpers.is_authenticated import is_user_authenticated
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

company_schema = CompanySchema(many=True)
api = Namespace('api',description='Test REST API')
login_model = api.model(
    'login_form',
    {
        'email':fields.String('User email'),
        'password':fields.String('Type password')
    }
)
new_user = api.model(
    'new user',
    {
        "name":fields.String("user name"),
        "email":fields.String("user email"),
        "password":fields.String("user password")

    }
)
insert_model = api.model(
    'post',
    {
        'company_name': fields.String('enter name'),
    }
)
delete_model = api.model(
    'delete',
    {
        'company_id': fields.Integer('enter company Id'),
    }
)
update_model = api.model(
    'update',
    {
        'id': fields.Integer('enter user id'),
        'name': fields.String('enter name'),
        'email': fields.String('enter email'),
        'password' : fields.String('enter password')
    }
)
@api.route('/create_user')
class createUser(Resource):
    @api.expect(new_user)
    def post(self):
        rq = request.json
        password = generate_password_hash(
            rq['password'],
            method='sha256',
            salt_length=32
        )
        new_user = User(
            name=rq['name'],
            email=rq['email'],
            password=password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            return {'response':'email already exists, please try another one'}
        return {'response':'user created'}
        
@api.route('/login')
class LoginUser(Resource):
    @api.expect(login_model)
    def post(self):
        r = request.json
        if not r:
            return {'response':'authentication information missing'}
        user = User.query.filter_by(email=r['email']).first()
        if not user or not check_password_hash(user.password, r['password']):
            return {'response':'no user found. please check user/password'}
        # session['user_id'] = user.id
        login_user(user)
        return {'response':'user logged in successfully'}
    @login_required
    def get(self):
        return {'name':current_user.name, 'email':current_user.email}

@api.route('/logout')
class LogoutUser(Resource):
    @login_required
    def get(self):
        # session.pop('user_id')
        logout_user()
        return {'response':'user logged out'}

@api.route('/companies')
class CompanyInformation(Resource):
    @login_required
    def get(self):
        try:
            companies = Company.query.filter_by(user_id=current_user.id)
        except Exception as e:
            print(e)
            return {'response': 'could not execute query'}
        return jsonify(company_schema.dump(companies))
    
    @api.expect(insert_model)
    @login_required
    def post(self):
        try:
            # saving the response from the post action
            rq = request.json
            user =  User.query.get(current_user.id)
            new_company = Company(company_name=rq['company_name'],user=user)
            db.session.add(new_company)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not create company'}
        return {'response':'company created'}

    @login_required
    def delete(self):
        try:
            company = Company.query.get(request.json['company_id'])
            db.session.delete(company)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not delete company'}
        return {'response':'company removed'}

    @login_required
    def put(self):
        try:
            company = Company.query.get(request.json['company_id'])
            if not company:
                return {'response':'no company found with the provided information'}
            company.company_name = request.json['company_name']
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not update company'}
        return {'response':'company updated'}

@api.route('/companies/<int:id>')
class CompanySingle(Resource):
    @login_required
    def get(self,id):
        company = Company.query.filter_by(id=id,user_id=current_user.id)
        if company.count() == 0:
            return abort(404)
        company_schema = CompanySchema()
        return jsonify(company_schema.dump(company[0]))