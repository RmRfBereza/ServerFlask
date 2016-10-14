# -*- coding: utf-8 -*-
import json
import sys
from flask import Flask, render_template
from flask_socketio import join_room, leave_room, send, SocketIO

import conf
from utils import decode_json

app = Flask(__name__)
app.debug = conf.DEBUG
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello():
    return render_template('index.html')


@socketio.on('join')
def on_join(request):
    data = decode_json(json.loads(request))
    username = data['username']
    room = data['room']
    join_room(room)
    send(json.dumps('{0} has entered the room.'.format(username)), room=room)


@socketio.on('leave')
def on_leave(request):
    data = decode_json(json.loads(request))
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('message')
def message_for_room(request):
    data = decode_json(json.loads(request))
    room = data['room']
    send(json.dumps(json.dumps(data)), room=room)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        host = conf.HOST
        port = conf.PORT
    else:
        host = sys.argv[1]
        port = sys.argv[2]

    socketio.run(app, host=host, port=int(port))
