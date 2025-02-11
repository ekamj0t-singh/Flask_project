from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/zephyrus')
def zephyrus():
    return render_template('zephyrus.html')

@app.route('/zenbook')
def zenbook():
    return render_template('zenbook.html')

@app.route('/vivobook')
def vivobook():
    return render_template('vivobook.html')

@app.route('/tuf')
def tuf():
    return render_template('tuf.html')

@app.route('/strix')
def strix():
    return render_template('strix.html')




if __name__ == '__main__':
    app.run(debug=True)
    
