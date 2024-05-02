from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['inputField']
    role = request.form['option']
    # change_permission(email, role)
    return f'You entered: {email} and selected: {role}'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
