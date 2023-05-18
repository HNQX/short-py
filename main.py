from flask import Flask, render_template, request, redirect
from gevent import pywsgi
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB("db/db.json")
Me = Query()


@app.route("/", methods=["get", "post"])
def index():
    data = db.all()
    res = {"data": data}
    return render_template("index.html", **res)


@app.route("/shorten", methods=["post"])
def short_url():
    r_code = request.form["custom_url"]
    if len(db.search(Me.code == r_code)):
        return err(201, "CODE EXIST", "CODE EXIST!", "CHANGE PLZ :D")
    else:
        db.insert({"url": request.form["url"], "code": r_code})
        return redirect("/")


@app.route("/remove", methods=["post"])
def remove_url():
    db.remove(Me.code == request.form["code"])
    return redirect("/")


@app.route("/<url>")
def redirect_url(url):
    data = db.search(Me.code == url)
    if len(data):
        return redirect(data[0]["url"])
    else:
        return err(404, "NOT FOUND URL", "[" + url + "] IS NOT FOUND", "CHECK PLZ :D")


@app.route("/edit", methods=["post"])
def edit_url():
    r_code_old = request.form["previousCode"]
    r_code = request.form["code"]
    r_url = request.form["url"]

    if len(db.search(Me.code == r_code)):
        return err(201, "CODE EXIST", "CODE EXIST!", "CHANGE PLZ :D")
    else:
        db.update({"code": r_code, "url": r_url}, Me.code == r_code_old)
        return redirect("/")


def err(code, title, m1, m2):
    return render_template("error.html", code=code, title=title, m1=m1, m2=m2)


server = pywsgi.WSGIServer(("0.0.0.0", 5000), app)
server.serve_forever()
