from marshmallow import Schema

class CompanySchema(Schema):
    class Meta:
        fields = ('id','company_name','user_id','creation_date')