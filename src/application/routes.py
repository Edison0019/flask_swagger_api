from flask import jsonify, request, session, abort
from flask_restx import Resource
from application import db, api
from application.models import User, Company
from application.serializers import CompanySchema
from application.doc_data import insert_model
from helpers.encrypt import EncryptPassword

company_schema = CompanySchema(many=True)

@api.route('/login')
class LoginUser(Resource):
    def post(self):
        r = request.json
        if r == None:
            return {'response':'authentication information missing'}
        ep = EncryptPassword(r['password'])
        user = User.query.filter_by(email=r['email'])
        if user.count() != 1:
            return {'response':'no user found. please check user/password'}
        elif ep.encript(user[0].password_salt) != user[0].password:
            return {'response':'no user found. please check user/password'}
        session['user_id'] = user[0].id
        return {'response':'user logged in successfully'}

@api.route('/logout')
class LogoutUser(Resource):
    def get(self):
        if 'user_id' in session:
            session.pop('user_id')
            return {'response':'user logged out successsfully'}
        return {'response':'no user logged in'}

@api.route('/companies')
class CompanyInformation(Resource):
    def get(self):
        if not 'user_id' in session:
            return {'response':'please make sure to log in the system'}
        try:
            companies = Company.query.filter_by(user_id=session['user_id'])
        except:
            return {'response': 'could not execute query'}
        return jsonify(company_schema.dump(companies))
    
    @api.expect(insert_model)
    def post(self):
        try:
            if not 'user_id' in session:
                return {'response':'please make sure to log in the system'}
            # saving the response from the post action
            rq = request.json
            user =  User.query.get(session['user_id'])
            new_company = Company(company_name=rq['company_name'],user=user)
            db.session.add(new_company)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not create company'}
        return {'response':'company created'}

    def delete(self):
        if not 'user_id' in session:
            return {'response':'please make sure to log in the system'}
        try:
            company = Company.query.get(request.json['company_id'])
            db.session.delete(company)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'response':'could not delete company'}
        return {'response':'company removed'}

    def put(self):
        if not 'user_id' in session:
            return {'response':'please make sure to log in the system'}
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
    def get(self,id):
        if not 'user_id' in session:
            return {'response':'please make sure to log in the system'}
        company = Company.query.get(id)
        if not company:
            return abort(404)
        company_schema = CompanySchema()
        return jsonify(company_schema.dump(company))