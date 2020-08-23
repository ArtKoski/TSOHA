from db import db
from flask import redirect, render_template, session
from datetime import date

def add_exercise(exercise):
    try:
        sql = "INSERT INTO exercises (exercise, popularity) VALUES (:exercise,0)"
        db.session.execute(sql, {"exercise":exercise})
        db.session.commit()
        
    except:
        #TEST THIS
        #sql = "ROLLBACK;"
        #db.session.execute(sql)
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

def get_exercise_id(exercise):
    sql = "SELECT id FROM exercises WHERE exercise=:exercise"
    result = db.session.execute(sql, {"exercise":exercise})
    return result.fetchone()[0]



def get_exercise_name(exerciseId):
    sql = "SELECT exercise FROM exercises WHERE id=:exerciseId"
    result = db.session.execute(sql, {"exerciseId":exerciseId})
    return result.fetchone()[0]

def get_trackedExercise_id(exercise, userId):
    sql = "SELECT tE.id FROM trackedExercises tE, exercises e WHERE e.exercise=:exercise AND tE.exercise_id=e.id AND tE.user_id=:userId"
    result = db.session.execute(sql, {"exercise":exercise, "userId":userId})
    return result.fetchone()[0]

def get_trackedExercise_idByUserAndExercise(userId, exerciseId):
    sql = "SELECT id FROM trackedExercises WHERE exercise_id=:exerciseId AND user_id=:userId"
    result = db.session.execute(sql, {"exerciseId":exerciseId, "userId":userId})
    return result.fetchone()[0]


def trackExercise(exercise):
    userId = session["userId"]
    exerciseId = get_exercise_id(exercise)
        
    if checkForDuplicate(exercise, userId, exerciseId):
        sql  = "UPDATE trackedExercises SET visible = 1 WHERE user_id=:userId AND exercise_id=:exerciseId"
        db.session.execute(sql, {"userId":userId, "exerciseId":exerciseId})
        db.session.commit()
        return False
        
    else:
        sql  = "INSERT INTO trackedExercises (exercise_id, user_id, visible) VALUES (:exerciseId,:userId, 1)"
        db.session.execute(sql, {"userId":userId, "exerciseId":exerciseId})
        db.session.commit()
        return True
    
    

def checkForDuplicate(exercise, userId, exerciseId):
        sql  = "SELECT EXISTS(SELECT id FROM trackedExercises WHERE user_id=:userId AND exercise_id=:exerciseId)"
        result = db.session.execute(sql, {"userId":userId, "exerciseId":exerciseId})
        if result.fetchone()[0]:
            return True
        else:
            return False

    
    
def untrackExercise(exercise):
    try:
        userId = session["userId"]
        exerciseId = get_exercise_id(exercise)
        
        sql  = "UPDATE trackedExercises SET visible = 0 WHERE user_id=:userId AND exercise_id=:exerciseId"
        db.session.execute(sql, {"userId":userId, "exerciseId":exerciseId})
        db.session.commit()
        return True
    except:
        return False

    
    
def get_trackedList():
    userId = session["userId"]
    sql = "SELECT exercise FROM exercises, trackedExercises WHERE exercises.id=trackedExercises.exercise_id AND trackedExercises.user_id=:userId AND trackedExercises.visible=1"
    result = db.session.execute(sql, {"userId":userId})
    polls = result.fetchall()
    return polls


def get_exerciseVariablesListForTEST(exercise, userId):
        sql = "SELECT ex.exercise, e.setsTotal, e.reps, e.weight, e.time, e.info, e.id FROM exerciseVariables e, trackedExercises tE, exercises ex WHERE ex.id=:exerciseId AND tE.id=e.trackedExercise_id AND tE.user_id=:userId AND tE.visible=1 AND e.trackedExercise_id=:trackedExerciseId ORDER BY e.id DESC"
        result = db.session.execute(sql, {"userId":userId, "exerciseId":get_exercise_id(exercise), "trackedExerciseId":get_trackedExercise_id(exercise, userId)})
        polls = result.fetchall()
        if len(polls) != 0:
            return polls
        else:
            lista=[]
            polls = (exercise, "No saved workouts!")
            lista.append(polls)
            return lista


def get_exerciseVariablesList():
    userId = session["userId"]
    lista = get_trackedList()
    
    if len(lista) == 0:
        return None
    
    palautettava = []
    for alkio in lista:
        polls = get_exerciseVariablesListForTEST(alkio[0], userId)
        palautettava.append(polls)    
        
    return palautettava


def saveWorkout(Exercise, Sets, Reps, Weight, Info):
    ExerciseId = get_trackedExercise_id(Exercise, session["userId"])
    try:
        sql  = "INSERT INTO exerciseVariables (trackedExercise_id, setsTotal, reps, weight, time, info) VALUES (:exerciseId,:sets,:reps,:weight,CURRENT_DATE,:info)"
        db.session.execute(sql, {"exerciseId":ExerciseId,"sets":Sets,"reps":Reps,"weight":Weight,"info":Info})
        db.session.commit()
        return True
    except:
        return False
    
    

def editWorkout(Id, Sets, Reps, Weight, Info):
    try:
        sql  = "UPDATE exerciseVariables SET setsTotal=:sets, reps=:reps, weight=:weight, info=:info WHERE id=:id"
        db.session.execute(sql, {"id":Id,"sets":Sets,"reps":Reps,"weight":Weight,"info":Info})
        db.session.commit()
        return True
    except:
        return False
    
def deleteWorkout(Id):
    try:
        sql  =  "DELETE FROM exerciseVariables WHERE id=:id"
        db.session.execute(sql, {"id":Id})
        db.session.commit()
        return True
    except:
        return False
    

    
def searchBank(query):
    sql = "SELECT exercise FROM exercises WHERE exercise LIKE :query"  # NO LIMIT ATM
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    results = result.fetchall()
    return results;

    
    

