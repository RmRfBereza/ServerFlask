from flask import Flask, render_template
from flask_socketio import join_room, leave_room, send, SocketIO

import conf

app = Flask(__name__)
app.debug = conf.DEBUG
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello():
    return render_template('index.html')


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('message')
def message_for_room(data):
    room = data['room']
    send('received data: ' + str(data), room=room)


if __name__ == '__main__':
    socketio.run(app, host=conf.HOST)
