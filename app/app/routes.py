from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
import subprocess

from app import app, db, bcrypt
from app.models import User
from app.forms import LoginForm, GeneralForm, BotForm, PlexForm
from app import configHandler

db.create_all()
BOT_SECTION = 'bot_envs'
proc = None

def manage_bot(option):
    global proc
    if option == 'start':
        proc = subprocess.Popen(["python", "app/bot/Invitarr.py"])
    elif option == 'kill':
        if proc:
            proc.terminate()

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    flash('Logged out.')
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = GeneralForm()
    if request.method == 'GET':
        user = User.query.all()[0]
        form.username.data = user.username
        form.password.data = user.password
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.all()[0]
            user.username = form.username.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            logout_user()
            flash('Details updated.')
            return redirect(url_for('login'))
    return render_template('index.html', form=form)

@app.route('/bot', methods=['GET', 'POST'])
@login_required
def bot():
    form = BotForm()
    if request.method == 'GET':
        try:
            config = configHandler.get_config()
            form.discord_bot_token.data = config.get(BOT_SECTION, 'discord_bot_token')
            form.role_id.data = config.get(BOT_SECTION, 'role_id')
            form.channel_id.data = config.get(BOT_SECTION, 'channel_id')
            form.owner_id.data = config.get(BOT_SECTION, 'owner_id')
            form.auto_remove_user.data = config.get(BOT_SECTION, 'auto_remove_user')
        except:
            pass
    elif request.method == 'POST':
        if form.validate_on_submit():
            try:
                configHandler.change_config_form(form)
                flash('Settings updated.')
                manage_bot('kill')
                manage_bot('start')
            except:
                flash('Some error in updating settings')
    return render_template('bot.html', form = form)

@app.route('/plex', methods=['GET', 'POST'])
@login_required
def plex():
    form = PlexForm()
    if request.method == 'GET':
        try:
            config = configHandler.get_config()
            form.plex_user.data = config.get(BOT_SECTION, 'plex_user')
            form.plex_pass.data = config.get(BOT_SECTION, 'plex_pass')
            form.plex_server_name.data = config.get(BOT_SECTION, 'plex_server_name')
            form.plex_libs.data = config.get(BOT_SECTION, 'plex_libs')
        except:
            pass
    elif request.method == 'POST':
        if form.validate_on_submit():
            try:
                configHandler.change_config_form(form)
                flash('Settings updated.')
            except:
                flash('Some error in updating settings')
            try:
                manage_bot('kill')
                manage_bot('start')
            except Exception as e:
                raise Exception(e)

    return render_template('plex.html', form = form)
