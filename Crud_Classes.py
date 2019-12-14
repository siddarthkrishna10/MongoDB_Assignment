from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField

class CreatePlayer(FlaskForm):
    title = TextField('Player Name')
    position = TextField('Position')
    age = IntegerField('Age')
    create = SubmitField('Create')

class UpdatePlayer(FlaskForm):
    key = TextField('Player ID')
    position = TextField('New Position')
    update = SubmitField('Update')

class DeletePlayer(FlaskForm):
    key = TextField('Player ID')
    title = TextField('Player Name')
    delete = SubmitField('Delete')

class ResetData(FlaskForm):
    reset = SubmitField('Reset')
