from db import db
from flask import redirect, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
	
    if user == None:
        print("username not found")
        return False
    
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            print("correcto")
            session["username"] = username
            return True
        
        else:
            print("wrong password")
            return False
        
def register(username, password):
    try:
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
        
    except:
        return False
    
    return login(username, password) #Tai redirect loginiin

def logout():
    #del session["user_id"]
    session.pop('username', None)

def user_id():
    return session.get("user_id",0)
