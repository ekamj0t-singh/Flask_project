from flask import Flask, render_template
app = Flask(__name__)
@app.route('/Ekam')
def ekkam():
    return render_template('ekam.html')
@app.route('/lap')
def lap():
    return render_template('lap.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
