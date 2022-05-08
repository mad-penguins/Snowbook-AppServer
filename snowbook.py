import json
import hashlib
import secrets

from flask import Flask, request

import db


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/register')
def register_new_user():
    response = {}
    response['error'] = 'this username already exists'

    username = request.values.get('username', 'user')
    password = request.values.get('password', 'password')

    if db.getUser(username) is  None:
        passhash = hashlib.sha224(str(password).encode()).hexdigest()

        db.createNewUser(username, passhash)

        response.clear()
        response['register'] = 'OK'

    return json.dumps(response)


@app.route('/login')
def login():
    response = {}
    response['error'] = 'no access'

    username = request.values.get('username', 'user')
    password = request.values.get('password', 'password')

    u = db.getUser(username)

    if u is not None:
        passhash = hashlib.sha224(str(password).encode()).hexdigest()

        if u.passhash == passhash:
            response.clear()
            response['login'] = 'OK'

            token = secrets.token_hex(16)
            db.createNewToken(u.id, token)

            response['token'] = token

    return json.dumps(response)


@app.route('/notes/<token>')
def get_all_notes(token):
    response = {}
    response['error'] = 'no access'

    t = db.getToken(token)

    if t is not None:
        response.clear()
        response['getAllNotes'] = 'OK'

        u = db.getById(db.User, t.user_id)
        notes_list = db.getAllNotes(u)

        notes_id_list = []
        for x in notes_list:
            notes_id_list.append(x.id)

        response['notes'] = notes_id_list

    return json.dumps(response)


@app.route('/notes/<int:note_id>/<token>')
def get_note(note_id, token):
    response = {}
    response['error'] = 'no access'

    t = db.getToken(token)

    if t is not None:
        u = db.getById(db.User, t.user_id)
        n = db.getById(db.Note, note_id)

        if n is not None:
            if u.id == n.user_id:
                response.clear()
                response['getNote'] = 'OK'

                note = {}
                note['title'] = n.title
                note['text'] = n.text

                response['note'] = note

    return json.dumps(response)


@app.route('/notes/new/<token>')
def create_note(token):
    response = {}
    response['error'] = 'no access'

    t = db.getToken(token)

    if t is not None:
        response.clear()
        response['createNewNote'] = 'OK'

        u = db.getById(db.User, t.user_id)

        title = request.values.get('title', "some name")
        text = request.values.get('text', "some text")

        db.createNewNote(u.id, title, text)

        response['note_id'] = db.getAllNotes(u)[-1].id

    return json.dumps(response)


@app.route('/notes/<int:note_id>/update/<token>')
def update_note(note_id, token):
    response = {}
    response['error'] = 'no access'

    t = db.getToken(token)

    if t is not None:
        u = db.getById(db.User, t.user_id)
        n = db.getById(db.Note, note_id)

        if n is not None:
            if u.id == n.user_id:
                response.clear()
                response['updateNote'] = 'OK'

                title = request.values.get('title', n.title)
                text = request.values.get('text', n.text)

                n.title = title
                n.text = text

                db.update(n)

    return json.dumps(response)


@app.route('/notes/<int:note_id>/delete/<token>')
def delete_note(note_id, token):
    response = {}
    response['error'] = 'no access'

    t = db.getToken(token)

    if t is not None:
        u = db.getById(db.User, t.user_id)
        n = db.getById(db.Note, note_id)

        if n is not None:
            if u.id == n.user_id:
                response.clear()
                response['deleteNote'] = 'OK'

                db.delete(n)

    return json.dumps(response)
