from flask import Flask,  render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("contenido.html")    

@app.route('/layout')
def layout():
    return render_template("contenido.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/registro')
def registro():
    return render_template("registro.html")

if __name__ == '__main__':
    app.run(debug=True)