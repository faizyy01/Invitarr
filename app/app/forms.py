from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):

    username = StringField('Username',
                                validators=[DataRequired()])

    password =  PasswordField('Password',
                                validators=[DataRequired()])

    submit = SubmitField('Save Changes')

class GeneralForm(FlaskForm):
    
    username = StringField('Username',
                                validators=[DataRequired()])

    password =  PasswordField('Password',
                                validators=[DataRequired()])

    submit = SubmitField('Save Changes')

class BotForm(FlaskForm):
    
    discord_bot_token = StringField('Discord Bot Token',
                                validators=[DataRequired()])

    role_id =  IntegerField('Role Id',
                                validators=[DataRequired()])

    channel_id = IntegerField('Channel Id',
                                validators=[DataRequired()])
    owner_id = IntegerField('Owner Id',
                                validators=[DataRequired()])
    # Auto Remove User
    auto_remove_user = BooleanField('On')

    submit = SubmitField('Save Changes')

class PlexForm(FlaskForm):
    
    plex_user = StringField('Plex User',
                                validators=[DataRequired()])
    plex_pass = StringField('Plex Pass',
                                validators=[DataRequired()])
    plex_server_name = StringField('Plex Server Name',
                                validators=[DataRequired()])
    plex_libs = StringField('Plex Libs',
                                validators=[DataRequired()])
    submit = SubmitField('Save Changes')