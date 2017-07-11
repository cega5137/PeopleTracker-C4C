from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return render_template('hello', message="Hello World!")

if __name__ == "__main__":
    app.run(host='10.0.0.227', port=8080)
