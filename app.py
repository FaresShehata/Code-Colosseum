from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message_from_client')
def handle_client_message(message):
    username = users.get(request.sid, 'Unknown User')
    text = message['text']
    print(f'Message from {username}: {text}')
    
    # Emit the received message only to the sender
    emit('present_question', {'username': username, 'text': text}, room=request.sid)

@socketio.on('set_username')
def handle_set_username(data):
    username = data['username']
    users[request.sid] = username

if __name__ == '__main__':
    socketio.run(app, debug=True)
