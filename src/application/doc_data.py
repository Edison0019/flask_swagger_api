from attr import field
from application import api
from flask_restx import fields

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