from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, login


resource_fields_2 = {
    'username' : fields.String,
    'password' : fields.String,
}

acc_post_args = reqparse.RequestParser()
acc_post_args.add_argument("username", type=str, help = "Username is required", required = True, location='form')
acc_post_args.add_argument("password", type=str, help = "Password is required", required = True, location='form')

class new_acc(Resource):
    @marshal_with(resource_fields_2)
    def post(self):
        args = acc_post_args.parse_args()
        new = login(username = args["username"], password = args["password"], acc_type = 'General')
        db.session.add(new)
        db.session.commit()
        return new
    
