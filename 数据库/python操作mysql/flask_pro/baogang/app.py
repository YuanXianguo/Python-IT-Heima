from flask import Flask, render_template, jsonify, request

import config
from exts import db
from models import Pictures

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# @app.route('/')
# def index():
#     return render_template("index.html")


@app.route("/api/id/", methods=["POST", "GET"])
def id():
    if request.method == "POST":
        work_id = request.form.get("workId")
        print(work_id)
        picture = Pictures.query.filter(Pictures.id == 1).first()
        picture.work_id = work_id
        db.session.add(picture)
        db.session.commit()
        return jsonify(picture.json())
    else:
        return "hello python"


# @app.route("/search/")
# def search():
#     picture = Pictures.query.filter(Pictures.id == 1).first()
#     picture.work_id = 10
#     db.session.add(picture)
#     db.session.commit()
#     return render_template("search.html")


@app.route("/api/show/", methods=["POST", "GET"])
def show():
    # time1 = request.form.get("time1")
    # time2 = request.form.get("time2")

    time1 = "2019-07-10 09:59:45"
    time2 = "2019-07-16 09:59:45"
    pictures = Pictures.query.filter(Pictures.time >= time1, Pictures.time <= time2).all()
    dic = dict()
    for i in range(len(pictures)):
        dic[i] = pictures[i].json()
    return jsonify(dic)


if __name__ == '__main__':
    app.run()
