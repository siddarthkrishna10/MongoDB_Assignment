from flask import Flask, render_template, redirect
from pymongo import MongoClient
from Crud_Classes import *

webapp = Flask(__name__)
webapp.config.update(dict(SECRET_KEY='yoursecretkey'))

client = MongoClient('localhost:27017')
db = client.FootballDB

if db.settings.find({'name': 'player_id'}).count() <= 0:
    print("player_id Not found, creating....")
    db.settings.insert_one({'name': 'player_id', 'value': 0})

def updatePlayerID(value):
    player_id = db.settings.find_one()['value']
    player_id += value

    db.settings.update_one({'name': 'player_id'}, {'$set': {'value': player_id}})

def createPlayer(form):
    title = form.title.data
    age = form.age.data
    position = form.position.data
    player_id = db.settings.find_one()['value']

    task = {'id': player_id, 'title': title, 'position': position, 'age': age}

    db.tasks.insert_one(task)
    updatePlayerID(1)
    return redirect('/')

def updatePlayer(form):
    key = form.key.data
    position = form.position.data

    db.tasks.update_one({"id": int(key)}, {"$set": {"position": position}},)
    return redirect('/')

def deletePlayer(form):
    key = form.key.data
    title = form.title.data

    if (key):
        print(key, type(key))
        db.tasks.delete_many({'id': int(key)})
    else:
        db.tasks.delete_many({'title': title})
    return redirect('/')

def resetData(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name': 'player_id', 'value': 0})
    return redirect('/')

@webapp.route('/', methods=['GET', 'POST'])
def main():
    cform = CreatePlayer(prefix='cform')
    uform = UpdatePlayer(prefix='uform')
    dform = DeletePlayer(prefix='dform')
    reset = ResetData(prefix='reset')

    if cform.validate_on_submit() and cform.create.data:
        return createPlayer(cform)

    if uform.validate_on_submit() and uform.update.data:
        return updatePlayer(uform)

    if dform.validate_on_submit() and dform.delete.data:
        return deletePlayer(dform)

    if reset.validate_on_submit() and reset.reset.data:
        return resetData(reset)

    docs = db.tasks.find()
    data = []

    for i in docs:
        data.append(i)

    return render_template('layout.html', cform=cform,
                           uform=uform, dform=dform,
                           data=data, reset=reset)

if __name__ == '__main__':
    webapp.run(debug=True)
