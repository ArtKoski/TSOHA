from app import app
from flask import render_template, request, redirect, session, flash, g
import users_logic, exercises_logic

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        trackedExercises = exercises_logic.get_exerciseVariablesList()
        if trackedExercises == None:
            return redirect("/track") 
        else:
            return render_template("main.html", name=username, trackedExercises=trackedExercises)
    else:
            return render_template("main.html")
        

@app.before_request
def get_current_user():
    g.user = None
    userId = session.get('userId')
    if userId is not None:
        g.user = userId

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
    if users_logic.login(username,password):
            return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users_logic.register(username,password):
            return redirect("/login")
        else:
            return render_template("register.html")


@app.route("/logout")
def logout():
    users_logic.logout()
    return redirect("/")


#NÄÄ VARMAAN ERILLEEN SELVYYDEN VUOKSI
@app.route("/addExercise", methods=["post"])
def addExercise():
    exercise = request.form["userAddedExercise"]
    exercises_logic.add_exercise(exercise)
    return redirect("/track")
    
    
@app.route("/track", methods=["get"])
def track():
    listExercises = exercises_logic.get_list()
    listTrackedExercises = exercises_logic.get_trackedList()
    return render_template("workout.html", exercises=listExercises, trackedExercises=listTrackedExercises)

@app.route("/trackExercise", methods=["post"])
def trackExercise():
    exercise = request.form["exercise"]
    if exercises_logic.trackExercise(exercise):
        return redirect("/track")
    else:
        return redirect("/track")   ##JAVASCRIPT?? JOKU POP-UP
    
@app.route("/untrackExercise", methods=["post"])
def untrack():
    exercise = request.form["exercise"]
    if exercises_logic.untrackExercise(exercise):
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
    
    if exercises_logic.saveWorkout(Exercise, Sets, Reps, Weight, Info):  #MISSING: ERROR HANDLING
        return redirect("/") 
        

@app.route("/searchBank", methods=["get"])
def searchExerciseBank():
    searchTerm = request.args["search"]
    listExercises = exercises_logic.searchBank(searchTerm)
    listTrackedExercises = exercises_logic.get_trackedList()
    return render_template("workout.html", exercises=listExercises, trackedExercises=listTrackedExercises)
        

@app.route("/editWorkout", methods=["post"])
def editWorkout():
    ExerciseVariableId = request.form["exerciseVariableId"]
    Sets = request.form["Sets"]
    Reps = request.form["Reps"]
    Weight = request.form["Weight"]
    Info = request.form["Info"]
    
    if exercises_logic.editWorkout(ExerciseVariableId, Sets, Reps, Weight, Info):  #MISSING: ERROR HANDLING
        return redirect("/")
    
@app.route("/deleteWorkout", methods=["post"])
def deleteWorkout():
    Id = request.form["exerciseVariableId"]
    
    if(exercises_logic.deleteWorkout(Id)):
        return redirect("/")
    
    
    
    
    
    
    
    
    
    
    
    
    
    