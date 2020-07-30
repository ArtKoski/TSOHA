from db import db
from flask import redirect, render_template, session


def addExercise(exercise):
    try:
        sql = "INSERT INTO exercises (exercise, popularity) VALUES (:exercise,0)"
        db.session.execute(sql, {"exercise":exercise})
        db.session.commit()
        
    except:
        sql = "ROLLBACK;"
        db.session.execute(sql)
        updateExercise(exercise)
        
def updateExercise(exercise):
        sql = "UPDATE exercises SET popularity = popularity + 1 WHERE exercise=:exercise"
        db.session.execute(sql, {"exercise":exercise})
        db.session.commit()
    
    
def get_list():
    sql = "SELECT exercise FROM exercises ORDER BY popularity DESC"
    result = db.session.execute(sql)
    polls = result.fetchall()
    return polls
    