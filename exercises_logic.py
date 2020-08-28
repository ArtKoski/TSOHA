from db import db
from flask import session, flash
from random import choice

def add_exercise(exercise):
    
    ex = exercise.replace(" ", "-").title()
    
    try:
        sql = "INSERT INTO exercises (exercise, popularity) VALUES (:exercise,0)"
        db.session.execute(sql, {"exercise":ex})
        db.session.commit()
        
    except:
        #Ilman rollbackia johtaa InternalErroriin.
        db.session.remove()
        update_exercise(ex)
        
def update_exercise(exercise):
        sql = "UPDATE exercises SET popularity = popularity + 1 WHERE exercise=:exercise"
        db.session.execute(sql, {"exercise":exercise})
        db.session.commit()
    
def get_exercise_list():
    sql = "SELECT exercise, id FROM exercises ORDER BY popularity DESC LIMIT 10"
    result = db.session.execute(sql)
    polls = result.fetchall()
    return polls

def search_exercise_bank(query):
    sql = "SELECT exercise FROM exercises WHERE LOWER(exercise) LIKE LOWER(:query) LIMIT 10"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    results = result.fetchall()
       
    return results;

def get_exercise_id(exercise):
    sql = "SELECT id FROM exercises WHERE exercise=:exercise"
    result = db.session.execute(sql, {"exercise":exercise})
    return result.fetchone()[0]



def get_exercise_name(exercise_id):
    sql = "SELECT exercise FROM exercises WHERE id=:exerciseId"
    result = db.session.execute(sql, {"exerciseId":exercise_id})
    return result.fetchone()[0]

def get_trackedExercise_id(exercise, user_id):
    sql = "SELECT tE.id FROM trackedExercises tE, exercises e WHERE e.exercise=:exercise \
    AND tE.exercise_id=e.id AND tE.user_id=:userId"
    result = db.session.execute(sql, {"exercise":exercise, "userId":user_id})
    return result.fetchone()[0]

def track_exercise(ex_id):
    user_id = session["userId"]
    try:
            sql  = "INSERT INTO trackedExercises (exercise_id, user_id, visible) VALUES (:exercise_id,:user_id, 1)"
            db.session.execute(sql, {"user_id":user_id, "exercise_id":ex_id})
            db.session.commit()
    
    except:
            db.session.remove() #InternalError ilman tätä
            sql  = "UPDATE trackedExercises SET visible = 1 WHERE user_id=:user_id AND exercise_id=:exercise_id"        
            db.session.execute(sql, {"user_id":user_id, "exercise_id":ex_id})
            db.session.commit()
    
        
def untrack_exercise(ex_id):
    try:
        user_id = session["userId"]
        sql  = "UPDATE trackedExercises SET visible = 0 WHERE user_id=:userId AND exercise_id=:exerciseId"
        db.session.execute(sql, {"userId":user_id, "exerciseId":ex_id})
        db.session.commit()
    except:
        flash("Something weird happened.. Try again","error")

    
#Hakee Exercises Exercise,ID
def get_tracked_list():
    user_id = session["userId"]
    sql = "SELECT ex.exercise, ex.id FROM exercises ex, trackedExercises tE WHERE ex.id=tE.exercise_id \
    AND tE.user_id=:userId AND tE.visible=1"
    result = db.session.execute(sql, {"userId":user_id})
    polls = result.fetchall()
    return polls

def get_exerciseVariables_list_for(exercise, exercise_id, user_id, limit):
        sql = "SELECT ex.exercise, e.setsTotal, e.reps, ROUND(e.weight, 2), e.time, e.info, e.id, replace(ex.exercise, ' ', '') \
        FROM exerciseVariables e, trackedExercises tE, exercises ex WHERE ex.id=:exerciseId \
        AND tE.id=e.trackedExercise_id AND tE.user_id=:userId AND tE.visible=1 AND e.trackedExercise_id=:trackedExerciseId \
        ORDER BY e.id DESC LIMIT :limit"
        result = db.session.execute(sql, {"userId":user_id, "exerciseId":exercise_id, \
                                          "trackedExerciseId":get_trackedExercise_id(exercise, user_id),
                                          "limit":limit})
        polls = result.fetchall()
        if len(polls) != 0:
            return polls
        else:
            lista=[]
            polls = (exercise, "No saved workouts!")
            lista.append(polls)
            return lista

def get_exerciseVariables_list(limit):
    user_id = session["userId"]
    lista = get_tracked_list()
    
    if len(lista) == 0:
        return None
    
    palautettava = []
    for alkio in lista:
            polls = get_exerciseVariables_list_for(alkio[0], alkio[1], user_id, limit)
            palautettava.append(polls)    
            
    return palautettava





def save_workout(exercise, sets, reps, weight, info):
    
    ex_id = get_trackedExercise_id(exercise, session["userId"])
    
    if not check_numbers(sets, reps, weight):
        return
    
    try:
        sql  =  "INSERT INTO exerciseVariables (trackedExercise_id, setsTotal, reps, weight, time, info) \
        VALUES (:exerciseId,:sets,:reps,:weight,CURRENT_DATE,:info)"
        db.session.execute(sql, {"exerciseId":ex_id,"sets":sets,"reps":reps,"weight":weight,"info":info})
        db.session.commit()
    except:
        return
    

def edit_workout(ex_id, sets, reps, weight, info):
    if not check_numbers(sets, reps, weight):
        return False
    
    try:
        sql  =  "UPDATE exerciseVariables SET setsTotal=:sets, reps=:reps, weight=:weight, info=:info WHERE id=:id"
        db.session.execute(sql, {"id":ex_id,"sets":sets,"reps":reps,"weight":weight,"info":info})
        db.session.commit()
        return True
    except:
        return False
    
def delete_workout(ex_id):
    try:
        sql  =  "DELETE FROM exerciseVariables WHERE id=:id"
        db.session.execute(sql, {"id":ex_id})
        db.session.commit()
        return True
    except:
        return False
    
def check_numbers(sets, reps, kg):
    
    #Tarkistaa onko syotteet numeroita
    try:
        val1 = int(sets)
        val2 = int(reps)
        val3 = float(kg)
    
    except ValueError:
        flash(get_random_errortext(), "error")
        return False
    
    #Tarkistaa ovatko syötteet realistisia
    flag = True
    if float(kg) > 1000 or float(kg) < 0:
        flag = False
    
    elif int(reps) > 50 or int(reps) < 0:
        flag = False
    
    elif int(sets) > 50 or int(sets) < 0:
        flag = False
    
    if flag == False:
        flash(get_random_errortext(), "error")
        
    return flag
    
def get_random_errortext():
    errors = ["Lets be real now..", "Hmm..", "A typo?..", "Interesting.."]
    return choice(errors)
