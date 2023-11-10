from pyhtml import *
from jinja2 import Template
import sys
import matplotlib.pyplot as plt

print(sys.argv)

l = []
data = open('data.csv', 'r')
for i in data:
    l.append(i.split())
del l[0]
for i in l:
    for j in range(len(i)-1):
        i[j] = i[j].replace(',','')
for i in l:
    for j in range(len(i)):
        i[j] = int(i[j])

final_list = l

ids = []
for i in final_list:
    ids.append(i[0])
    ids.append(i[1])


if sys.argv[1] not in ['-c', '-s']  or int(sys.argv[-1]) not in ids:
    content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Something went wrong</title>
    </head>
    <body>
        <h1>Wrong Inputs</h1>
        <p>Something went wrong</p>
    </body>
    </html>
    """
    template = Template(content)
    t = template.render()

else:

    
    if sys.argv[1] == '-s':
        st_marks = []
        for i in final_list:
            if i[0] == int(sys.argv[-1]):
                st_marks.append([i[1], i[-1]])
        content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Student Data</title>
        </head>
        <body>
            <div>
                <h1>Student Details</h1>
            </div>
            <div>
                <table border = "1">
                    <thead>
                        <tr>
                            <th>Student Id</th>
                            <th>Course Id</th>
                            <th>Marks</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for rows in stu %}
                            
                        <tr>
                            <td>{{list[-1]}}</td>
                            <td>{{rows[0]}}</td>
                            <td>{{rows[1]}}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        template = Template(content)
        t = template.render(list = sys.argv, stu = st_marks)


    if sys.argv[1] == '-c':
        crs_marks = []
        for i in final_list:
            if i[1] == int(sys.argv[-1]):
                crs_marks.append(i[-1])

        maximum = max(crs_marks)
        average = sum(crs_marks)/len(crs_marks)

        graph_list = []
        for i in final_list:
            if i[1] == int(sys.argv[-1]):
                graph_list.append(i[-1])

        mark_frequency = {}
        for mark in graph_list:
            if mark in mark_frequency:
                mark_frequency[mark] += 1
            else:
                mark_frequency[mark] = 1
        plt.bar(list(mark_frequency.keys()), list(mark_frequency.values()), width=7)
        plt.savefig('bar.png')

        content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Course Data</title>
        </head>
        <body>
            <div>
                <h1>Course Details</h1>
            </div>
            <div>
                <table border = "1">
                    <thead>
                        <tr>
                            <th>Average Marks</th>
                            <th>Maximum Marks</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{avg}}</td>
                            <td>{{max}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div>
                <img src="bar.png" alt="error" height="500", width="600">
            </div>
        </body>
        </html>
        """
        template = Template(content)
        t = template.render(avg = average, max = maximum)



output_file_path = "output.html"
with open(output_file_path, "w") as f:
    f.write(t)
f.close()








