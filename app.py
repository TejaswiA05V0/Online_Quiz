from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------
# DATABASE MODELS
# ----------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300))
    option1 = db.Column(db.String(200))
    option2 = db.Column(db.String(200))
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    answer = db.Column(db.String(200))


# ----------------------------
# CREATE DATABASE & INSERT QUESTIONS
# ----------------------------

with app.app_context():
    db.create_all()

    # Insert questions only if database is empty
    if Question.query.count() == 0:
        questions = [

            Question(
                question="What is 20% of 150?",
                option1="20",
                option2="25",
                option3="30",
                option4="35",
                answer="30"
            ),

            Question(
                question="Which language is used for web apps?",
                option1="Python",
                option2="Java",
                option3="HTML",
                option4="All of the above",
                answer="All of the above"
            ),

            Question(
                question="Which data structure uses FIFO?",
                option1="Stack",
                option2="Queue",
                option3="Tree",
                option4="Graph",
                answer="Queue"
            ),

            Question(
                question="Which keyword is used to define a function in Python?",
                option1="func",
                option2="define",
                option3="def",
                option4="function",
                answer="def"
            ),

            Question(
                question="What does HTML stand for?",
                option1="Hyper Text Markup Language",
                option2="High Text Machine Language",
                option3="Hyperlink and Text Markup Language",
                option4="Home Tool Markup Language",
                answer="Hyper Text Markup Language"
            ),

            Question(
                question="Which company developed Python?",
                option1="Microsoft",
                option2="Google",
                option3="Python Software Foundation",
                option4="Apple",
                answer="Python Software Foundation"
            ),

            Question(
                question="Which operator is used for exponent in Python?",
                option1="^",
                option2="**",
                option3="*",
                option4="//",
                answer="**"
            ),

            Question(
                question="Which of these is a Python framework?",
                option1="Django",
                option2="Laravel",
                option3="Spring",
                option4="Express",
                answer="Django"
            ),

            Question(
                question="Which SQL command is used to retrieve data?",
                option1="GET",
                option2="SELECT",
                option3="FETCH",
                option4="RETRIEVE",
                answer="SELECT"
            ),

            Question(
                question="What is the output of 5 // 2 in Python?",
                option1="2.5",
                option2="3",
                option3="2",
                option4="1",
                answer="2"
            )
        ]

        db.session.bulk_save_objects(questions)
        db.session.commit()


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return "User already exists!"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Credentials!"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "user" not in session:
        return redirect("/login")

    questions = Question.query.all()

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.form.get(str(q.id))
            if selected == q.answer:
                score += 1

        total = len(questions)
        percentage = (score / total) * 100

        # Performance message logic
        if percentage >= 80:
            message = "Excellent 🎉"
        elif percentage >= 50:
            message = "Good 👍"
        else:
            message = "Try Again 💪"

        return render_template(
            "result.html",
            score=score,
            total=total,
            message=message
        )

    return render_template("quiz.html", questions=questions)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ----------------------------
# RUN APPLICATION
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)