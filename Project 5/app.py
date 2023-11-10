from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///week7_database.sqlite3"
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

# db.create_all()
# student.query.delete()
# course.query.delete()
# enrollments.query.delete()
# db.session.commit()

num_rows = db.session.query(student).count()
# print(num_rows)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        r_no = request.form['roll']
        f_nm = request.form['f_name']
        l_nm = request.form['l_name']

        courses_selected = request.form.getlist('courses')

        try:
            stu = student(roll_number=r_no, first_name=f_nm, last_name=l_nm)
            db.session.add(stu)
            db.session.commit()

            for course_value in courses_selected:
                course_id = int(course_value)  # No need to split here
                enrollment = enrollments(estudent_id=stu.student_id, ecourse_id=course_id)
                db.session.add(enrollment)
                db.session.commit()

            return redirect("/")  
        except Exception as e:
            db.session.rollback()  
            print(str(e))  
            return render_template('existing.html')

    allstu = student.query.all()
    return render_template('index.html', num_rows=num_rows, allstu=allstu)


@app.route("/student/create", methods = ['GET', 'POST'])
def add_student():
    all_crs = course.query.all()
    return render_template('add_stu_copy.html', all_crs=all_crs)



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
        enrollments_to_delete = enrollments.query.filter_by(estudent_id=student_id).all()
        for enrollment in enrollments_to_delete:
            db.session.delete(enrollment)
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


@app.route("/courses", methods = ['GET', 'POST'])
def course_details():
    try:
        if request.method == "POST":
            crs_code = request.form['code']
            crs_name = request.form['c_name']
            crs_desc = request.form['desc']
            crs = course(course_code = crs_code, course_name = crs_name, course_description = crs_desc)
            db.session.add(crs)
            db.session.commit()
        all_courses = course.query.all()
        
        return render_template('all_courses.html', all_courses=all_courses)
    except: return render_template('existing_course.html')
@app.route("/course/create", methods = ['GET', 'POST'])
def add_course():
    
    return render_template("add_course.html")

@app.route("/course/<int:course_id>")
def crs_code_click(course_id):
    course_get = course.query.get(course_id)
    courses_enrolled = course_get.enrollments
    crs = course.query.filter_by(course_id=course_id).first()
    return render_template('course_code_clickable.html', crs = crs, courses_enrolled=courses_enrolled)

@app.route('/course/<int:course_id>/update', methods = ['GET', 'POST'])
def course_update(course_id):
    if request.method == "POST":
        courses_selected = request.form.getlist('courses')
        # c_code = request.form['code']
        c_name = request.form['c_name'] 
        c_desc = request.form['desc']
        crs = course.query.filter_by(course_id=course_id).first()
        # crs.course_code = c_code
        crs.course_name = c_name
        crs.course_description = c_desc
        db.session.add(crs)
        db.session.commit()
        return redirect("/")
    crs = course.query.filter_by(course_id=course_id).first()
    return render_template('course_update.html', crs=crs)

@app.route("/course/<int:course_id>/delete")
def course_delete(course_id):
    crs = course.query.filter_by(course_id = course_id).first()
    enrollments_to_delete = enrollments.query.filter_by(ecourse_id=course_id).all()
    for enrollment in enrollments_to_delete:
        db.session.delete(enrollment)
    db.session.delete(crs)
    db.session.commit()
    return redirect("/")











if __name__ == "__main__":
    app.run(debug=True)

