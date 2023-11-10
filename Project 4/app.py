from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///api_database.sqlite3"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    roll_number = db.Column(db.String(10), unique = True, nullable = False)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(35))

    def __repr__(self):
        return f"{self.student_id}-{self.first_name} {self.last_name}"

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    course_code = db.Column(db.String(10), unique = True, nullable = False)
    course_name = db.Column(db.String(30), nullable = False)
    course_description = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.course_id}-{self.course_code} {self.course_name}"

class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

 # Define the relationships
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

    def __repr__(self):
        return f"{self.enrollment_id}-{self.estudent_id} {self.ecourse_id}"


# db.create_all()
# Enrollments.query.delete()
# db.session.commit()

resource_fields = {
  "course_id": fields.Integer,
  "course_name": fields.String,
  "course_code": fields.String,
  "course_description": fields.String,
}

std_resource_fields = {
  "student_id": fields.Integer,
  "first_name": fields.String,
  "last_name": fields.String,
  "roll_number": fields.String,
}

enroll_resource_fields = {
  "enrollment_id": fields.Integer,
  "estudent_id": fields.Integer,
  "ecourse_id": fields.Integer,
}

crs_post_args = reqparse.RequestParser()
crs_post_args.add_argument("course_name", type=str, help = "Course name is required", required = True)
crs_post_args.add_argument("course_code", type=str, help = "Course code is required", required = True)
crs_post_args.add_argument("course_description", type=str, help = "Course description is required", required = True)

crs_update_args = reqparse.RequestParser()
crs_update_args.add_argument("course_name", type=str)
crs_update_args.add_argument("course_code", type=str)
crs_update_args.add_argument("course_description", type=str)


std_post_args = reqparse.RequestParser()
std_post_args.add_argument("first_name", type=str, help = "First name is required", required = True)
std_post_args.add_argument("last_name", type=str, help = "Last name is required", required = True)
std_post_args.add_argument("roll_number", type=str, help = "Roll number is required", required = True)

std_update_args = reqparse.RequestParser()
std_update_args.add_argument("first_name", type=str)
std_update_args.add_argument("last_name", type=str)
std_update_args.add_argument("roll_number", type=str)


enroll_post_args = reqparse.RequestParser()
enroll_post_args.add_argument("ecourse_id", type=int, help = "Course id is required", required = True)

class Crs(Resource):
    @marshal_with(resource_fields)
    def get(self, course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, message = "Course not found")
        return course, 200
    

    def put(self, course_id):
        args = crs_update_args.parse_args()
        put = Course.query.filter_by(course_id=course_id).first()
        if not put:
            abort(404, message = "Course not found")
        if args['course_name']:
            put.course_name = args['course_name']
        if args['course_code']:
            put.course_code = args['course_code']
        if args['course_description']:
            put.course_description = args['course_description']
        db.session.commit()
        return "Successfully updated", 200
    

    def delete(self, course_id):
        delete = Course.query.filter_by(course_id=course_id).first()
        if not delete:
            abort(404, message = "Course not found")
        db.session.delete(delete)
        db.session.commit()
        return "Successfully Deleted", 200

class Post(Resource):    
    @marshal_with(resource_fields)
    def post(self):
        args = crs_post_args.parse_args()
        course_code = args["course_code"]
        post = Course.query.filter_by(course_code=course_code).first()
        if post:
            abort(409, message = "course_code already taken")
        new_course = Course(course_name=args['course_name'], course_code=course_code, course_description=args['course_description'])
        db.session.add(new_course)
        db.session.commit()
        return new_course
        

    def get(self):
        posts = Course.query.all()
        courses = {}
        for post in posts:
            courses[post.course_id] = {'course_name' : post.course_name, 'course_code' : post.course_code, 'course_description' : post.course_description}
        return courses


class Std(Resource):
    @marshal_with(std_resource_fields)
    def get(sef, student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            abort(404, message = "Course not found")
        return student, 200


    def put(self, student_id):
        args = std_update_args.parse_args()
        put = Student.query.filter_by(student_id=student_id).first()
        if not put:
            abort(404, message = "Student not found")
        if args['first_name']:
            put.first_name = args['first_name']
        if args['last_name']:
            put.last_name = args['last_name']
        if args['roll_number']:
            put.roll_number = args['roll_number']
        db.session.commit()
        return "Successfully updated", 200
    

    def delete(self, student_id):
        delete = Student.query.filter_by(student_id=student_id).first()
        if not delete:
            abort(404, message = "Student not found")
        db.session.delete(delete)
        db.session.commit()
        return "Successfully Deleted", 200

class Std_post(Resource):
    @marshal_with(std_resource_fields)
    def post(self):
        args = std_post_args.parse_args()
        roll_number = args["roll_number"]
        post = Student.query.filter_by(roll_number=roll_number).first()
        if post:
            abort(409, message = "Student already exists")
        new_student = Student(first_name=args['first_name'], last_name = args['last_name'], roll_number=roll_number)
        db.session.add(new_student)
        db.session.commit()
        return new_student


    def get(self):
        posts = Student.query.all()
        students = {}
        for post in posts:
            students[post.student_id] = {'first_name' : post.first_name, 'last_name' : post.last_name, 'roll_number' : post.roll_number}
        return students


class Enroll(Resource):
    @marshal_with(enroll_resource_fields)
    def get(self, student_id):
        enroll = Enrollments.query.filter_by(estudent_id=student_id).first()
        if not enroll:
            abort(400, message = "Invalid Student Id")
        return enroll, 200


    @marshal_with(enroll_resource_fields)
    def post(self, student_id):
        args = enroll_post_args.parse_args()
        stu_id = Student.query.filter_by(student_id=student_id).first()
        course_id = args['ecourse_id']
        post = Enrollments.query.filter_by(estudent_id=student_id).first()
        if post:
            abort(400, message = "Bad request")
        if not stu_id:
            abort(404, message = "Student not found")
        print("Captured student_id:", student_id)
        print("Captured course_id:", course_id)
        new_enrollment = Enrollments(estudent_id = student_id, ecourse_id = course_id)
        db.session.add(new_enrollment)
        db.session.commit()
        return new_enrollment


class Enroll_delete(Resource):
    def delete(self, student_id, course_id):
        stu_id = Student.query.filter_by(student_id=student_id).first()
        stu_del = Enrollments.query.filter_by(estudent_id=student_id).first()
        crs_del = Enrollments.query.filter_by(ecourse_id=course_id).first()
        if not stu_del or not crs_del:
            abort(400, message = "Enrollment for the student not found")
        db.session.delete(stu_del)
        db.session.commit()
        return "Successfully Deleted", 200


class Enroll_show_all(Resource):
    def get(self):
        posts = Enrollments.query.all()
        enrollments = {}
        for post in posts:
            enrollments[post.enrollment_id] = {'estudent_id' : post.estudent_id, 'ecourse_id' : post.ecourse_id}
        return enrollments
















api.add_resource(Crs, "/course/<int:course_id>")
api.add_resource(Post, "/course")
api.add_resource(Std, "/student/<int:student_id>")
api.add_resource(Std_post, "/student")
api.add_resource(Enroll, "/student/<int:student_id>/course")
api.add_resource(Enroll_delete, "/student/<int:student_id>/course/<int:course_id>")
api.add_resource(Enroll_show_all, "/enroll")


if __name__ == "__main__":
    app.run(debug=True)

