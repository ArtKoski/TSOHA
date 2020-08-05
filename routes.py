from app import app
from flask import render_template, request, redirect, session
import usersLogic, exercisesLogic

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        trackedExercises = exercisesLogic.get_exerciseVariablesList()
        return render_template("main.html", name=username, trackedExercises=trackedExercises)
    else:
        return render_template("mainNotLogged.html")


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
    if usersLogic.login(username,password):
            return redirect("/")

    else:
        #javascriptiä tai jtn tähän
        return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if usersLogic.register(username,password):
            return redirect("/")
        else:
#ja tähän
            return render_template("error.html",message="Rekisteröinti ei onnistunut")


@app.route("/logout")
def logout():
    usersLogic.logout()
    return redirect("/")


#NÄÄ VARMAAN ERILLEEN SELVYYDEN VUOKSI
@app.route("/addExercise", methods=["post"])
def addExercise():
    exercise = request.form["userAddedExercise"]
    exercisesLogic.addExercise(exercise)
    return redirect("/track")
    
    
@app.route("/track", methods=["get"])
def track():
    listExercises = exercisesLogic.get_list()
    listTrackedExercises = exercisesLogic.get_trackedList()
    return render_template("workout.html", exercises=listExercises, trackedExercises=listTrackedExercises)

@app.route("/trackExercise", methods=["post"])
def trackExercise():
    exercise = request.form["exercise"]
    if exercisesLogic.trackExercise(exercise):
        return redirect("/track")
    else:
        return redirect("/track")   ##JAVASCRIPT?? JOKU POP-UP
    
@app.route("/untrackExercise", methods=["post"])
def untrack():
    exercise = request.form["exercise"]
    if exercisesLogic.untrackExercise(exercise):
        return redirect("/track")
    else:
        print("ei onnistunut")
        return redirect("/track")    
    
@app.route("/saveWorkout", methods=["post"])
def saveWorkout():
    Exercise = request.form["Exercise"]
    Sets = request.form["Sets"]
    Reps = request.form["Reps"]
    Weight = request.form["Weight"]
    Info = request.form["Info"]
    
    exercisesLogic.saveWorkout(Exercise, Sets, Reps, Weight, Info)
    return redirect("/")

@app.route("/searchBank", methods=["get"])
def searchExerciseBank():
    searchTerm = request.args["search"]
    listExercises = exercisesLogic.searchBank(searchTerm)
    listTrackedExercises = exercisesLogic.get_trackedList()
    return render_template("workout.html", exercises=listExercises, trackedExercises=listTrackedExercises)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    