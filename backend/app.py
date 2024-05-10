from flask import Flask, render_template, request
from permissions_change import changePermission
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['inputField']
    role = request.form['option']
    purpose = request.form['purposeField']
    changePermission(email, role)
    with open("logs/permissions_change.log", "a") as f:
        f.write(f"{datetime.datetime.now()}, {email}, {role}, {purpose}\n")
    return render_template('success.html', email=email, role=role)

@app.route('/logs')
def logsHandler():
    with open("logs/permissions_change.log", "r") as f:
        logs = f.readlines()        
    return logs
            

@app.errorhandler(Exception)
def bruh(e):
    err = f"An exception of type {type(e).__name__} occurred. Arguments:\n{e.args!r}"
    return render_template('oopsy.html', problem=err), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
