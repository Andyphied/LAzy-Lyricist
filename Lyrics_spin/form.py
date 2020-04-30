from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class Lyrics_info(FlaskForm):

    artist = StringField('Artist', [DataRequired()])
    
    album  = StringField('Album',[DataRequired()])

    lines = IntegerField('No of Lines', [DataRequired()])

    submit = SubmitField('Spin Lyrics')