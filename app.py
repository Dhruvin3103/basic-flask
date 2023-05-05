from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_create = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/home', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home')
        except:
            return 'Errors'
    else:
        tasks = Todo.query.order_by(Todo.date_create).all()
        return render_template('index.html', task=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/home')

    except:
        return "Errors"

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/home')
        except:
            return "errors"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
