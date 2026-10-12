from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)

    
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = None

    if request.method == "POST":
        message = "Форму заповнено успішно. Це демонстраційна форма, повідомлення не надсилається."

    return render_template("contact.html", title="Контакти", message=message)


if __name__ == "__main__":
    app.run(debug=True)
