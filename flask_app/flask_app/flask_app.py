import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask_app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_APP_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text form entries order by id desc')
    entries = cur.fetchall()
    return render_template('show-entries.html', entries=entries)


@app.route('/add', method=['POST'])
def add_entries():
    if not session.get('loggeg_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully pasted')
    return redirect(url_for('show_entries'))


@app.route('/login', method=['GET, POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] !=app.config['USERNAME']:
            error = 'Niełaściwa nazwa użytkownika'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Niewłaściwe hasło'
        else:
            session['logged_in'] = True
            flash('Zostałeś poprawnie zalogowany:)')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Zostałeś poprawnie wylogowany')
    return redirect(url_for('show_entries'))
# http://flask.pocoo.org/docs/0.12/tutorial/views/#tutorial-views