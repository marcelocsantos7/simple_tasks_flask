from  flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Task {self.id}"

@app.route('/', methods=['GET', 'POST'])
def index():
    #add a task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    update_task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        update_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template('edit.html', task=update_task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)