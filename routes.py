from app import app
from flask import render_template, request, redirect, session
import usersLogic

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return render_template("main.html", name=username)
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

