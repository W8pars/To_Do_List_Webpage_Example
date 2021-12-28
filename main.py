from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


# create flask item to manage server
app = Flask(__name__)

# connect to/create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)


# create new task, pulling just the title from the entry
def add_task():
    task_name = request.form['name']
    status = False
    new_task = Task(
        name=task_name,
        completed=status
    )
    db.session.add(new_task)
    db.session.commit()


def complete_task():
    # check for all checked tasks and compare name to db for matches
    update_status = request.form.getlist('checkboxtask')
    list_of_tasks = Task.query.filter_by(name=update_status[0]).all()

    uncompleted_tasks = []

    # append all tasks with uncompleted status to new list
    for count, task in enumerate(list_of_tasks):
        if not task.completed:
            uncompleted_tasks.append(list_of_tasks[count])

    # iterate from beginning of list to max range of length of checkmark boxes and mark as complete
    for item in uncompleted_tasks[0:len(update_status)]:
        setattr(item, 'completed', True)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    # feed tasks to index.html to have list of all items
    tasks = db.session.query(Task).all()
    if request.method == 'POST':
        add_task_button = request.form.get('add_task_button')
        completed_button = request.form.get('completed_button')
        if add_task_button is not None:
            add_task()
        elif completed_button is not None:
            complete_task()
        return redirect(url_for('index'))
    return render_template('index.html', tasks=tasks)


@app.route('/completed-tasks', methods=['GET'])
def completed_tasks():

    tasks = db.session.query(Task).all()
    marked_complete_tasks = []
    for task in tasks:
        if task.completed:
            marked_complete_tasks.append(task)
    return render_template('completed_tasks.html', tasks=marked_complete_tasks)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
