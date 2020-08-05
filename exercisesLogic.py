from db import db
from flask import redirect, render_template, session
import usersLogic, datetime


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

def get_exercise_id(exercise):
    sql = "SELECT id FROM exercises WHERE exercise=:exercise"
    result = db.session.execute(sql, {"exercise":exercise})
    return result.fetchone()[0]



def get_exercise_name(exerciseId):
    sql = "SELECT exercise FROM exercises WHERE id=:exerciseId"
    result = db.session.execute(sql, {"exerciseId":exerciseId})
    return result.fetchone()[0]

def get_trackedExercise_id(exercise):
    sql = "SELECT tE.id FROM trackedExercises tE, exercises e WHERE e.exercise=:exercise AND tE.exercise_id=e.id"
    result = db.session.execute(sql, {"exercise":exercise})
    return result.fetchone()[0]

def get_trackedExercise_idByUserAndExercise(userId, exerciseId):
    sql = "SELECT id FROM trackedExercises WHERE exercise_id=:exerciseId AND user_id=:userId"
    result = db.session.execute(sql, {"exerciseId":exerciseId, "userId":userId})
    return result.fetchone()[0]


def trackExercise(exercise):
    
    userId = usersLogic.user_id_db()
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
        userId = usersLogic.user_id_db()
        exerciseId = get_exercise_id(exercise)
        
        sql  = "UPDATE trackedExercises SET visible = 0 WHERE user_id=:userId AND exercise_id=:exerciseId"
        db.session.execute(sql, {"userId":userId, "exerciseId":exerciseId})
        db.session.commit()
        return True
    except:
        return False

    
    
def get_trackedList():
    userId = usersLogic.user_id_db()
    sql = "SELECT exercise FROM exercises, trackedExercises WHERE exercises.id=trackedExercises.exercise_id AND trackedExercises.user_id=:userId AND trackedExercises.visible=1"
    result = db.session.execute(sql, {"userId":userId})
    polls = result.fetchall()
    return polls


def get_exerciseVariablesListFor(exercise, userId):
    sql = "SELECT exercises.exercise, e.setsTotal, e.reps, e.weight, e.time FROM exerciseVariables e INNER JOIN trackedExercises tE INNER JOIN exercises ON tE.user_id=:userId AND tE.exercise_id=exercises.id AND exercises.id=tE.exercise_id AND tE.id=e.trackedExercise_id AND tE.visible=1 AND exercises.exercise=:exerciseName ORDER BY e.time DESC"
    result = db.session.execute(sql, {"userId":userId, "exerciseName":exercise})
    polls = result.fetchall()
    return polls


def get_exerciseVariablesListForTEST(exercise, userId):
    if checkForDuplicateTEST(userId, exercise):
        sql = "SELECT ex.exercise, e.setsTotal, e.reps, e.weight, e.time, e.info, e.trackedExercise_id FROM exerciseVariables e, trackedExercises tE, exercises ex WHERE ex.id=:exerciseId AND tE.id=e.trackedExercise_id AND tE.user_id=:userId AND tE.visible=1 AND e.trackedExercise_id=:trackedExerciseId ORDER BY e.time DESC"
        result = db.session.execute(sql, {"userId":userId, "exerciseId":get_exercise_id(exercise), "trackedExerciseId":get_trackedExercise_id(exercise)})
        polls = result.fetchall()
        return polls
    else:
        lista=[]
        polls = (exercise, "No saved workouts!")
        lista.append(polls)
        return lista


def checkForDuplicateTEST(userId, exercise):
        exerciseId = get_exercise_id(exercise)
        sql  = "SELECT EXISTS(SELECT e.trackedExercise_id, e.setsTotal, e.reps, e.weight, e.time FROM exerciseVariables e, trackedExercises tE WHERE tE.id=e.trackedExercise_id AND tE.user_id=:userId AND tE.visible=1 AND tE.exercise_id=:exerciseId ORDER BY e.time DESC)"
        result = db.session.execute(sql, {"userId":userId, "exerciseId":exerciseId})
        if result.fetchone()[0]:
            print("asdasd")
            return True
        else:
            return False



def get_exerciseVariablesList():
    userId = usersLogic.user_id_db()
    list = get_trackedList()
    
    palautettava = []
    for alkio in list:
        polls = get_exerciseVariablesListForTEST(alkio[0], userId)
        palautettava.append(polls)
    
    return palautettava


def saveWorkout(Exercise, Sets, Reps, Weight, Info):
    ExerciseId = get_trackedExercise_id(Exercise)
    time = datetime.datetime.now()
    time.strftime('%Y-%m-%d')
    try:
        sql  = "INSERT INTO exerciseVariables (trackedExercise_id, setsTotal, reps, weight, time, info) VALUES (:exerciseId,:sets,:reps,:weight,:time,:info)"
        db.session.execute(sql, {"exerciseId":ExerciseId,"sets":Sets,"reps":Reps,"weight":Weight,"time":time,"info":Info})
        db.session.commit()
        return True
    except:
        return False
    
def searchBank(query):
    sql = "SELECT exercise FROM exercises WHERE exercise LIKE :query"  # NO LIMIT ATM
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    results = result.fetchall()
    return results;
    
    

