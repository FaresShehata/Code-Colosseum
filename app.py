from flask import Flask, request
from src.logic import execute_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        code = request.form.get('code_box')
        result = execute_code(code)
        return result
    return '''<form method="POST">
                  Code to execute: <br>
                  <input type="text" name="code_box" /><br>
                  <input type="submit" value="Execute" /><br>
              </form>'''

if __name__  == "__main__":
    app.run(host='0.0.0.0', debug=True)
