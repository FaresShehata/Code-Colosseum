from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send, emit
from testCase import testCase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}
game_code = None
responses = {}

questions = [
    testCase("add", [
        ([1,2],3)
    ], description="make a function 'add' to add 2 numbers"),
    testCase("factorial", [
        [[5],120], [[6],720]
    ], description="write a function 'factorial' to calculate the facotrial of a number")
]

@app.route('/')
def index():
    return render_template('waiting.html')

@app.route('/admin')
def admin():
    return render_template('host.html')

@app.route('/question')
def waiting():
   return render_template('index.html')

@app.route('/displayResultsPlayer')
def display_results_player():
    return render_template('displayResultsPlayer.html')

@socketio.on('message_from_client')
def handle_client_message(message):
    username = users.get(request.sid, 'Unknown User')
    text = message['text']
    t = questions[1]
    t.code = text

    res = str(t.returnMessage())
    print(f'Message from {username}: {text}')

    print(f'Output: {res}')
    # Broadcast the received message with the username
    emit('present_question', {'username': username, 'text': res}, room=request.sid)

@socketio.on('set_username')
def handle_set_username(data):
    username = data['username']
    if username == "admin":
        emit('redirect_to_admin', {'url': '/admin'})
    else:
        users[request.sid] = username

@socketio.on("set_game_code")
def handle_set_game_code(data):
    game_code = data["game_code"]
    # Wait for the host to start the game
    # TODO start the game

@socketio.on("start_game")
def handle_start_game():
    # Display question for all players.
    emit('redirect_to_question', {'url': '/question'}, broadcast=True)

def display_next_question():
    question = ""
    # TODO get the question
    # Emit the question to all clients
    socketio.broadcast.emit("new_question", question)
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
    
