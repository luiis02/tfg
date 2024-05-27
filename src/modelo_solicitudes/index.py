
from flask import Flask, request, redirect, render_template, url_for, flash, get_flashed_messages, make_response
from prediccion import clasificar_frase
import requests, json


app = Flask(__name__)
app.secret_key = 'change-this'



@app.before_request
def clear_flash():
    if len(get_flashed_messages()) > 0:
        flash("")
    if request.method == 'GET': metodo = "GET"
    else: metodo = "POST"
    
    http_version = request.environ.get('SERVER_PROTOCOL')

    request_string = f"{metodo} {request.path}"
    
    print(request_string)
    if clasificar_frase(request_string) == "Ataque":
        if request.cookies.get('human') != 'yes':
            response = make_response(redirect(url_for("botpage")))
            response.set_cookie('ruta', request.path)
            return response
            print("----------------------------- ATAQUE")
            return redirect(url_for('botpage'))
    else:
        print("----------------------------- NORMAL")

@app.route("/", methods=["GET", "POST"])
def home():
    return "Hello, World!"

@app.route("/saludo/", methods=["GET", "POST"])
def saludo():
    return "Hola, Mundo!"



@app.route("/botpage/", methods=["GET", "POST"])
def botpage():
    sitekey = "6LfXEq8UAAAAAEcgY_bRY7PyaWy7O2Y43DKYteZB"
    if request.method == "POST":
        captcha_response = request.form['g-recaptcha-response']
        if esHumano(captcha_response):
            print("YES")
            ruta_cookie = request.cookies.get('ruta')
            response = make_response(redirect(ruta_cookie))
            response.set_cookie('human', 'yes')
            return response
        else:
            status = "Sorry ! Bots are not allowed."
            print("NO")
    return render_template("botpage.html", sitekey=sitekey)
                

                
def esHumano(captcha_response):
    secret = "6LfXEq8UAAAAACPtCIXcmbiVhVjf9mj_xRFmhs-b"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)