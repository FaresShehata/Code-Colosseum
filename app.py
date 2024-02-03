from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send, emit
from testCase import testCase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}
game_code = None
responses = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/displayResultsPlayer')
def display_results_player():
    return render_template('displayResultsPlayer.html')

@socketio.on('message_from_client')
def handle_client_message(message):
    username = users.get(request.sid, 'Unknown User')
    text = message['text']
    t = testCase("add", [
        ([1,2],3),
        ([-1,-2],-3)
    ], text)

    res = t.returnMessage()
    print(f'Message from {username}: {res}')
    # Broadcast the received message with the username
    emit('present_question', {'username': username, 'text': res}, room=request.sid)

@socketio.on('set_username')
def handle_set_username(data):
    username = data['username']
    users[request.sid] = username

@socketio.on("set_game_code")
def handle_set_game_code(data):
    game_code = data["game_code"]
    # Wait for the host to start the game
    # TODO start the game

@socketio.on("start_game")
def handle_start_game(data):
    # Start displaying questions
    responses = users.copy()
    for key in responses:
        responses[key] = None
    display_next_question()

def display_next_question():
    question = ""
    # TODO get the question
    # Emit the question to all clients
    socketio.broadcast.emit("new_question", question)
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
    
