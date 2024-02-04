from flask import Flask, render_template, request, redirect, request
from flask_socketio import SocketIO, send, emit
from src.testCase import testCase
from threading import Timer
from random import randint

users = {}
wait_for_this_many_users = 2
current_question = 0

results = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

yes = [100, 50, 32, 87, 42]

questions = [
    testCase("add", [
        ([1, 2], 3)
    ], description="make a function 'add' to add 2 numbers"),
    testCase("factorial", [
        ([5], 120), ([6], 720)
    ], description="write a function 'factorial' to calculate the factorial of a number"),
    # testCase("sum_array", [
    #     ([1, 2, 3, 4, 5], 15), ([10, 20, 30], 60)
    # ], description="write a function 'sum_array' that returns the sum of all elements in an array"),
    # testCase("is_prime", [
    #     ([2], True), ([4], False), ([11], True)
    # ], description="write a function 'is_prime' to check if a number is prime"),
    # testCase("fibonacci", [
    #     ([5], 5), ([7], 13)
    # ], description="write a function 'fibonacci' that returns the nth number in the Fibonacci sequence")
]

responses: list[dict[str, str]] = [{} for _ in range(len(questions))]

@app.route('/')
def index():
    return render_template('waiting.html')

@app.route('/admin')
def admin():
    return render_template('host.html')

@app.route('/question')
def waiting():
   return render_template('index.html', first_question = questions[current_question].description)

@app.route('/displayResultsPlayer')
def display_results_player():
    names = "".join([f"{n[0]}\n" for n in users.values()])
    # data = {"labels":[f"{n[0]}" for n in users.values()],
    #         "values":[e["percentage"] 
    #                     for r in responses
    #                     for e in r.values()]}
    data = {"labels": [f"{n[0]}" for n in users.values()], "values": [yes[i % len(yes)] for i in range(len(users))]}

    return render_template('displayResultsPlayer.html', names=names, data=data)

def end():
    emit('end', {"url": "/displayResultsPlayer"}, broadcast=True)

@socketio.on('message_from_client')
def handle_client_message(data):
    t = questions[current_question]
    t.code = data["answer"]

    res = t.returnMessage()
    print(f'Message from {users[data["uuid"]][0]}: {data["answer"]}')
    print(f'Output: {res["ret"]}')
    # responses[users[data["uuid"]][current_question]] = res
    responses[current_question][users[data["uuid"]][1]] = res

    if len(responses[current_question]) == len(users):
        print(f"{responses = }")
        handle_question_end()
    # Broadcast the received message with the username
    #emit('present_question', {'username': username, 'text': res})

@socketio.on("connect")
def handle_connection():
    pass
    
@socketio.on('set_username')
def handle_set_username(data):
    # Add the user to the results data structure
    if data["uuid"] not in results:
        results[data["uuid"]] = []
    # print("--------------------", request.sid)
    id = request.sid
    #print("++++++++++++++", request.namespace.socket.sessid)
    # Check if the user is in users
    if data["uuid"] in users:
        pass
    elif data["username"] != "admin":
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
    users[data["uuid"]][1] = request.sid
    
@socketio.on("start_game")
def handle_start_game():
    # Display question for all players.
    emit('redirect_to_question', {'url': '/question'}, broadcast=True)

def display_next_question():
    # for key in responses:
    #     responses[key] = None
    # TODO get the question
    # Emit the question to all clients
    msg = {
        "description": questions[current_question].description
    }
    emit("new_question", msg, broadcast=True)

# Handles when all responses have been received or timeout occurs
def handle_question_end():
    # # Send the feedback to all the users
    # for key in responses:
    #     emit("receive_feedback", responses[key], to=users[key][1])
    # # Next question
    # display_next_question()
    global current_question
    current_question += 1
    if current_question < len(questions):
        display_next_question()
    else:
        # todo dislpay results
        current_question = 0
        end()

if __name__ == '__main__':
    socketio.run(app, debug=True)
    
