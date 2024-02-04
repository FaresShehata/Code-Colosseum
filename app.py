from flask import Flask, render_template, request, redirect, request
from flask_socketio import SocketIO, send, emit
from testCase import testCase
from threading import Timer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}
game_code = None
responses = {}
received_responses = 0
timingThread = None
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
def handle_client_message(data):
    # username = users.get(request.sid, 'Unknown User')
    #username = message['username']
    #text = message['text']
    t = questions[1]
    t.code = data["answer"]

    res = str(t.returnMessage())
    print(f'Message from {users[data["uuid"]]}: {data["answer"]}')
    print(f'Output: {res}')
    responses[data["uuid"]] = res
    if received_responses == len(users):
        handle_question_end()
    # Broadcast the received message with the username
    #emit('present_question', {'username': username, 'text': res})
@socketio.on("connect")
def handle_connection():
    pass
    
@socketio.on('set_username')
def handle_set_username(data):
    print("--------------------", request.sid)
    id = request.sid
    #print("++++++++++++++", request.namespace.socket.sessid)
    # Check if the user is in users
    if data["uuid"] in users:
        pass
    else:
        users[data["uuid"]] = [data["username"], id]
    # Checking if the user has an old socket
    # if (data["oldsid"] != ""):
    #     handle_update_connection(data)
    
    # else:
    #     users[data["sid"]] = data["username"]
    #     responses[data["sid"]] = []
    
    if data["username"] == "admin":
        emit('redirect_to_admin', {'url': '/admin'})


@socketio.on("update_connection")
def handle_update_connection(data):
    users[data["uuid"]] = request.sid
    
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
    for key in responses:
        responses[key] = None
    received_responses = 0
    # TODO get the question
    # Emit the question to all clients
    socketio.broadcast.emit("new_question", question)
    # Start the timer
    question_time = 60 
    timingThread = Timer(question_time, handle_question_end)
    timingThread.start()

# Handles when all responses have been received or timeout occurs
def handle_question_end():
    timingThread.cancel()
    # Send the feedback to all the users
    for key in responses:
        socketio.to(key).emit("receive_feedback", responses[key])
    # Next question
    display_next_question()

if __name__ == '__main__':
    socketio.run(app, debug=True)
    
