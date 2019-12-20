from flask import Flask, render_template, flash

app = Flask(__name__)

flag = [0]

app.config["SECRET_KEY"] = "afdkajdvkadhuasduioq32hifvsn"


@app.route("/")
def index():
    if flag:
        # 添加闪现信息
        flash('hello1')
        flash('hello2')
        flash('hello3')
        flag.pop()

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
