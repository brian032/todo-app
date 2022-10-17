from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def home():
    all_tasks = db.session.query(Task).all()
    if request.method == 'POST':
        new_task = Task(task=request.form['task'])
        db.session.add(new_task)
        db.session.commit()
        redirect(url_for('home'))
    return render_template("index.html", tasks=all_tasks)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_task = Task(task=request.form['task'],
                        status="Todo")
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/delete")
def delete():
    task_id = request.args.get('id')
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        task_id = request.args.get('id')
        task_to_update = Task.query.get(task_id)
        task_to_update.task = request.form['task']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", id=request.args.get('id'))


@app.route("/update-status")
def update_status():
    task_id = request.args.get('id')
    task_to_update = Task.query.get(task_id)
    if task_to_update.status == "In Progress":
        task_to_update.status = "Completed"
        db.session.commit()
    elif task_to_update.status == "Todo":
        task_to_update.status = "In Progress"
        db.session.commit()
    else:
        task_to_update.status = "Todo"
        db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
