from db import db
from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import os 

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
	
    if user == None:
        flash("Username not found", "message")
        return False
    
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["userId"] = user[1]
            session["csrf_token"] = os.urandom(16).hex()
            flash("Succesfully logged in!", "success_message")
            return True
        
        else:
            flash("Wrong password", "message")
            return False
        
def register(username, password):
    
    flag = True
    if len(username) < 3 or len(username) > 12:
         flash("Username must be between 3 and 12 characters long", "message")
         flag = False
    
    
    if len(password) < 3 or len(password) > 15:
         flash("Password must be between 3 and 15 characters long", "message")
         flag = False
    
    if not flag:
        return False
    
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
        
    except:
        flash("Username already exists", "message")
        return False
    
    
    flash("Account created!", "success_message")
    return True #Tai redirect loginiin

def logout():
    session.pop('username', None)
    session.pop('userId', None)

def user_id():
    return session.get("user_id",0)
