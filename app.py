from flask import Flask , render_template, request, redirect ,url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def get_db():
    return sqlite3.connect("std.db")

conn = get_db()
cursor =conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS student(
               name TEXT,
               roll INTEGER PRIMARY KEY,
               phy_marks INTEGER,
               math_marks INTEGER,
               stats_marks INTEGER,
               total_marks INTEGER,
               percentage REAL,
               grade TEXT)
""")
conn.commit()
conn.close()

@app.route("/add" , methods=["POST"])
def add_student():
    name = request.form["name"]
    roll = int(request.form["roll"])
    pmarks = int(request.form["pmarks"])
    mmarks = int(request.form["mmarks"])
    smarks = int(request.form["smarks"])
    tmarks = pmarks + mmarks + smarks
    percentage = round((tmarks/300)*100,2)
    
    if percentage >=90:
        grade = "+O"
    elif percentage >=80:
        grade = "O"
    elif percentage >=70:
        grade = "A"
    elif percentage >=60:
        grade = "B"
    elif percentage >=50:
        grade = "C"
    elif percentage >=40:
        grade = "D"
    else:
        grade = "F"


    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO student(name,roll,phy_marks,math_marks,stats_marks,total_marks,percentage,grade) VALUES(?,?,?,?,?,?,?,?)""",
                       (name,roll,pmarks,mmarks,smarks,tmarks,percentage,grade))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "Roll No. Already Exists!!"
    
    conn.close()
    return redirect(url_for("show_students")) 



@app.route("/del", methods=["POST"])
def del_roll():
    roll = int(request.form["roll"])
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE roll=?",(roll,))
    if cursor.rowcount==0:
        conn.close()
        return "Roll No. Not Found!"
    conn.commit()
    conn.close()

    return redirect(url_for("show_students"))

@app.route("/student")
def show_students():
    conn = get_db()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    conn.close()
    return render_template("student.html", students = students)

@app.route("/edit/<int:roll>")
def edit_roll(roll):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE roll=?",(roll,))
    student = cursor.fetchone()
    conn.close()

    if student is None:
        return "Student not found!!"
    
    return render_template("edit.html",s=student)


@app.route("/update/<int:roll>", methods =["POST"])
def update(roll):
    name =request.form["name"]
    roll =int(request.form["roll"])
    pmarks =int(request.form["pmarks"])
    mmarks =int(request.form["mmarks"])
    smarks =int(request.form["smarks"])
    tmarks = pmarks+ mmarks+ smarks
    percentage = round((tmarks/300)*100,2)
    
    if percentage >=90:
        grade = "+O"
    elif percentage >=80:
        grade = "O"
    elif percentage >=70:
        grade = "A"
    elif percentage >=60:
        grade = "B"
    elif percentage >=50:
        grade = "C"
    elif percentage >=40:
        grade = "D"
    else:
        grade = "F"

    conn = get_db()
    cursor =conn.cursor()
    cursor.execute("""UPDATE student
                   SET name = ?,phy_marks=?,math_marks=?,stats_marks=?,total_marks=?,percentage=?,grade=?,
                   WHERE roll=?""",(name,pmarks,mmarks,smarks,tmarks,percentage,grade))
    
    conn.commit()
    conn.close()



if __name__== "__main__":
    app.run()