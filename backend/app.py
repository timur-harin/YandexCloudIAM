from flask import Flask, render_template, request
from persmissions_change import changePermission

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['inputField']
    role = request.form['option']
    changePermission(email, role)
    return render_template('success.html', email=email, role=role)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
