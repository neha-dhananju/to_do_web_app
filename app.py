from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'todo.db'

# Create DB table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')

# Home route – show tasks and form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute('INSERT INTO tasks (content) VALUES (?)', (task_content,))
        return redirect(url_for('index'))

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT id, content FROM tasks')
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

# Delete route
@app.route('/delete/<int:task_id>')
def delete(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

# Initialize DB when starting the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
