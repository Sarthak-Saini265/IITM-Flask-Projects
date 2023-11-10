from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import matplotlib
matplotlib.use("Agg")  # Use the "Agg" backend for non-interactive image generation
import matplotlib.pyplot as plt
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///marks.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class st_marks(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Artificial primary key
    cr_id = db.Column(db.Integer, nullable=False)
    st_id = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.st_id} - {self.cr_id} - {self.marks}"

l = []
data = open('data.csv', 'r')
for i in data:\
    l.append(i.split())
del l[0]
for i in l:
    for j in range(len(i)-1):
        i[j] = i[j].replace(',', '')
for i in l:
    for j in range(len(i)):
        i[j] = int(i[j])

    final_list = l

ids = []
for i in final_list:
    ids.append(i[0])
    ids.append(i[1])

s_id = []
for i in final_list:
    s_id.append(i[0])

@app.route("/", methods=['GET', 'POST'])
def hello():
    if not st_marks.query.first():
        for i in final_list:
            mark_add = st_marks(cr_id=i[1], st_id=i[0], marks=i[-1])
            db.session.add(mark_add)
            db.session.commit()
    selected_option = request.form.get("option")
    text_box = request.form.get("id_value")

    return render_template('index.html', selected_option=selected_option, text_box=text_box)

# @app.route("/clear-data", methods=['GET', 'POST'])
# def clear_data():
#     with app.app_context():
#         # Delete all records from the st_marks table
#         db.session.query(st_marks).delete()
#         db.session.commit()
#     return "All data has been cleared from the st_marks table."


@app.route("/show", methods=['GET', 'POST'])
def student_id():
    text_box = request.form.get("id_value")
    allmarks = st_marks.query.all()
    # print(allmarks)
    selected_option = request.form.get("option")
    if selected_option not in ["student_id", "course_id"] or text_box == '' or int(text_box) not in ids:
        return render_template('error.html')
    else:
        try:
            if selected_option == "student_id" and int(text_box) in s_id:
                stu_marks = []
                for i in final_list:
                    if i[0] == int(text_box):
                        stu_marks.append(i[-1])
                summation = sum(stu_marks)
                return render_template('stu_details.html', allmarks=allmarks, text_box=text_box, summation=summation)
            elif selected_option == "course_id":
                crs_marks = []
                for i in final_list:
                    if i[1] == int(text_box):
                        crs_marks.append(i[-1])
                # print(crs_marks)
                maximum = max(crs_marks)
                average = sum(crs_marks)/len(crs_marks)
                graph_list = []
                for i in final_list:
                    if i[1] == int(text_box):
                        graph_list.append(i[-1])

                mark_frequency = {}
                for mark in graph_list:
                    if mark in mark_frequency:
                        mark_frequency[mark] += 1
                    else:
                        mark_frequency[mark] = 1
                plt.bar(list(mark_frequency.keys()), list(mark_frequency.values()), width=7, color = 'blue')
                plt.savefig('static/bar.png')
                return render_template('crs_details.html', allmarks=allmarks, text_box=text_box, maximum=maximum, average=average)
            else:
                return render_template('error.html')
        except: return render_template('error.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
