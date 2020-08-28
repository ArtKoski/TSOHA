from app import app
from flask import render_template, request, redirect, session, g
import users_logic, exercises_logic


@app.route("/*")
def reroute():
    return redirect("/")

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        
        try:
            limit = request.args["limit"]
        except:
            limit = 30
        
        tracked_exercises = exercises_logic.get_exerciseVariables_list(limit)
        
        if tracked_exercises == None:
            return redirect("/exercises") 
        else:
            return render_template("main.html", name=username, trackedExercises=tracked_exercises)
    else:
            return render_template("main.html")
        
@app.before_request
def get_current_user():
    g.user = None
    user_id = session.get('userId')
    if user_id is not None:
        g.user = user_id

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


#Add exercise to exercise bank
@app.route("/exercises/add", methods=["post"])
def add_exercise():
    exercise = request.form["added_exercise"]
    exercises_logic.add_exercise(exercise)
    return redirect("/exercises")
    
    
@app.route("/exercises", methods=["get"])
def exercises():
    try:
        search_term = request.args["search"]
        exercises_list = exercises_logic.search_exercise_bank(search_term)
    except:
        exercises_list = exercises_logic.get_exercise_list()
        
    tracked_exercises_list = exercises_logic.get_tracked_list()    
    return render_template("exercises.html", exercises=exercises_list, tracked_exercises=tracked_exercises_list)

@app.route("/exercises/track", methods=["post"])
def track_exercise():
    ex_id = request.form["exercise_id"]
    exercises_logic.track_exercise(ex_id)
    return redirect("/exercises")
   
    
@app.route("/exercises/untrack", methods=["post"])
def untrack_exercise():
    ex_id = request.form["exercise_id"]
    exercises_logic.untrack_exercise(ex_id)
    return redirect("/exercises")    

@app.route("/workout/save", methods=["post"])
def save_workout():
    check_csrf(request.form["csrf_token"])
    
    exercise = request.form["exercise"]
    sets = request.form["sets"]
    reps = request.form["reps"]
    weight = request.form["weight"]
    info = request.form["info"]
    
    exercises_logic.save_workout(exercise, sets, reps, weight, info)
    return redirect("/") 
        

        

@app.route("/workout/edit", methods=["post"])
def edit_workout():
    check_csrf(request.form["csrf_token"])
    
    ex_var_id = request.form["exercise_variable_id"]
    sets = request.form["sets"]
    reps = request.form["reps"]
    weight = request.form["weight"]
    info = request.form["info"]
    
    exercises_logic.edit_workout(ex_var_id, sets, reps, weight, info)
    return redirect("/")
    
@app.route("/workout/delete", methods=["post"])
def delete_workout():
    ex_var_id = request.form["exercise_variable_id"]
    
    exercises_logic.delete_workout(ex_var_id)
    return redirect("/")
    
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def check_csrf(token):
     if session["csrf_token"] != token:
        abort(403)