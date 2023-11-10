from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    roll_number = db.Column(db.String(10), unique = True, nullable = False)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(35))

    def __repr__(self):
        return f"{self.student_id}-{self.first_name} {self.last_name}"

class course(db.Model):
    course_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    course_code = db.Column(db.String(10), unique = True, nullable = False)
    course_name = db.Column(db.String(30), nullable = False)
    course_description = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.course_id}-{self.course_code} {self.course_name}"

class enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

 # Define the relationships
    student = db.relationship('student', backref='enrollments')
    course = db.relationship('course', backref='enrollments')

    def __repr__(self):
        return f"{self.enrollment_id}-{self.estudent_id} {self.ecourse_id}"


num_rows = db.session.query(student).count()
print(num_rows)

@app.route("/", methods = ['GET', 'POST'])
def hello():
    try:
        if request.method == 'POST':
            r_no = request.form['roll']
            f_nm = request.form['f_name']
            l_nm = request.form['l_name']

            courses_selected = request.form.getlist('courses')

            stu = student(roll_number = r_no, first_name = f_nm, last_name = l_nm)
            db.session.add(stu)
            db.session.commit()

            for course_value in courses_selected:
                course_id = int(course_value.split('_')[1])  
                enrollment = enrollments(estudent_id=stu.student_id, ecourse_id=course_id)
                db.session.add(enrollment)
                db.session.commit()

        allstu = student.query.all()
        return render_template('index.html', num_rows=num_rows, allstu=allstu)
    except: return render_template('existing.html')

@app.route("/student/create", methods = ['GET', 'POST'])
def add_student():
    return render_template('add_stu.html')



@app.route('/delete/<int:student_id>')
def delete(student_id):
    stu = student.query.filter_by(student_id=student_id).first()
    enrollments_to_delete = enrollments.query.filter_by(estudent_id=student_id).all()
    for enrollment in enrollments_to_delete:
        db.session.delete(enrollment)
    db.session.delete(stu)
    db.session.commit()
    return redirect("/")

@app.route('/student/<int:student_id>/update', methods = ['GET', 'POST'])
def update(student_id):
    if request.method == "POST":
        courses_selected = request.form.getlist('courses')
        f_nm = request.form['f_name']
        l_nm = request.form['l_name'] 
        stu = student.query.filter_by(student_id=student_id).first()
        stu.first_name = f_nm
        stu.last_name = l_nm
        for course_value in courses_selected:
            course_id = int(course_value.split('_')[1])  # Extract course ID from the value
            enrollment = enrollments(estudent_id=stu.student_id, ecourse_id=course_id)
            db.session.add(enrollment)
        db.session.add(stu)
        db.session.commit()
        return redirect("/")
    stu = student.query.filter_by(student_id=student_id).first()
    return render_template('update.html', stu=stu)


@app.route("/student/<int:student_id>")
def rno_click(student_id):
    stud = student.query.get(student_id)
    courses_enrolled = stud.enrollments
    stu = student.query.filter_by(student_id=student_id).first()
    return render_template('r_no_clickable.html', stu = stu, courses_enrolled=courses_enrolled)





if __name__ == "__main__":
    app.run(debug=True)

# git check
